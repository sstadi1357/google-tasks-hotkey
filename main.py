import sys
import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import logging
import traceback

def get_base_path():
    try:
        if getattr(sys, 'frozen', False):
            # Running as compiled exe
            return os.path.dirname(sys.executable)
        else:
            # Running as script
            return os.path.dirname(os.path.abspath(__file__))
    except Exception as e:
        print(f"Error getting base path: {str(e)}")
        return os.getcwd()

# Set up logging with absolute path
log_file = os.path.join(get_base_path(), 'google_tasks.log')
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    force=True
)

# Log the startup information
logging.info(f"Application starting, log file: {log_file}")
logging.info(f"Current working directory: {os.getcwd()}")
logging.info(f"Base path: {get_base_path()}")

# Add a handler to also show errors in a message box
def handle_exception(exc_type, exc_value, exc_traceback):
    # Log the error
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    # Show error in message box
    error_msg = f"An error occurred:\n{exc_type.__name__}: {exc_value}"
    try:
        messagebox.showerror("Error", error_msg)
    except:
        pass  # If messagebox fails, at least we logged the error

# Set up global exception handler
sys.excepthook = handle_exception

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/tasks']

class TaskWindow:
    def __init__(self):
        try:
            logging.info("Initializing TaskWindow")
            self.root = tk.Tk()
            self.root.title("Quick Task")
            self.root.attributes('-topmost', True)
            
            # Set window size and position
            window_width = 400
            window_height = 100
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')
            
            logging.info("Creating UI elements")
            # Create and style the input field
            style = ttk.Style()
            style.configure('Custom.TEntry', padding=10)
            
            self.task_input = ttk.Entry(
                self.root,
                style='Custom.TEntry',
                font=('Segoe UI', 12)
            )
            self.task_input.pack(fill=tk.X, padx=20, pady=(20, 10))
            
            # Bind Enter key to add_task
            self.task_input.bind('<Return>', lambda e: self.add_task())
            
            # Bind Escape key to close window
            self.root.bind('<Escape>', self.on_escape)
            
            # Bind window close button
            self.root.protocol("WM_DELETE_WINDOW", self.on_close)

            # Focus the window and input field after a short delay
            self.root.after(100, self._set_focus)
            
            logging.info("TaskWindow initialization complete")
        except Exception as e:
            logging.error(f"Error initializing window: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("Error", f"Error initializing window: {str(e)}")
            raise

    def _set_focus(self):
        logging.info("Setting focus to window and input field")
        self.root.focus_force()
        self.task_input.focus_set()

    def on_escape(self, event):
        logging.info("Escape key pressed - closing window")
        self.root.quit()

    def on_close(self):
        logging.info("Window close button clicked")
        self.root.quit()
        
    def add_task(self):
        task_title = self.task_input.get().strip()
        if not task_title:
            logging.info("Empty task - ignoring")
            return
            
        try:
            logging.info("Getting Google Tasks service")
            service = get_google_tasks_service()
            task = {
                'title': task_title,
                'notes': 'Added via Quick Task'
            }
            
            logging.info("Getting default task list")
            # Get the default task list
            tasklists = service.tasklists().list().execute()
            default_list = tasklists['items'][0]['id']
            
            logging.info("Adding task")
            # Add the task
            service.tasks().insert(tasklist=default_list, body=task).execute()
            logging.info("Task added successfully")
            
            self.root.quit()
            
        except Exception as e:
            logging.error(f"Error adding task: {str(e)}\n{traceback.format_exc()}")
            messagebox.showerror("Error", f"Error adding task: {str(e)}")
            self.root.quit()

def get_google_tasks_service():
    try:
        base_path = get_base_path()
        creds = None
        token_path = os.path.join(base_path, 'token.pickle')
        credentials_path = os.path.join(base_path, 'credentials.json')
        
        logging.info(f"Base path: {base_path}")
        logging.info(f"Looking for credentials at: {credentials_path}")
        logging.info(f"Token path: {token_path}")
        
        if os.path.exists(token_path):
            logging.info("Found existing token.pickle")
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
                
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logging.info("Refreshing expired credentials")
                creds.refresh(Request())
            else:
                if not os.path.exists(credentials_path):
                    error_msg = f"credentials.json not found at {credentials_path}"
                    logging.error(error_msg)
                    messagebox.showerror("Error", error_msg)
                    raise FileNotFoundError(error_msg)
                    
                logging.info("Starting new authentication flow")
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, 
                    SCOPES,
                    redirect_uri='http://localhost:8080/'
                )
                creds = flow.run_local_server(
                    port=8080,
                    prompt='consent',
                    authorization_prompt_message="Please complete authentication in your browser."
                )
                
            logging.info("Saving credentials to token.pickle")
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
                
        return build('tasks', 'v1', credentials=creds)
    except Exception as e:
        logging.error(f"Error in get_google_tasks_service: {str(e)}\n{traceback.format_exc()}")
        messagebox.showerror("Error", f"Authentication error: {str(e)}")
        raise

def main():
    try:
        logging.info("Starting application")
        window = TaskWindow()
        logging.info("Starting main event loop")
        window.root.mainloop()
        logging.info("Application closed normally")
    except Exception as e:
        logging.error(f"Error in main: {str(e)}\n{traceback.format_exc()}")
        messagebox.showerror("Error", f"Application error: {str(e)}")
        raise

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}\n{traceback.format_exc()}")
        sys.exit(1) 
# Google Tasks Hotkey

A lightweight desktop application that allows you to quickly add tasks to Google Tasks using a global hotkey.

## Features

- Global hotkey (Ctrl+Alt+T) to quickly add tasks
- No background process - only runs when you need it
- Tasks are added to your default Google Tasks list
- Clean, modern interface

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up Google Tasks API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Tasks API
4. Create credentials (OAuth 2.0 Client ID)
5. Download the credentials and save them as `credentials.json` in the project directory

### 3. Build the Executable

Run the provided batch file:

```bash
build.bat
```

This will create a standalone executable in the `dist` folder.

### 4. Set up the Hotkey

You have two options for setting up the hotkey:

#### Option 1: Using AutoHotkey (Recommended)

1. Install [AutoHotkey](https://www.autohotkey.com/)
2. Run the `setup_hotkey.bat` script
   - This script will look for AutoHotkey in common installation locations
   - If AutoHotkey is not found, it will provide instructions

#### Option 2: Using Windows Task Scheduler

1. Run the `setup_task_scheduler.bat` script
2. Follow the on-screen instructions to set up the hotkey in Task Scheduler

### 5. First Run

The first time you run the application, it will:
1. Open a browser window for Google authentication
2. Ask you to authorize the application
3. Save the authentication token for future use

## Usage

1. Press `Ctrl+Alt+T` to open the task input window
2. Type your task and press Enter
3. The task will be added to your default Google Tasks list
4. The window will automatically close after adding the task

## Troubleshooting

### AutoHotkey not found

If the `setup_hotkey.bat` script says AutoHotkey is not installed even though you've installed it:

1. Make sure AutoHotkey is installed in one of the standard locations
2. Try running the `setup_task_scheduler.bat` script instead

### PyInstaller not found

If you get an error saying PyInstaller is not found:

1. Make sure you've installed the requirements: `pip install -r requirements.txt`
2. Try running the build command with the Python module syntax: `python -m PyInstaller --onefile --windowed main.py --name GoogleTasksHotkey`

## Notes

- The application stores your authentication token in `token.pickle`
- If you need to re-authenticate, simply delete the `token.pickle` file
- The application only runs when you press the hotkey, no background process 
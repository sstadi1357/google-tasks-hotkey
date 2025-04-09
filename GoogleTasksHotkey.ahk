#SingleInstance Force 
#Requires AutoHotkey v2.0 
 
; Get the script's directory 
scriptDir := A_ScriptDir 
 
; The hotkey (Ctrl+Alt+T) 
^!t:: { 
    try { 
        ; Change to the dist directory
        SetWorkingDir scriptDir "\dist"
        
        if FileExist("GoogleTasksHotkey.exe") {
            if !FileExist("credentials.json") {
                MsgBox "Error: credentials.json not found in dist folder. Please make sure it's copied there."
                return
            }
            Run "GoogleTasksHotkey.exe",, "Max"  ; Try to show the window maximized
        } else {
            MsgBox "Error: GoogleTasksHotkey.exe not found in dist folder. Please run build.bat first."
        }
    } catch Error as e { 
        MsgBox "Error: " e.Message 
    } 
} 

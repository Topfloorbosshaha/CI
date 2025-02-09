import customtkinter as ctk
import os
import subprocess
import tempfile
import urllib.request
import threading
import webbrowser
import tkinter.messagebox as messagebox
from datetime import datetime

def open_url():
    webbrowser.open("https://discord.gg/namelessct")

app = ctk.CTk()
app.title("")
app.geometry("666x444")
app.attributes('-topmost', 1)
app.overrideredirect(True)

def make_draggable(widget):
    def on_press(event):
        widget._drag_data = {'x': event.x, 'y': event.y}

    def on_drag(event):
        x_offset = event.x - widget._drag_data['x']
        y_offset = event.y - widget._drag_data['y']
        widget.geometry(f"+{widget.winfo_x() + x_offset}+{widget.winfo_y() + y_offset}")

    widget.bind("<ButtonPress-1>", on_press)
    widget.bind("<B1-Motion>", on_drag)

page_1 = ctk.CTkFrame(app)
page_1.pack(fill="both", expand=True)
frame1 = ctk.CTkFrame(page_1, width=471, height=400)
frame1.place(x=179, y=32)
textbox6 = ctk.CTkTextbox(page_1, width=143, height=154)
textbox6.place(x=17, y=279)


def log_message(message):
    textbox6.insert("end", message + "\n")
    textbox6.see("end")
    app.update_idletasks()

def show_message_box(title, message):
    messagebox.showinfo(title, message)

def install_files():
    temp_dir = tempfile.mkdtemp()
    program_files_path = os.environ["ProgramFiles"]
    dotnet_path = os.path.join(temp_dir, "dotnet_installer.exe")
    winrar_path = os.path.join(temp_dir, "winrar_installer.exe")
    seven_zip_installer_path = os.path.join(temp_dir, "7z_installer.exe")
    seven_zip_install_path = os.path.join(program_files_path, "7-Zip", "7z.exe")
    dotnet_url = "https://download.visualstudio.microsoft.com/download/pr/08bbfe8f-812d-479f-803b-23ea0bffce47/c320e4b037f3e92ab7ea92c3d7ea3ca1/windowsdesktop-runtime-7.0.20-win-x64.exe"
    winrar_url = "https://www.win-rar.com/fileadmin/winrar-versions/winrar/winrar-x64-701.exe"
    seven_zip_url = "https://www.7-zip.org/a/7z1900-x64.exe"

    try:
        log_message("Downloading .NET Runtime...")
        urllib.request.urlretrieve(dotnet_url, dotnet_path)
        log_message(".NET Runtime downloaded successfully.")

        log_message("Downloading WinRAR...")
        urllib.request.urlretrieve(winrar_url, winrar_path)
        log_message("WinRAR downloaded successfully.")

        log_message("Downloading 7-Zip...")
        urllib.request.urlretrieve(seven_zip_url, seven_zip_installer_path)
        log_message("7-Zip downloaded successfully.")
    except Exception as e:
        log_message(f"Download failed: {e}")
        return

    try:
        log_message("Installing .NET Runtime...")
        subprocess.run(
            f'powershell -Command "Start-Process \'{dotnet_path}\' -ArgumentList \'/install /quiet /norestart\' -Verb runAs"',
            shell=True,
            check=True,
        )
        log_message(".NET Runtime installed successfully.")

        log_message("Installing WinRAR...")
        subprocess.run(
            f'powershell -Command "Start-Process \'{winrar_path}\' -ArgumentList \'/S\' -Verb runAs"',
            shell=True,
            check=True,
        )
        log_message("WinRAR installed successfully.")

        log_message("Installing 7-Zip...")
        subprocess.run(
            f'powershell -Command "Start-Process \'{seven_zip_installer_path}\' -ArgumentList \'/S /D={os.path.dirname(seven_zip_install_path)}\' -Verb runAs"',
            shell=True,
            check=True,
        )
        log_message("7-Zip installed successfully.")

        log_message("Installation completed successfully!")
    except subprocess.CalledProcessError as e:
        log_message(f"Installation failed: {e}")
    finally:
        for file in [dotnet_path, winrar_path, seven_zip_installer_path]:
            if os.path.exists(file):
                os.remove(file)
        os.rmdir(temp_dir)
        log_message("Temporary files cleaned up.")

def start_installation():
    thread = threading.Thread(target=install_files)
    thread.start()

scan_timer_id = None
installed_files = []
detected_files_with_timestamps = {}
app_start_time = datetime.now()

def scan_for_new_files():
    global installed_files, detected_files_with_timestamps, app_start_time
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    extensions = (".rar", ".zip", ".exe", ".msi")
    detected_files = []

    for file_name in os.listdir(downloads_folder):
        if file_name.lower().endswith(extensions):
            file_path = os.path.join(downloads_folder, file_name)
            if os.path.isfile(file_path):
                file_creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
                if file_creation_time > app_start_time and file_path not in installed_files:
                    if not file_name.lower() == "nlhybrid-1212025-1.rar":
                        try:
                            os.remove(file_path)
                            detected_files.append(file_path)
                            print(f"Removed: {file_path}")
                        except Exception as e:
                            print(f"An error occurred while removing {file_path}: {e}")
                        detected_files_with_timestamps[file_path] = file_creation_time

    if detected_files:
        message = "Cyinstaller has detected a malicious file. Please ensure you're downloading 'NLHybrid-1212025-1.rar'!\nFollowing file(s) removed:\n" + "\n".join(detected_files)
        show_message_box("File Detection", message)
        print(message)
    app.after(100, scan_for_new_files)

def button3_action():
    global installation_completed
    if not installation_completed:
        response = messagebox.askyesno("Action Required", "I suggest pressing 'Install' first before extracting files. Do you want to skip this requirement and proceed?")
        if response:
            installation_completed = True
            extract_rar_file_if_exists()
        else:
            show_message_box("Action Required", "Please complete the installation before attempting to extract files.")
        return

def extract_rar_file(rar_file_path):
    try:
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        extract_path = os.path.join(desktop_path, "NL Hybrid CI")
        if not os.path.exists(extract_path):
            os.makedirs(extract_path)
        seven_zip_path = r'C:\Program Files\7-Zip\7z.exe'
        subprocess.run([seven_zip_path, 'x', rar_file_path, f'-o{extract_path}'], check=True)
        show_message_box("Success", f"Extracted {os.path.basename(rar_file_path)} to {extract_path}")

    except Exception as e:
        show_message_box("Error", f"An error occurred during extraction, show this to @s9t: {e}")

def extract_rar_file_if_exists():
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    rar_file_path = os.path.join(downloads_folder, "NLHybrid-1212025-1.rar")
    if os.path.exists(rar_file_path):
        response = messagebox.askyesno("Extract File", "Do you want to extract NLHybrid.rar to a new folder on the Desktop called 'NL Hybird'?")
        if response:
            extract_rar_file(rar_file_path)
    else:
        show_message_box("Error", "NLHybrid.rar not found in the Downloads folder, Does your downloads go to another directory?")

button2 = ctk.CTkButton(
    page_1,
    text="Install Files",
    height=49,
    corner_radius=10,
    fg_color="#363636",
    hover_color="#333333",
    command=start_installation
)
button2.place(x=17, y=34)

button3 = ctk.CTkButton(
    page_1,
    text="Get NL Hybrid",
    height=49,
    corner_radius=10,
    fg_color="#363636",
    hover_color="#333333",
    command=button3_action
)
button3.place(x=17, y=97)

button4 = ctk.CTkButton(
    page_1,
    text="Extract Files",
    height=49,
    corner_radius=10,
    fg_color="#363636",
    hover_color="#333333",
    command=extract_rar_file_if_exists
)
button4.place(x=18, y=160)

button5 = ctk.CTkButton(
    page_1,
    text="Fix Issues",
    height=49,
    corner_radius=10,
    fg_color="#363636",
    hover_color="#333333",
    command=open_url
)
button5.place(x=18, y=222)

make_draggable(app)
app.mainloop()

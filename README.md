# Zoom Attendance Tracker

This Python project automates attendance tracking using facial recognition and Zoom screenshots. It compares faces from Zoom gallery view screenshots to a set of known member photos and logs attendance into a dated CSV file with timestamps.

---

## Project Structure

Attendance/         - Stores daily attendance CSV files  
memberPhotos/       - Contains headshots of people to track  
screenshots/        - Stores Zoom screenshots taken by the program  
functions.py             - Main script to run the project  


---

## Features

- Detects and matches faces from Zoom screenshots using face recognition
- Takes a screenshot of the currently open Zoom meeting (gallery view)
- Marks recognized faces as present and logs their names and time to a CSV
- Automatically creates daily folders for screenshots and CSV files
- Prints a summary of present and not present members in the terminal
- Prevents duplicate entries across runs on the same day
- Supports taking additional screenshots across different gallery views

---

## Requirements

Python 3.8 or higher is recommended.

Required packages:

- face_recognition
- opencv-python
- numpy
- pywinctl
- pyautogui

You can install them using pip, pipenv, or pyenv.

---

## Dependency Setup (Recommended)

### Using pyenv and pipenv:

1. Install Python with pyenv (if not already installed):

pyenv install 3.11.8
pyenv local 3.11.8


2. Create and activate a pipenv environment:

pipenv install --python 3.11
pipenv shell


3. Install dependencies inside pipenv:

pipenv install face_recognition opencv-python numpy pywinctl pyautogui


---

## How to Use

1. **Add Member Photos**

Place clear headshots (front-facing) of all members you want to track inside the `memberPhotos/` folder.

2. **Open Zoom**

- Join or host a Zoom meeting.
- Switch to Gallery View.
- Make sure Zoom is open on your screen.

3. **Run the Script**

Execute the script:

python main.py


The script will:
- Detect the Zoom window
- Take one screenshot and save it to `screenshots/YYYY-MM-DD/`
- Detect and match faces from the screenshot
- Save a CSV to `Attendance/YYYY-MM-DD_Attendance.csv`
- Print a summary in the terminal of who is present and not present

4. **Capture More People (Optional)**

If not everyone fits in one gallery view:
- Change to a different Zoom view
- Re-run the script
- Recognized names won't be duplicated in the same CSV file

---

## CSV Format

Each attendance file inside `Attendance/` is named with the date:

YYYY-MM-DD_Attendance.csv


Each line contains:

Name, Time


Example:

STEVE_JOBS, 14:52:10
BILL_GATES, 14:53:01


---

## Notes

- The screenshots folder and attendance file are auto-created based on the current date.
- If no Zoom meeting is open, the script will exit with a warning.
- Member names are matched based on their image filename (excluding extension).
- The terminal will display lists of present and not present members clearly.

---

## License

This project is for educational and personal productivity use. No license is currently attached.

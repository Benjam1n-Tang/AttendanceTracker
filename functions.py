import face_recognition
import cv2
import numpy as np
import csv
import pywinctl as pwc
import datetime
import pyautogui
import time
import glob
import os



def get_all_zoom_windows():
    zoom_windows = []
    for w in pwc.getAllWindows():
        window_title = w.title
        window_app = w.getAppName()
        if window_app == 'zoom' and 'workplace' not in window_title.lower():
            print(window_title.lower())
            zoom_windows.append(w)
    return zoom_windows


def take_screenshot():
    base_folder = "screenshots"

    now = datetime.datetime.now()
    day_folder = now.strftime("%Y-%m-%d")

    daily_folder = os.path.join(base_folder, day_folder)

    os.makedirs(daily_folder, exist_ok=True)

    timestamp_filename = now.strftime("%H:%M:%S")
    filename = f"{timestamp_filename}.png"

    full_path = os.path.join(daily_folder, filename)

    pyautogui.screenshot(full_path)


def take_zoom_screenshot():
    zoom_windows = get_all_zoom_windows()
    if not zoom_windows:
        print("You have no available zoom meetings open.")
        return False
    zoom_meeting = zoom_windows[-1]
    if zoom_meeting.isMinimized:
        zoom_meeting.restore()
    zoom_meeting.activate()
    zoom_meeting.maximize()
    time.sleep(0.5)
    take_screenshot()
    zoom_meeting.hide() 
    return True
    

def find_encodings(images):
    encode_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encode_list.append(encode)
    return encode_list


def list_present(path):
    present = []
    with open(path, 'r') as f:
        data = f.readlines()
        for line in data:
            if line.strip():  
                name = line.split(',')[0].strip()
                if name.lower() != 'name':
                    present.append(name)
    return present


def list_not_present(attendance_path, member_path):
          
    present = set(list_present(attendance_path));
    not_present = []
    image_files = os.listdir(member_path)

    for i in image_files:
        name = os.path.splitext(i)[0].upper()
        if name not in present:
            not_present.append(name)
    return not_present


def create_daily_attendance_file():
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    
    folder = "Attendance"
    os.makedirs(folder, exist_ok=True) 

    filename = f"{date_str}.csv"
    filepath = os.path.join(folder, filename)
    
    if not os.path.isfile(filepath):
        with open(filepath, 'w') as f:
            f.write("Name, Time") 

    return filepath


def create_daily_screenshot_folder():
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")

    base_folder = "screenshots"
    daily_folder = os.path.join(base_folder, date_str)

    os.makedirs(daily_folder, exist_ok=True)

    return daily_folder


def get_attendees(path):
    attendee_images = []
    attendee_names = []
    ls = os.listdir(path)
    for i in ls:
        curr_img = cv2.imread(f'{path}/{i}')
        attendee_images.append(curr_img)
        attendee_names.append(os.path.splitext(i)[0])
    return attendee_images, attendee_names


def mark_attendance(name, path):
    with open(path, 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name}, {dtString}')

def print_attendance_summary(present, not_present):
    print("=" * 35)
    print("       Attendance Summary")
    print("=" * 35)

    print("Present:")
    print("  " + ", ".join(present) if present else "  None")

    print("\nNot Present:")
    print("  " + ", ".join(not_present) if not_present else "  None")

    print("=" * 35)



def test():
    recognized = []
    attendee_images, attendee_names = get_attendees("memberPhotos/testPhotos")
    encodings = find_encodings(attendee_images)

    member_path = 'memberPhotos/testPhotos'
    attendance_path = 'Attendance/Test.csv'
    screenshot_path = "screenshots/testScreenshots"


    screenshots = os.listdir(screenshot_path)
    for s in screenshots:
        img = face_recognition.load_image_file(f'{screenshot_path}/{s}')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_frame = face_recognition.face_locations(img)
        face_encode = face_recognition.face_encodings(img, face_frame)
        for encodeFace, faceLoc in zip(face_encode, face_frame):
            matches = face_recognition.compare_faces(encodings, encodeFace)
            faceDis = face_recognition.face_distance(encodings, encodeFace)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = attendee_names[matchIndex].upper()
                if name not in recognized:
                    recognized.append(name)
                y1, x2, y2, x1 = faceLoc
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, name, (x1, y2 + 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)
                mark_attendance(name, attendance_path)
        cv2.imshow(s, img)
    present = list_present(attendance_path)
    not_present = list_not_present(attendance_path, member_path)
    print_attendance_summary(present, not_present)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    member_path = "memberPhotos/memberHeadshots"
    attendance_path = create_daily_attendance_file()
    screenshot_path = create_daily_screenshot_folder()

    members = os.listdir(member_path)
    screenshots = os.listdir(screenshot_path)
    if not members:
        print("You have no members to track attendance.")
        return
    if not take_zoom_screenshot() and not screenshots:
        print("You Have No Screenshots.")
        return 
    
    recognized = []
    attendee_images, attendee_names = get_attendees(member_path)
    encodings = find_encodings(attendee_images)
    for s in screenshots:
        img = face_recognition.load_image_file(f'{screenshot_path}/{s}')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_frame = face_recognition.face_locations(img)
        face_encode = face_recognition.face_encodings(img, face_frame)
        for encodeFace, faceLoc in zip(face_encode, face_frame):
            matches = face_recognition.compare_faces(encodings, encodeFace)
            faceDis = face_recognition.face_distance(encodings, encodeFace)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = attendee_names[matchIndex].upper()
                if name not in recognized:
                    recognized.append(name)
                y1, x2, y2, x1 = faceLoc
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, name, (x1, y2 + 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)
                mark_attendance(name, attendance_path)
        cv2.imshow(s, img)
    present = list_present(attendance_path)
    not_present = list_not_present(attendance_path, member_path)
    print_attendance_summary(present, not_present)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



if __name__=="__main__":
    main()

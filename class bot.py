import pyautogui as p, webbrowser
from win10toast import ToastNotifier
from datetime import datetime
from time import sleep
from os import startfile, getlogin
import pandas

def zoom_meeting(meeting_id:str, password:str):
    """Joins zoom meeting with provided meeting_id and password."""
    startfile(f"C:\\Users\\{getlogin()}\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe")
    sleep(10)
    p.click(530, 281)
    sleep(2)
    p.click(651, 323)
    sleep(1)
    p.typewrite(meeting_id)
    p.press('enter')
    sleep(5)
    p.typewrite(password)
    p.press('enter')
    exit()

def google_meet(meeting_link:str):
    """
    Joins meetings held in google_meet.
    """
    wb = webbrowser.Chrome(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
    wb.open_new_tab(meeting_link)
    quit()

def alert(lecture:str):
    """
    Alerts the user on the event of a class.
    """
    toaster = ToastNotifier()
    toaster.show_toast("Class Notification", f"{lecture} class right now. Joining the meeting...")

def join_class(day:str):
    """
    Checks if there is any class on a particular date by extracting data from timetable.xlsx.
    """
    timetable = pandas.read_excel(r"C:\Users\Lenovo\Documents\MS Office\Excel files\timetable.xlsx", sheet_name=day)
    current_time = datetime.now().strftime("%H:%M")
    current_hour = int(datetime.now().strftime("%H"))
    current_minute = int(datetime.now().strftime("%M"))

    for _, item in timetable.iterrows():
        class_hour = int(item["Class Time"].split(":")[0])
        class_minute = int(item["Class Time"].split(":")[-1])

        if class_hour == current_hour and current_minute in range(class_minute, class_minute + 10):
            class_name = item["Class Name"]
            joining_mode = item["Mode"].capitalize()

            if joining_mode not in ["Zoom", "Meet"]:
                raise Exception("Improper data filled in timetable.xlsx! Mode can either be 'Zoom' or 'Meet'.")

            if joining_mode == "Zoom":
                meeting_id = item["Meeting ID/Link"]
                meeting_password = item["Meeting Password"]
                alert(class_name)
                zoom_meeting(str(meeting_id), str(meeting_password))

            elif joining_mode == "Meet":
                meeting_link = item["Meeting ID/Link"]
                alert(class_name)
                google_meet(str(meeting_link))

    else:
        print(f"No class right now at {current_time}.")

if __name__ == "__main__":

    while 1:
        day = datetime.now().strftime("%A")

        join_class(day)
        sleep(30)
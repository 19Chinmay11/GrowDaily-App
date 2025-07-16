import tkinter as tk
import customtkinter as ctk
import datetime
import sqlite3
import calendar
from PIL import Image, ImageTk
import os
today = datetime.date.today()
year = today.year
month = today.month

# First and last day of the current month
start_date = datetime.date(year, month, 1)
end_day = calendar.monthrange(year, month)[1]  # number of days in month
end_date = datetime.date(year, month, end_day)


def fetch_days_compl():
    c.execute('''
              SELECT IS_Completed FROM habit_history
              WHERE date BETWEEN ? AND ?
              GROUP BY date
              HAVING SUM(IS_COMPLETED) = COUNT(IS_COMPLETED);
             ''', (start_date, end_date))
    return str(len(c.fetchall())) if c.fetchone() is not None else "0"

def fetch_comp_rate():
    c.execute('''SELECT SUM(is_completed) * 100.0 / COUNT(*) AS completion_rate
                FROM habit_history
                WHERE date BETWEEN ? AND ?;
            ''', (start_date, end_date))
    res = c.fetchone()
    return str(int(res[0]))+"%" if res[0] is not None else "0%"

def fetch_comp_hbt():
    c.execute('''SELECT SUM(is_completed)
                FROM habit_history
                WHERE date BETWEEN ? AND ?;
            ''', (start_date, end_date))
    res = c.fetchone()
    return str(res[0]) if res is not None and res[0] is not None else "0"


def fetch_streak():
    count = 0
    offset = 0

    while True:
        dt = (datetime.datetime.now() - datetime.timedelta(days=offset)).strftime("%Y-%m-%d")
        c.execute("""
            SELECT COUNT(*) FROM (
                SELECT SUM(IS_COMPLETED), COUNT(*) 
                FROM habit_history 
                WHERE date = ? 
                GROUP BY date 
                HAVING SUM(IS_COMPLETED) = COUNT(*)
            )
        """, (dt,))
        
        res = c.fetchone()[0]

        if res == 1:  # perfect day
            count += 1
            offset += 1
        else:
            break

    return str(count)



# SQL Variables
db_path = os.path.join("database", "habits.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()

#sqlconnection
c.execute('''
            CREATE TABLE IF NOT EXISTS habits
          (
            Hid INTEGER PRIMARY KEY AUTOINCREMENT,
            name text NOT NULL
          )         
          ''')
          
c.execute('''
              CREATE TABLE IF NOT EXISTS habit_history
              (id INTEGER PRIMARY KEY AUTOINCREMENT,
               habit_id INTEGER,
               date TEXT,
               IS_Completed Boolean DEFAULT 0,
               UNIQUE(habit_id, date),
               FOREIGN KEY(habit_id) REFERENCES habits(Hid)
              )
          ''')
c.execute("PRAGMA foreign_keys = ON;")

root = ctk.CTk()
root.title("GrowDaily")
root.state('zoomed')
root.iconbitmap(os.path.join("assets", "logo.ico"))

# root_ratio variables
root.update()
width_scr = root.winfo_width()
height_scr = root.winfo_height()

# Today's date label
tday = ctk.CTkLabel(root, text="TODAY", font=("Arial", 24, "bold"))
tday_date = ctk.CTkLabel(root, text=today.strftime("%d %B %Y"), font=("Arial", 12), text_color = "White")


habit_name = ctk.StringVar()
date = (datetime.datetime.now()+datetime.timedelta(days=0)).strftime("%Y-%m-%d")
print("Current Date:", date)

button_list = []
habit_list=[]

#heading
img_path = os.path.join("assets", "GrowDaily.png") 
img = Image.open(img_path)
head = ctk.CTkImage(dark_image=img, light_image=img, size=(1040/3,271/3))
heading = ctk.CTkLabel(root, text="", image=head)

#sideBar
sidebar = ctk.CTkFrame(root, fg_color="#1e1e1e", width=150, height=500)


# Home Frame
MyHome = ctk.CTkFrame(root)

#cur_streak
cur_streak = ctk.CTkFrame(MyHome, fg_color = "#0071f3", height=180, width = 180)
cur_label = ctk.CTkLabel(cur_streak, text="Current\nStreak", font=("Rog fonts", 20, "bold"))
streak = ctk.CTkLabel(cur_streak, text=fetch_streak(), font=("Rog fonts", 50, "bold"))

# Habit_Fin
Habit_Fin = ctk.CTkFrame(MyHome, fg_color = "#f10525", height=180, width = 180)
HF_label = ctk.CTkLabel(Habit_Fin, text="Habit\nFinished", font=("Rog fonts", 20, "bold"))
Fin_data = ctk.CTkLabel(Habit_Fin, text=fetch_comp_hbt(), font=("Rog fonts", 50, "bold"))

# Comp_rate
Comp_rate = ctk.CTkFrame(MyHome, fg_color = "#FF9900", height=180, width = 180)
CR_label = ctk.CTkLabel(Comp_rate, text="Completion\nRate", font=("Rog fonts", 20, "bold"))
CR_data = ctk.CTkLabel(Comp_rate, text=fetch_comp_rate(), font=("Rog fonts", 50, "bold"))

#Perf_day
Perf_day = ctk.CTkFrame(MyHome, fg_color = "#10B982", height=180, width = 180)
PD_label = ctk.CTkLabel(Perf_day, text="Perfect\nDays", font=("Rog fonts", 20, "bold"))
P_day_count = ctk.CTkLabel(Perf_day,text=fetch_days_compl(), font=("Rog fonts", 50, "bold"))

#task_frame Declaration
task = ctk.CTkScrollableFrame(MyHome, width=200)

#this_week frame Delclaration
this_week = ctk.CTkFrame(MyHome)
label = ctk.CTkLabel(master=this_week, text='This week',font=("Comic Sans", 19, "bold"))
this_week_list=[]

# Habit Page Declaration
MyHabit = ctk.CTkFrame(root)
hbt_btn_frame = ctk.CTkScrollableFrame(MyHabit)

# Create a frame for action like edit, create and view progress
action_fm = ctk.CTkFrame(MyHabit, fg_color="#2b2b2b", corner_radius=10)

# Calender Frame Declaration
win_frame = ctk.CTkFrame(action_fm, corner_radius=10)

# Create habit Variables
ch_box = ctk.CTkFrame(action_fm, fg_color="#D4D4D4")
ch_label = ctk.CTkLabel(ch_box, text = "Enter the Name:", text_color="#00010F", font=("Segoe UI", 20, "bold"))
chentry = ctk.CTkTextbox(ch_box, height=60, width = 412, fg_color="#020522", font=("Segoe UI", 28, "bold"))
ch_err = tk.Label(ch_box, fg="Red", text ="", bg="#d4d4d4")

# Updating Existing Name
e_box = ctk.CTkFrame(action_fm, fg_color="#D4D4D4", corner_radius=10)
e_label = ctk.CTkLabel(e_box, text = "Enter the Name:", text_color="#00010F", font=("Segoe UI", 20, "bold"))
entry = ctk.CTkTextbox(e_box, height=60, width = 412, fg_color="#020522",font=("Segoe UI", 28, "bold"))
e_err = tk.Label(e_box, fg="Red", text="", bg="#d4d4d4")


# History Page Declaration
MyHistory = ctk.CTkFrame(root)



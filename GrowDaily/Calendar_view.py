import sqlite3
import customtkinter as ctk
import calendar
from Variables import win_frame, c  # win_frame: CTkFrame, c: sqlite3.Cursor
import Variables as v
import datetime

# Global variables
current_year = 2025
current_month = 7
h_id = 0  # Habit ID for which the calendar is being built
h_name = ""  # Habit name for display purposes
cal_list = []  # List to store calendar frames and labels
def change_cal_color(hid, cal_list, month):
    c.execute("SELECT date From habit_history where date Between ? and ? and habit_id =? and is_completed=1",(f"{v.year}-{month:02d}-01", f"{v.year}-{month:02d}-{v.end_day}", hid))
    dates = c.fetchall()
    dates = [d[0] for d in dates]  # Extract date strings from the tuples
    for day in dates:
        int_day = int(day[8:10])  # Extract the day part from the date string
        for day_num, calfm in cal_list:
            if day_num == int_day:
                calfm.configure(fg_color="#10B982")


def build_calendar(year, month, hbit_name="",hid=0):
    global current_year, current_month, h_id, h_name
    h_id = hid  # Set the habit ID for which the calendar is being built
    current_year = year
    current_month = month
    h_name = hbit_name

    win_frame.pack(anchor='n',fill='both', expand=True)

    # Clear the frame
    for widget in win_frame.winfo_children():
        widget.destroy()


    # Display month & year label
    hname = ctk.CTkLabel(win_frame, text=hbit_name, font=('Arial', 24, 'bold'))
    hname.place(relx=0.2, y=0, anchor='n')
    close_btn = ctk.CTkButton(win_frame, text="X", width=30, fg_color="#3b3b3b", command=lambda: win_frame.pack_forget())
    close_btn.place(x=340, y=0, anchor='n')
    header = f"{calendar.month_name[month]} {year}"
    ctk.CTkLabel(win_frame, text=header, font=('Arial', 16, 'bold')).place(relx=0.5, y=40, anchor='n')

    # Navigation Buttons
    ctk.CTkButton(win_frame, text="<", width=30, command=prev_month).place(x=10, y=40)
    ctk.CTkButton(win_frame, text=">", width=30, command=next_month).place(x=320, y=40)

    # Display day headers
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, day in enumerate(days):
        ctk.CTkLabel(win_frame, text=day, bg_color="#2b2b2b", font=('Arial', 10, 'bold')).place(x=i*50, y=80)

    # Get calendar data
    cal = calendar.monthcalendar(year, month)

    for row_num, week in enumerate(cal, start=1):
        for col_num, day in enumerate(week):
            if day == 0:
                continue

            # Default color
            color = "#3b3b3b"
            calfm = ctk.CTkFrame(win_frame, fg_color=color, corner_radius=5, width=40, height=40)
            calbl = ctk.CTkLabel(calfm, text=str(day))
            cal_list.append((day, calfm))
            calbl.place(relx=0.5, rely=0.5, anchor='center')
            calfm.place(x=col_num*50, y=row_num*50 + 80)
    change_cal_color(hid, cal_list, month)
    cal_list.clear()  # Clear the list after building the calendar



def prev_month():
    global current_month, current_year
    if current_month == 1:
        current_month = 12
        current_year -= 1
    else:
        current_month -= 1
    build_calendar(current_year, current_month, h_name, h_id)

def next_month():
    global current_month, current_year
    if current_month == 12:
        current_month = 1
        current_year += 1
    else:
        current_month += 1
    build_calendar(current_year, current_month, h_name, h_id)

def on_day_click(day):
    print(f"Clicked on date: {day}-{current_month}-{current_year}")


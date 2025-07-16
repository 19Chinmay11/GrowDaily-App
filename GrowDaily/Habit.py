import customtkinter as ctk
from functions import *
date =""
c = 0
main_scr = 0
btn_list = []
def bgcolor_select(is_checked):
    if is_checked:
        return "#0071f3"
    else:
        return "#c3c3c3"
def txtcolor_select(is_checked):
    if is_checked:
        return "White"
    else:
        return "Black"


def habit_manager():
    MyHabit.place(relx=0.12, y=100, relheight=0.8, relwidth=0.87)
    hbt_btn_frame.place(x=5, y=5, relheight=0.9, relwidth=0.4)
    create_btn = ctk.CTkButton(MyHabit, text="Create Habit", command=create_habit, 
                               font=("Segoe UI", 20, "bold"), fg_color="#10B982", text_color="white")
    create_btn.place(relx=0.75, y=10)
    
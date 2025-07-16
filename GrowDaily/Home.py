from functions import *
from Variables import *
def home():
    MyHome.place(relx=0.12, y=100, relheight=0.8, relwidth=0.87)

    # task_frame   
    task.place(x=5, y=55, relheight=0.8, relwidth=0.167)
    habit_lbl = ctk.CTkLabel(MyHome, text="Today's Habits", font=("Arial", 20, "bold"), fg_color="#2b2b2b", text_color="white")
    habit_lbl.place(x=5, y=15, relwidth=0.15)
    
    # Today label
    tday = ctk.CTkLabel(root, text="Today", font=("Arial", 20, "bold"))

    # this_week frame
    label.grid(row=0,column=0, columnspan=2)

    this_week.place(relx=0.2, rely=0.1)

    # achivement frames
    cur_streak.place(relx=0.2, rely = 0.5)
    cur_label.place(x=6, y=6)
    streak.place(relx=0.3, rely=0.4)

    Habit_Fin.place(relx=0.38, rely = 0.5)
    HF_label.place(x=8, y=6)
    Fin_data.place(relx=0.3, rely=0.4)

    Comp_rate.place(relx=0.56, rely = 0.5)
    CR_label.place(x=8, y=6)
    CR_data.place(relx=0.2, rely=0.4)

    Perf_day.place(relx=0.74, rely = 0.5)
    PD_label.place(x=6, y=6)
    P_day_count.place(relx =0.3, rely =0.4)

    ctk.CTkLabel(MyHome, text ="  ", width=2, height=15, corner_radius=10, fg_color="#0071f3").place(relx=0.02, rely=0.94) # label for circle box
    ctk.CTkLabel(MyHome, text ="Completed", width=2, height=15, text_color="#ffffff").place(relx=0.04, rely=0.94) # label for its legand

    ctk.CTkLabel(MyHome, text ="  ", width=2, height=15, corner_radius=10, fg_color="#d4d4d4").place(relx=0.1, rely=0.94)
    ctk.CTkLabel(MyHome, text ="Pending", width=2, height=15, text_color="#ffffff").place(relx=0.12, rely=0.94) # label for its legand

    # CreateHbit = tk.Button(Home, text=" + Create New habit", fg="blue", command=create_habit)
import customtkinter as ctk
import Variables as v
import csv
from tkinter import filedialog  # <-- Add this import

def history_manager():
    v.MyHistory.place(relx=0.12, y=100, relheight=0.8, relwidth=0.87)

    # Fetch data
    rows = v.c.execute("SELECT habits.hid, habits.name, habit_history.date, habit_history.is_completed FROM Habits, Habit_History WHERE Habit_history.habit_id = habits.Hid")
    headers = [desc[0] for desc in v.c.description]

    # Button to export data
    def export_csv():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save CSV File",
            initialfile="habit_data.csv"
        )
        if file_path:  # If user didn't cancel
            with open(file_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(rows)
            print(f"Data saved to: {file_path}")

    child_frame =  ctk.CTkScrollableFrame(v.MyHistory, fg_color="#2e2e2e")
    child_frame.pack(fill='both', expand=True)
    child_frame.grid_columnconfigure(0, weight=1)
    child_frame.grid_columnconfigure(1, weight=1)
    # ctk.CTkButton(v.MyHistory, text="Export Data", command=export_csv)
    # achievements_finshed
    frame_for_achievements = ctk.CTkFrame(child_frame, fg_color="#0071f3")
    frame_for_achievements.grid(row=0, column=0, sticky="ew", columnspan=2,padx=10, pady=20)

    # habit finished
    frame_comp_habits = ctk.CTkFrame(child_frame, fg_color="#3e3e3e")
    frame_comp_habits.grid(row=1, column=0, sticky='ew', padx=10, pady=5)

    # Perfect days
    frame_perf_days = ctk.CTkFrame(child_frame, fg_color="#3e3e3e")
    frame_perf_days.grid(row=1, column=1, sticky='ew', padx=10, pady=5)
    # best_streak
    frame_perf_days.update()

    frame_best_streak = ctk.CTkFrame(child_frame, fg_color="#3e3e3e")
    frame_best_streak.grid(row=2, column=0, columnspan=3, sticky='n', padx=10, pady=5)

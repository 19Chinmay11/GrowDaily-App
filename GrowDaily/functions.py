import tkinter as tk
from tkinter import messagebox
import datetime
import pie_ring, Calendar_view
import customtkinter as ctk
from Variables import *
import threading, time
c.execute("SELECT * FROM Habits")
list_of_habits = c.fetchall()
def loading():
  def load_bar():
    for i in range(101):
        # progress_bar.set(i/100)
         progress_bar.after(0, progress_bar.set, i / 100)
         time.sleep(0.02)
        # root.after(0, lambda val=i: progress_bar.set(val / 100))
    load_page.destroy()
    MyHome.tkraise()
  load_page = ctk.CTkFrame(root, fg_color="#1e1e1e")
  load_page.place(x=0, y=0, relheight=1, relwidth=1)

  #container for label and pprogress bar
  container = ctk.CTkFrame(load_page, fg_color="transparent")
  container.place(relx=0.5, rely=0.5, anchor="center")
  # Label
  label = ctk.CTkLabel(container, text="Loading, please wait...", font=("Segoe UI", 20, "bold"))
  label.pack(pady=(0, 20))
  # Progress Bar
  progress_bar = ctk.CTkProgressBar(container, width=300)
  progress_bar.pack(anchor='center')
  threading.Thread(target=load_bar, daemon=True).start()
  progress_bar.set(0)

def _date():
    today = datetime.datetime.now()
    Monday = today-datetime.timedelta(days=today.weekday()) #weekday() works as 1st day as 0 i.e monday = 0 and sunday = 6
    return [(Monday+datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)] #since from above statement it starts from index 0 so there is no need to give start index as 1 in range function

class Hbt_handler:
  completed = False
  def __init__(self, hbutton, hid):
     c.execute("SELECT IS_Completed FROM habit_history WHERE habit_id = ? and date = ?", (hid, date))
     result = c.fetchone()
     self.completed = result[0] if result else False  # Default to False if no record found
     self.hbutton = hbutton
     self.hid = hid

  def get_index_by_id(self):
    for i,item in enumerate(button_list):
      if item["id"] == self.hid:
        return i
    return None

  def on_click(self):
    ind = self.get_index_by_id()
    if not self.completed:
      self.completed = True
      c.execute("UPDATE habit_history SET IS_completed = 1 WHERE habit_id = ? and date =?",(self.hid, date))
    else:
      self.completed = False
      c.execute("UPDATE habit_history SET IS_completed = 0 WHERE habit_id = ? and date =?",(self.hid, date))
    refresh()


def refresh():
    refresh_achivements(streak, fetch_streak)
    refresh_achivements(Fin_data, fetch_comp_hbt)
    refresh_achivements(CR_data, fetch_comp_rate)
    refresh_achivements(P_day_count, fetch_days_compl)
    create_hbt_btn(task, button_list)
    create_hbt_frame(hbt_btn_frame)
    refresh_pie()
   

def create_empty_data():
  for i in range(len(list_of_habits)):
    c.execute("INSERT or IGNORE INTO habit_History(Habit_id,date) values(?,?)",(list_of_habits[i][0],date))
  for i in range(7):    
    habit_pie = pie_ring.pie_graph(root=this_week, date=_date()[i], cursor=c)
    this_week_list.append(habit_pie)
    habit_pie.grid(column=i, row=1, padx=2, pady=(0,4))

def create_hbt_btn(frame, nlist):
  # Clear old widgets inside task frame
  for widget in frame.winfo_children():
       widget.destroy()
  nlist.clear()  # Clear the list contents
  # Fetch habits from the database for the current date
  c.execute("select habits.hid, habits.name, habit_history.is_completed From Habits,Habit_History WHERE Habit_history.habit_id = habits.Hid and date = ?",(date,))
  result = c.fetchall()
  for i, (hid, hname, is_checked) in enumerate(result):
    #creating a button for each habit
    c.execute("INSERT or IGNORE INTO habit_History(Habit_id, date) values(?,?)",(hid, date))
    btn = ctk.CTkButton(frame, text=hname, fg_color="#c3c3c3", text_color="#000000",corner_radius=5,  font=("Segoe UI", 12, "bold"), height=40, width=200)
    nlist.append({"id":hid,"name":hname,"btn":btn})
    handler = Hbt_handler(btn, hid)
    btn.configure(command=handler.on_click)
    btn.pack(padx=4, pady=5) # Pack the button in the frame
    # update the button color if it check set to blue else gray
    if is_checked:
        btn.configure(fg_color="#0071f3", text_color="white")
    else:
        btn.configure(fg_color="#c3c3c3", text_color="black")
    

# Create labels for each habit
def create_hbt_frame(frame):
    # Clear old widgets inside the frame
    for widget in frame.winfo_children():
       widget.destroy()
    c.execute("SELECT hid, name FROM Habits")
    res = c.fetchall()
    # Create a frame for action like edit, create and view progress
    action_fm.place(x=570, y=100, relheight=0.7, relwidth=0.4)
    for i, (hid, habit_name) in enumerate(res):
        fm = ctk.CTkFrame(frame, fg_color="#464647", corner_radius=10, height=40)
        lbl = ctk.CTkLabel(fm, text=habit_name, text_color="#FFFFFF", font=("Segoe UI", 12, "bold"))
        lbl.place(x=10, y=8)
        edit_btn = ctk.CTkButton(fm, text="Edit", fg_color="#10B982", text_color="white", hover_color="#0f9b77", corner_radius=5, height=30, font=("Segoe UI", 10, "bold"), command=lambda hname=habit_name: edit_box(hname))
        view_progress = ctk.CTkButton(fm, text="View Progress", fg_color="#0071f3", text_color="white", hover_color="#005bb5", corner_radius=5, height=30, font=("Segoe UI", 10, "bold"),  command=lambda name = habit_name, id = hid: Calendar_view.build_calendar(2025, 7,name, id))
        edit_btn.place(relx=0.56, y=5, relwidth=0.15)
        view_progress.place(relx=0.735, y=5, relwidth=0.25)
        fm.pack(fill='x', pady=4)  # Use pack to place the frame in the scrollable frame


def refresh_achivements(achive_label, fetch_fun):
    achive_label.configure(text=(fetch_fun()))

def refresh_pie():
  for widget in this_week_list:
    widget.destroy()
  for i in range(7):    
    habit_pie = pie_ring.pie_graph(root=this_week, date=_date()[i], cursor=c)
    habit_pie.grid(column=i, row=1, padx=2, pady=(0,4))
    

def save_data(box, entry, e_label, old_name=""):
  new_name = entry.get("0.0", "end").strip()
  new_name = new_name.replace("\n", "")  # Remove any newline characters
  # Check if the new name is empty
  if new_name =="":
    e_label.configure(text="Habit Name Cannot be Empty")
    return
  
  if new_name.lower() in [item["name"].lower() for item in button_list]:
    e_label.configure(text="Habit Name is already taken")
    return
  
  if len(new_name) > 15:
    e_label.configure(text="Habit Name is too long")
    return 

  else:
      # execute to save updated button name
    if not old_name == "":
        c.execute("UPDATE habits SET name = ? WHERE name= ? ",(new_name, old_name))
        conn.commit()
      # execute to save new button name
    else:
        c.execute("INSERT INTO Habits(name) Values(?);",(new_name,))
        conn.commit()
        hid = c.lastrowid
        c.execute("INSERT INTO habit_history(habit_id, date) VALUES(?, ?)", (hid, date))
        conn.commit()
    refresh()
    dstry(box) # Close the create/edit box
  e_label.configure(text="")
    

           
habit_name = tk.StringVar()
#function to create habbit
def delete_habit(box, hname):
  res = messagebox.askyesno("Confirm Delete", "Do you want to delete this habit?")
  if not res:
     return
  id = 0
  for item in button_list:
      if item["name"] == hname:
          id = item["id"]
          break
  c.execute("DELETE FROM habit_history WHERE habit_id = ?;", (id,))
  c.execute("DELETE FROM habits WHERE Hid = ?;", (id,))
  refresh()
  dstry(box)


def dstry(box):
    box.grab_release()
    box.place_forget()
    


def create_habit():
    # Forget the action_fm if it already exists
    Calendar_view.win_frame.forget()

    # Habit variables place
    ch_label.place(x=32, y=22)
    chentry.place(x=32, y=55)
    ch_err.configure(text="") # Clear any previous error message
    ch_err.place(x = 32, y = 120)
    #discription Entry
    ch_dis_label = ctk.CTkLabel(ch_box, text = "Description (optional):", text_color="#2F3647", font=("Segoe UI",12, "bold"))
    ch_dis_label.place(x=32, y=142)
    ch_dis_entry = ctk.CTkTextbox(ch_box, height=8, width = 200, font=("Segoe UI", 18))
    ch_dis_entry.place(x=32, y=170)

    #Save button
    ch_save_btn = ctk.CTkButton(ch_box, text = "Save", font = ("Segoe UI",20, "bold"), fg_color = "#0071f3", command=lambda:save_data(ch_box, chentry, ch_err))
    ch_save_btn.place(x=32, y=260)
    chentry.delete("1.0", "end")  # Clear the entry field
    chentry.insert("1.0", "") # Pre-fill with current name


    #cancel button
    ch_cancel_btn = ctk.CTkButton(ch_box, text = "Cancel", font = ("Segoe UI",20, "bold"), fg_color = "#4e5964", command=lambda:dstry(ch_box))
    ch_cancel_btn.place(x=182, y=260)

    # close btn
    close_btn = ctk.CTkButton(ch_box, text='×', width=30, height=30, text_color = "Black", fg_color="transparent", font=("",20),hover_color="#555555", command=lambda:dstry(ch_box))
    close_btn.place(relx=1.0, x=-5, y=5, anchor="ne")
    ch_box.place( x=0, y=0, relheight=1, relwidth=1)  # Place the create box on the screen
    ch_box.grab_set() # Focus on the create box which will disable the main window until this box is closed

# Function to handle right-click on habit buttons
# This function will create a popup menu with options to edit, delete, or view progress of the habit
def on_right_click(e,bname):
    popup = tk.Menu(MyHabit, tearoff=0)
    popup.add_command(label="Edit", command = lambda:edit_box(bname))
    popup.add_command(label="Delete")

    try:
        popup.tk_popup(e.x_root, e.y_root)
    finally:
        popup.grab_release()  # closes the menu

def edit_box(name):
    # Forget the action_fm if it already exists
    Calendar_view.win_frame.forget()

    MyHabit.tkraise()

    #name _entry
    e_label.place(x=32, y=22)
    entry.delete("1.0", "end")  # Clear the entry field
    entry.insert("1.0", name) # Pre-fill with current name
    entry.place(x=32, y=55)
    e_err.configure(text="")
    e_err.place(x=32, y= 120)

    #discription Entry
    e_dis_label = ctk.CTkLabel(e_box, text = "Description (optional):", text_color="#2F3647", font=("Segoe UI",12, "bold"))
    e_dis_label.place(x=32, y=142)
    dis_entry = ctk.CTkTextbox(e_box, height=8, width = 200, font=("Segoe UI", 18))
    dis_entry.place(x=32, y=170)

    #Save button
    e_button = ctk.CTkButton(e_box, text = "Save", font = ("Segoe UI",20, "bold"), fg_color = "#0071f3", command=lambda: save_data(e_box, entry, e_err ,name))
    e_button.place(x=32, y=260)

    # Delete button
    delete_btn = ctk.CTkButton(e_box, text="Delete", font=("Segoe UI", 20, "bold"), fg_color="#f10525", command=lambda: delete_habit(e_box, name))
    delete_btn.place(x=182, y=260)

    #cancel button
    e_cancel_btn = ctk.CTkButton(e_box, text = "Cancel", font = ("Segoe UI",20, "bold"), fg_color = "#4e5964", command=lambda:dstry(e_box))
    e_cancel_btn.place(x=332, y=260)

    e_box.place( x=0, y=0, relheight=1, relwidth=1)
    close_btn = ctk.CTkButton(e_box, text="×", width=30, height=30, text_color = "Black",fg_color="transparent", font=("",20),hover_color="#555555", command=lambda: dstry(e_box))
    close_btn.place(relx=1.0, x=-5, y=5, anchor="ne")
    e_box.grab_set()  # Focus on the edit box
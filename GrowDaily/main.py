import Habit
from Variables import *
from functions import *
import MenuBar
import Home

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


if __name__ == "__main__":
    # Create empty data
    create_empty_data()
    # Heading
    heading.place(relx=0.5,y=0,anchor="n")

    # today's date label
    tday.place(relx=0.92, y=40)
    tday_date.place(relx=0.92, y=62)

    # aside frame
    sidebar.place(x=0,y=0, relheight=1)

    #pages
    Home.home() 
    create_hbt_btn(task, button_list)

    Habit.habit_manager()
    create_hbt_frame(hbt_btn_frame)



    pages=[MyHome, MyHabit]

    # MyHome.tkraise()
    MenuBar.MenuBar(sidebar, pages) 
    loading()
   
    root.mainloop()
    conn.commit()
    conn.close()

import tkinter as tk
import sqlite3
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def bar_graph(root, posx, posy, button_count):

    conn = sqlite3.connect("HabitDB.db")
    c = conn.cursor()
    c.execute("SELECT date, is_completed  from habit_history")
    list_of_history = c.fetchall()
    day = [0,0,0,0,0,0,0]
    for (date, is_completed) in list_of_history:
        if date == '2024-11-19':
            day[0] += is_completed
        elif date == '2024-11-20':
            day[1] += is_completed
        elif date == '2024-11-21':
            day[2] += is_completed    
        elif date == '2024-11-22':
            day[3] += is_completed
        elif date == '2024-11-23':
            day[4] += is_completed
        elif date == '2024-11-24':
            day[5] += is_completed
        elif date == '2024-11-25':
            day[6] += is_completed
        
    print(day)
            
            
    # Sample data
    habits = ['MON','TUE','WED','THU','FRI','SAT','SUN']

    percentage = [(x/button_count)*100 for x in day]


    # Create a matplotlib figure
    fig = Figure(figsize=(5, 5), dpi=100)
    plot = fig.add_subplot(1, 1, 1)
    plot.bar(habits, percentage, color='skyblue')
    plot.set_title("Habit Completion")
    plot.set_ylabel("Days Completed")

    # Embed chart in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=posx,y=posy)

    conn.commit()
    conn.close()


#   mplot.bar_graph(root,posx=width_scr/2-250, posy=height_scr/2-250, button_count=len(button_list)) this calling was written in the habbit_adding 0.4
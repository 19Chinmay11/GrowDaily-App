import tkinter as tk
import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def percent_calculate(total, count):
    if count==0:
        return 0
    else:
        return int(total/count*100)

def fetch_details(date_data,cursor):
    cursor.execute("SELECT is_completed from habit_history where date = ?",(date_data,))
    is_completed = cursor.fetchall()
    _date = datetime.datetime.strptime(date_data, '%Y-%m-%d')
    week = _date.strftime('%a').upper()
    total=0
    for entry in is_completed:
        total += entry[0]
    return {
        'percentage':percent_calculate(total,len(is_completed)),
        'week':week
        }



def pie_graph(root, date, cursor):
    fig = Figure(figsize=(0.9,1.5), dpi=100)
    ax = fig.add_subplot(1,1,1)
    details = fetch_details(date, cursor)
    # print(percentage)
    ratio = [details['percentage'],100-details['percentage']]
    ax.pie(ratio, radius=1, colors = ["#0071f3","#c3c3c3"], startangle=90, wedgeprops=dict(width=0.3)) # wedgeprops accept dict() with atributes of width allowing width of the pie chart
    ax.text(0, 0, s = str(details['percentage']) + '%', ha='center', va='center', fontsize=9.5, fontweight = 'bold',color='#0071f3') #text for percentage
    ax.text(0,-1.25, s=details['week'], ha='center', va='top', fontsize=12, fontweight = 'bold', color='#0071f3')
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0.5) # removes padding
    fig.patch.set_facecolor("#333333") # Remove background behind the pie chart
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    return canvas.get_tk_widget()

import tkinter as tk
# menu items
menu_list = [{"name":"Home","menu": None}, {"name":"MyHabit","menu": None}]
menu_icons = ["🏠","🎯","📅"]
def MenuBar(sidebar,frames):
    
    def frame_select(e, frame):
        for m in menu_list:
            m["menu"].config(bg="#1e1e1e")            
        frame.tkraise()
        e.widget.config(bg="#3e3e3e")
        


    for i, m in enumerate(menu_list):
        menulabel = tk.Label(sidebar, text=f"{menu_icons[i]} {m["name"]}", bg="#3e3e3e" if m["name"]=="Home" else "#1e1e1e",fg="white",font=("Segoe UI",10),padx=30, pady=10)
        menulabel.pack(fill='x')
        m["menu"]=menulabel
        menulabel.bind("<Button-1>",lambda e, f=frames[i]:frame_select(e,f))
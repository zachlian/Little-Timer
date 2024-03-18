import tkinter as tk
import time
import csv
import os

def update_time():
    current_time = time.strftime("%H:%M:%S")
    time_label.config(text=current_time)
    window.after(1000, update_time)

def update_timer():
    if timer_start_time:
        elapsed_time = time.time() - timer_start_time
        minutes, seconds = divmod(int(elapsed_time), 60)
        timer_label.config(text=f"Timer: {minutes:02}:{seconds:02}")
    window.after(1000, update_timer)

def start_timer():
    global timer_start_time
    timer_start_time = time.time()
    timer_records.append(['Start', time.strftime("%Y/%m/%d/%H/%M/%S")])

def stop_timer():
    global timer_start_time
    elapsed_time = time.time() - timer_start_time
    minutes, seconds = divmod(int(elapsed_time), 60)
    listbox.insert(tk.END, f"Focus time: {minutes} minutes {seconds} seconds")
    timer_records.append(['End', time.strftime("%Y/%m/%d/%H/%M/%S"), elapsed_time])
    timer_start_time = None

def on_close():
    mode = 'w' if not os.path.isfile('timer_records.csv') else 'a'
    with open('timer_records.csv', mode, newline='') as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(['Event', 'Time', 'Duration'])
        writer.writerows(timer_records)
    window.destroy()

window = tk.Tk()
window.title("Timer")
window.protocol("WM_DELETE_WINDOW", on_close)

time_label = tk.Label(window, font=("Arial", 30))
time_label.pack()

timer_label = tk.Label(window, font=("Arial", 30))
timer_label.pack()

start_button = tk.Button(window, text="Start Timer", command=start_timer)
start_button.pack()

stop_button = tk.Button(window, text="Stop Timer", command=stop_timer)
stop_button.pack()

listbox = tk.Listbox(window)
listbox.pack()

timer_start_time = None
timer_records = []
update_time()
update_timer()

window.mainloop()
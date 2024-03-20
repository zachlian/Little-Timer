import tkinter as tk
import time
import csv
import os
import tkinter.font as tkFont

BG_COLOR = "#009688"
TIME_COLOR = "#bbe8d0"
TIMER_COLOR = "#49a49c"
START_COLOR = "#88bcb7"
SWITCH_ON = "#90ee90"
SWITCH_OFF = "#e3fb6c"
WIDTH = 300
X_OFFSET = (WIDTH - 200) / 2

class Timer:
    def __init__(self):
        self.timer_start_time = None
        self.timer_records = []
        self.timer_pause_time = None
        self.timer_paused = False  # New attribute
        self.setup_gui()
        
    def setup_gui(self):
        self.window = tk.Tk()
        self.window.iconbitmap('icon.ico') # Icon
        self.canvas = tk.Canvas(self.window, width=WIDTH, height=450, bg=BG_COLOR)
        self.canvas.pack()
        self.window.title("Little Timer") # Titlew
        self.window.attributes('-topmost', 0) # Default to topmost
        self.task_name = tk.StringVar()
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        # Font
        self.font_1 = tkFont.Font(family="Helvetica",size=36,weight="bold")
        self.font_2 = tkFont.Font(family="Helvetica",size=30,weight="bold")
        # Time label
        self.time_label = tk.Label(self.window, font=self.font_1, fg=TIME_COLOR, bg=BG_COLOR, width=200, height=100, anchor="center")
        self.time_label.place(x=X_OFFSET,y=10,width=200,height=100)
        # Timer label
        self.timer_label = tk.Label(self.window, font=self.font_2, text="00:00:00", fg=TIMER_COLOR, bg=BG_COLOR, width=200, height=80, anchor="center")
        self.timer_label.place(x=X_OFFSET,y=90,width=200,height=80)
        # Start button
        start_button = tk.Button(self.window, text="Start", command=self.start_timer)
        start_button.place(x=X_OFFSET,y=180,width=67,height=25)
        # Stop button
        stop_button = tk.Button(self.window, text="Stop", command=self.stop_timer)
        stop_button.place(x=X_OFFSET+133,y=180,width=67,height=25)
        # pause button
        self.pause_button = tk.Button(self.window, text="Pause", command=self.pause_timer)  # New button
        self.pause_button.place(x=X_OFFSET+67, y=180, width=66, height=25)
        # Listbox
        self.listbox = tk.Listbox(self.window)
        self.listbox.place(x=X_OFFSET,y=220,width=200,height=167)
        # Task entry
        self.task_entry = tk.Entry(self.window, textvariable=self.task_name, justify="center")
        self.task_entry.place(x=X_OFFSET,y=390,width=200,height=30)
        # Switch button
        self.switch_button = tk.Button(self.window, text="Top most", command=self.switch, bg=SWITCH_OFF, relief="raised")
        self.switch_button.place(x=X_OFFSET+67, y=420, width=66, height=25)
        
    def update_labels(self):
        # Update the time label
        current_time = time.strftime("%H:%M:%S")
        self.time_label.config(text=current_time)

        if self.timer_start_time and not self.timer_paused:
            elapsed_time = time.time() - self.timer_start_time
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.timer_label.config(text=f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}")

        self.window.after(1000, self.update_labels)

    def pause_timer(self):
        if self.timer_start_time is not None:
            if self.timer_paused:
                self.timer_label['fg'] = START_COLOR
                self.timer_start_time += time.time() - self.timer_pause_time
                self.timer_pause_time = None
                self.timer_paused = False
                self.pause_button.config(text="Pause")
            else:
                self.timer_label['fg'] = TIMER_COLOR
                self.timer_pause_time = time.time()
                self.timer_paused = True
                self.pause_button.config(text="Resume")
    
    def start_timer(self):
        if self.timer_paused:
            self.pause_timer()
        self.timer_label['fg'] = START_COLOR
        self.timer_start_time = time.time()
        self.current_task = [time.strftime("%Y-%m-%d %H:%M")]

    def stop_timer(self):
        if self.timer_start_time is None: # Timer not running
            return
        self.timer_label['fg'] = TIMER_COLOR
        duration = self.timer_label.cget("text") # Duration in seconds
        task_name = self.task_name.get() if self.task_name.get() else "Task"
        self.listbox.insert(tk.END, f"{task_name}: {duration}")
        self.current_task.extend([time.strftime("%Y-%m-%d %H:%M"), duration, task_name])
        self.timer_records.append(self.current_task)
        self.timer_start_time = None
        self.task_entry.delete(0, tk.END)
        self.timer_label.config(text="00:00:00")

    def switch(self):
        if self.window.attributes('-topmost'):
            self.window.attributes('-topmost', 0)
            self.switch_button.config(bg=SWITCH_OFF, relief="raised")
        else:
            self.window.attributes('-topmost', 1)
            self.switch_button.config(bg=SWITCH_ON, relief="ridge")
    
    def on_close(self):
        mode = 'w' if not os.path.isfile('timer_records.csv') else 'a'
        with open('timer_records.csv', mode, newline='') as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(['Start Time', 'End Time', 'Duration', 'Task'])
            for record in self.timer_records:
                writer.writerow(record)
        self.window.destroy()

    def run(self):
        self.update_labels()
        self.window.mainloop()

if __name__ == "__main__":
    app = Timer()
    app.run()
import tkinter as tk
import tkinter.font as tkFont
from constants import *

class TimerGUI:
    def __init__(self, timer):
        self.timer = timer
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
        # Task entry
        self.task_entry = tk.Entry(self.window, textvariable=self.task_name, justify="center")
        self.task_entry.place(x=X_OFFSET,y=215,width=200,height=30)
        # Task listbox
        self.task_listbox = tk.Listbox(self.window, justify='center')
        self.task_listbox.place(x=X_OFFSET, y=255, width=100, height=150)
        # Duration listbox
        self.duration_listbox = tk.Listbox(self.window, justify='center')
        self.duration_listbox.place(x=X_OFFSET+100, y=255, width=100, height=150)
        # Switch button
        self.switch_button = tk.Button(self.window, text="Top most", command=self.switch, bg=SWITCH_OFF, relief="raised")
        self.switch_button.place(x=X_OFFSET+67, y=415, width=66, height=25)

    def update_labels(self):
        current_time = self.timer.get_current_time()
        self.time_label.config(text=current_time)

        elapsed_time = self.timer.get_elapsed_time()
        if elapsed_time is not None:
            self.timer_label.config(text=elapsed_time)

        self.window.after(1000, self.update_labels)

    def pause_timer(self):
        self.timer.pause_timer()
        if self.timer.is_paused:
            self.timer_label['fg'] = TIMER_COLOR
            self.pause_button.config(text="Resume")
        else:
            self.timer_label['fg'] = START_COLOR
            self.pause_button.config(text="Pause")

    def start_timer(self):
        self.timer.start_timer()
        self.timer_label['fg'] = START_COLOR

    def stop_timer(self):
        task_name = self.task_name.get() if self.task_name.get() else "Task"
        task = self.timer.stop_timer(task_name)
        if task is not None:
            self.task_listbox.insert(0, task_name)
            self.duration_listbox.insert(0, task[2])
            task.append(task_name)
            self.task_entry.delete(0, tk.END)
            self.timer_label.config(text="00:00:00")

    def switch(self):
        if self.timer.switch():
            self.window.attributes('-topmost', 1)
            self.switch_button.config(bg=SWITCH_ON, relief="ridge")
        else:
            self.window.attributes('-topmost', 0)
            self.switch_button.config(bg=SWITCH_OFF, relief="raised")
    
    def on_close(self):
        self.timer.on_close(self.timer.records)
        self.window.destroy()

    def run(self):
        self.update_labels()
        self.window.mainloop()
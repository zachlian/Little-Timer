import tkinter as tk
import time
import csv
import os
import tkinter.font as tkFont

BG_COLOR = "#009688"
FG_COLOR = "#bbe8d0"

class Timer:
    def __init__(self):
        self.timer_start_time = None
        self.timer_records = []
        self.setup_gui()
        
    def setup_gui(self):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=400, height=500, bg=BG_COLOR)
        self.canvas.pack()
        self.window.title("Little Timer")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.task_name = tk.StringVar()
        # Font
        self.font_1 = tkFont.Font(family="Helvetica",size=36,weight="bold")
        self.font_2 = tkFont.Font(family="Helvetica",size=30,weight="bold")
        # Time label
        self.time_label = tk.Label(self.window, font=self.font_1, fg=FG_COLOR, bg=BG_COLOR, width=200, height=100, anchor="center")
        self.time_label.place(x=100,y=40,width=200,height=100)
        # Timer label
        self.timer_label = tk.Label(self.window, font=self.font_2, text="00:00", fg=FG_COLOR, bg=BG_COLOR, width=200, height=80, anchor="center")
        self.timer_label.place(x=100,y=140,width=200,height=80)
        # Start button
        start_button = tk.Button(self.window, text="Start Timer", command=self.start_timer)
        start_button.place(x=100,y=220,width=70,height=25)
        # Stop button
        stop_button = tk.Button(self.window, text="Stop Timer", command=self.stop_timer)
        stop_button.place(x=230,y=220,width=70,height=25)
        # Task entry
        self.task_entry = tk.Entry(self.window, textvariable=self.task_name, justify="center")
        self.task_entry.place(x=100,y=420,width=200,height=30)
        # Listbox
        self.listbox = tk.Listbox(self.window)
        self.listbox.place(x=100,y=250,width=200,height=167)
        
    def update_labels(self):
        # Update the time label
        current_time = time.strftime("%H:%M:%S")
        self.time_label.config(text=current_time)

        if self.timer_start_time:
            elapsed_time = time.time() - self.timer_start_time
            minutes, seconds = divmod(int(elapsed_time), 60)
            self.timer_label.config(text=f"{minutes:02}:{seconds:02}")

        self.window.after(1000, self.update_labels)

    def start_timer(self):
        self.timer_start_time = time.time()
        self.current_task = [time.strftime("%Y-%m-%d %H:%M")]

    def stop_timer(self):
        elapsed_time = time.time() - self.timer_start_time
        minutes, seconds = divmod(int(elapsed_time), 60)
        self.listbox.insert(tk.END, f"{self.task_name.get()}: {minutes} minutes {seconds} seconds")
        task_name = self.task_name.get() if self.task_name.get() else "Task"
        self.current_task.extend([time.strftime("%Y-%m-%d %H:%M"), elapsed_time, task_name])
        self.timer_records.append(self.current_task)
        self.timer_start_time = None
        self.task_entry.delete(0, tk.END)
        self.timer_label.config(text="00:00")

    def on_close(self):
        mode = 'w' if not os.path.isfile('timer_records.csv') else 'a'
        with open('timer_records.csv', mode, newline='') as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(['Start Time', 'End Time', 'Duration', 'Task'])
            for record in self.timer_records:
                hours, remainder = divmod(record[-2], 3600)
                minutes, seconds = divmod(remainder, 60)
                record[-2] = f"{int(hours)} hrs {int(minutes)} mins {int(seconds)} secs"
                writer.writerow(record)
        self.window.destroy()

    def run(self):
        self.update_labels()
        self.window.mainloop()

if __name__ == "__main__":
    app = Timer()
    app.run()
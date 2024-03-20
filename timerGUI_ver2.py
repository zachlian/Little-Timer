from timerGUI import TimerGUI
from constants import *
import csv
import os
import tkinter as tk
import time

class TimerGUIWithCSV(TimerGUI):
    def __init__(self, timer):
        super().__init__(timer) # timer is transferred to TimerGUI

        # Set new layout
        self.task_listbox.place(x=X_OFFSET+20, y=255, width=80)
        self.task_listbox.config(justify='center')
        self.duration_listbox.config(width=80)
        self.duration_listbox.config(justify='center')
        self.topmost_button.place(x=X_OFFSET+67, y=415, width=66, height=25)
        
        # Create a new listbox for the order of the data
        self.order_listbox = tk.Listbox(self.window, justify='center')
        self.order_listbox.place(x=X_OFFSET, y=255, width=20, height=150)

        # Create a scrollbar
        self.scrollbar = tk.Scrollbar(self.window, orient='vertical')
        self.scrollbar.place(x=X_OFFSET+180, y=255, width=20, height=150)

        # Connect the scrollbar to the listboxes
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        self.duration_listbox.config(yscrollcommand=self.scrollbar.set)
        self.order_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.onscroll)

        # Create a delete button
        self.delete_button = tk.Button(self.window, text="Delete", command=self.delete_item)
        self.delete_button.place(x=X_OFFSET+133, y=415, width=67, height=25)

        # Create New button
        self.new_button = tk.Button(self.window, text="New page", command=self.new_item)
        self.new_button.place(x=X_OFFSET, y=415, width=67, height=25)
        
        self.load_csv()
    
    def stop_timer(self): # Overriding the stop_timer method
        task_name = self.task_name.get() if self.task_name.get() else "Task"
        task = self.timer.stop_timer(task_name)
        if task is not None:
            # Insert the new task and its duration into the listboxes
            self.task_listbox.insert(0, task_name)
            self.duration_listbox.insert(0, task[2])
            self.order_listbox.insert(0, "01")

            # Append the task name to the task
            task.append(task_name)
            
            # Update the order indexes of the other tasks
            for i in range(1, self.order_listbox.size()):
                self.order_listbox.delete(i)
                self.order_listbox.insert(i, f"{i+1:02}")
            
            # Clear the task entry and reset the timer label
            self.task_entry.delete(0, tk.END)
            self.timer_label.config(text="00:00:00")
    
    def new_item(self):
        self.order_listbox.delete(0, 'end')
        self.task_listbox.delete(0, 'end')
        self.duration_listbox.delete(0, 'end')
        
        with open('timer_records.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["-", "-", "-", "-"])
        
        self.load_csv()
    
    def onscroll(self, *args):
        self.task_listbox.yview(*args)
        self.duration_listbox.yview(*args)
        self.order_listbox.yview(*args)

    def load_csv(self):
        if os.path.isfile('timer_records.csv'):
            with open('timer_records.csv', 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip the header
                rows = list(reader)
                cnt = 0
                for row in reversed(rows):
                    if all(item == "-" for item in row):
                        break
                    if len(row) >= 4:
                        self.order_listbox.insert(cnt, f"{cnt+1:02}")
                        self.task_listbox.insert(cnt, row[3])
                        self.duration_listbox.insert(cnt, row[2])
                        cnt += 1


    def delete_item(self):
        selected = self.task_listbox.curselection()
        if selected:
            self.order_listbox.delete(selected)
            self.task_listbox.delete(selected)
            self.duration_listbox.delete(selected)
            # Delete the corresponding row from the CSV file
            with open('timer_records.csv', 'r') as f:
                reader = csv.reader(f)
                rows = list(reader)
            del rows[len(rows) - selected[0] - 1]  # Delete the selected row
            with open('timer_records.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(rows)  # Write the remaining rows back to the CSV file
            # Update the order_listbox
            for i in range(len(self.order_listbox.get(0, 'end'))):
                self.order_listbox.delete(i)
                self.order_listbox.insert(i, f"{i+1:02}")
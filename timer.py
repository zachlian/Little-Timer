import time
import csv
import os
from constants import *

class Timer:
    def __init__(self):
        self.start_time = None
        self.records = []
        self.pause_time = None
        self.is_paused = False

    def get_current_time(self):
        return time.strftime("%H:%M:%S")

    def get_elapsed_time(self):
        if self.start_time and not self.is_paused:
            elapsed_time = time.time() - self.start_time
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}"
        return None

    def pause_timer(self):
        if self.start_time is not None:
            if self.is_paused:
                self.start_time += time.time() - self.pause_time
                self.pause_time = None
                self.is_paused = False
            else:
                self.pause_time = time.time()
                self.is_paused = True

    def start_timer(self):
        if self.is_paused:
            self.pause_timer()
        self.start_time = time.time()
        self.current_task = [time.strftime("%Y-%m-%d %H:%M")]

    def stop_timer(self, task_name):
        if self.start_time is None: # Timer not running
            return None
        duration = self.get_elapsed_time()
        self.current_task.extend([time.strftime("%Y-%m-%d %H:%M"), duration, task_name]) # write behind the start time
        self.records.append(self.current_task)
        self.start_time = None
        
        # Write the record to the CSV file
        mode = 'a' if os.path.isfile('timer_records.csv') else 'w'
        with open('timer_records.csv', mode, newline='') as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(['Start Time', 'End Time', 'Duration', 'Task'])
            writer.writerow(self.current_task)
        
        return self.current_task

    def switch(self):
        return not self.is_paused

    def on_close(self, records):
        pass
        

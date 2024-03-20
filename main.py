from timer import Timer
from timerGUI import TimerGUI
from timerGUI_ver2 import TimerGUIWithCSV

if __name__ == "__main__":
    timer = Timer()
    # app = TimerGUI(timer)
    # app.run()
    app = TimerGUIWithCSV(timer)
    app.run()
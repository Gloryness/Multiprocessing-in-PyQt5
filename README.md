# Multiprocessing in PyQt5
 Use this program to test how many threads can run at once while doing the same tasks.
 
# How To Use
This project was pretty fun to make, as you can mess around and see how much QThreadPool can handle in PyQt5.
To start with, there are **10 counters**, and all are idle until you presss Start. Stop will cancel that counter, and Reset will reset the counter back to its original number.

In the **Edit** MenuBar, you can see  a **Config** setting which you can configure the maximum number of threads allowed to happen at once and how much counters you want. There are also **Start All**, **Stop All** and **Reset All** options which will start/stop/reset all counters.

You may be wondering, what are these **'counters'**, well they are organized very neatly and each have their own Start, Stop and Reset option next to them.
They also will show what they will count up to and the current number they're at.
For example: **Process 1 (0-2500)**, **Process 2 (2500-5000)**, **Process 3 (5000-7500)** and etc.

Nothing much is happening inbetween each count, only a small `time.sleep(0.005)`. You can configure this by editting the **multiprocessing.py file** and going to **line 298** to configure what will happen inbetween each task.

Each row will have a different **colour** depending on it's status:
- Active: **Green**
- Inactive: **Black**
- Queued: **Red**

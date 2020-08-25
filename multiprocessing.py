from PyQt5.QtGui import QColor, QPalette, QBrush
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# noinspection PyUnresolvedReferences
from settings import SettingsDialog

import time
import re

step = [i for i in range(2500, 2500*10000, 2500)]

class Button(QPushButton):
    def __init__(self, base, parent=None):
        self.ui = base
        super(Button, self).__init__(parent)

    def mousePressEvent(self, *args, **kwargs):
        try:
            QPushButton.mousePressEvent(self, *args, **kwargs)
        except:
            pass
        search = int(re.search('\d+$', self.objectName())[0])
        if self.objectName().__contains__('Start'):
            arg1 = step[search]-2500
            arg2 = getattr(self.ui, f'counter{search-1}')
            arg3 = getattr(self.ui, f'label{search-1}')
            self.ui.active_threads.append(self.ui.threadpool.activeThreadCount() + 1)
            if self.ui.active_threads[-1] > self.ui.threadpool.maxThreadCount():
                getattr(self.ui, f'counter{search-1}').setPalette(self.ui.red_palette)
            else:
                getattr(self.ui, f'counter{search-1}').setPalette(self.ui.green_palette)
            self.ui.work(arg1, arg2, arg3)

        elif self.objectName().__contains__('Stop'):
            getattr(self.ui, f'counter{search - 1}').setPalette(self.ui.normal_palette)
            arg1 = self.ui
            arg2 = f'stop{step[search-1]}'
            arg3 = True
            setattr(arg1, arg2, arg3)

        elif self.objectName().__contains__('Reset'):
            class1 = getattr(self.ui, f'label{search-1}')
            class1.setText(f"{step[search-1]-2500}")


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress

    '''
    progress = pyqtSignal(int)
    palette = pyqtSignal(str)

class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, upto, label, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.label = label
        self.upto = upto
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        # Retrieve args/kwargs here; and fire processing using them
        self.fn(self.upto, self.signals.palette, self.signals.progress)

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.active_threads = []
        self.counters = []

        self.setupUi()
        self.show()

        self.threadpool = QThreadPool()

    def setupUi(self):
        self.resize(QSize(826, 330))
        self.setWindowTitle("PyQt5: Multithreading Example")
        self.centralwidget = QWidget(self)

        self.gridLayout1 = QGridLayout(self.centralwidget)
        self.gridLayout1.setContentsMargins(0, 0, 0, 0)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidget = QWidget()
        self.scrollAreaWidget.setGeometry(0, 0, 1000, 1000)

        self.gridLayout2 = QFormLayout(self.scrollAreaWidget)
        self.scrollArea.setWidget(self.scrollAreaWidget)

        self.frame = QFrame(self.scrollAreaWidget)

        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(-1, -1, 320, -1)
        self.gridLayout.setSizeConstraint(QLayout.SetFixedSize)

        self.gridLayout2.addWidget(self.frame)

        self.normal_palette = QPalette()
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        self.normal_palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        self.normal_palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        brush = QBrush(QColor(120, 120, 120))
        brush.setStyle(Qt.SolidPattern)
        self.normal_palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)

        self.green_palette = QPalette()
        brush = QBrush(QColor(19, 138, 15))
        brush.setStyle(Qt.SolidPattern)
        self.green_palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush = QBrush(QColor(19, 138, 15))
        brush.setStyle(Qt.SolidPattern)
        self.green_palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        brush = QBrush(QColor(120, 120, 120))
        brush.setStyle(Qt.SolidPattern)
        self.green_palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)

        self.red_palette = QPalette()
        brush = QBrush(QColor(200, 0, 26))
        brush.setStyle(Qt.SolidPattern)
        self.red_palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush = QBrush(QColor(200, 0, 26))
        brush.setStyle(Qt.SolidPattern)
        self.red_palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        brush = QBrush(QColor(120, 120, 120))
        brush.setStyle(Qt.SolidPattern)
        self.red_palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)

        self.setCounters(10)

        self.gridLayout1.addWidget(self.scrollArea)

        self.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 491, 21))

        self.editMenu = QMenu(self.menubar)
        self.editMenu.setTitle("Edit")

        self.config = QAction(self)
        self.config.setText("Configure")
        self.config.triggered.connect(lambda: SettingsDialog(self))

        self.startAll = QAction(self)
        self.startAll.setText("Start All")
        self.startAll.triggered.connect(self.startAllCounters)
        self.startAll.setShortcut("Ctrl+S")

        self.stopAll = QAction(self)
        self.stopAll.setText("Stop All")
        self.stopAll.triggered.connect(self.stopAllCounters)
        self.stopAll.setShortcut("Ctrl+T")

        self.resetAll = QAction(self)
        self.resetAll.setText("Reset All")
        self.resetAll.triggered.connect(self.resetAllCounters)
        self.resetAll.setShortcut("Ctrl+R")

        self.setMenuBar(self.menubar)

        self.editMenu.addAction(self.config)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.startAll)
        self.editMenu.addAction(self.stopAll)
        self.editMenu.addAction(self.resetAll)


        self.menubar.addAction(self.editMenu.menuAction())

        self.statusbar = QStatusBar(self)

        self.setStatusBar(self.statusbar)
        QMetaObject.connectSlotsByName(self)

    def setCounters(self, amount: int):
        new = self.counters.copy()
        for i in self.counters:
            new.remove(i)
            getCounter = getattr(self, f'counter{i}')
            getLabel = getattr(self, f'label{i}')
            getStart = getattr(self, f'start{i}')
            getStop = getattr(self, f'stopButton{i}')
            getReset = getattr(self, f'reset{i}')
            self.gridLayout.removeWidget(getCounter)
            self.gridLayout.removeWidget(getLabel)
            self.gridLayout.removeWidget(getStart)
            self.gridLayout.removeWidget(getStop)
            self.gridLayout.removeWidget(getReset)
            getCounter.deleteLater()
            getLabel.deleteLater()
            getStart.deleteLater()
            getStop.deleteLater()
            getReset.deleteLater()
            delattr(self, f'counter{i}')
            delattr(self, f'label{i}')
            delattr(self, f'start{i}')
            delattr(self, f'stopButton{i}')
            delattr(self, f'reset{i}')
        self.counters = new


        for i in range(amount):
            self.counters.append(i)
            setattr(self, f'counter{i}', QLabel(self.centralwidget))
            setattr(self, f'label{i}', QLabel(self.centralwidget))
            setattr(self, f'start{i}', Button(self, self.centralwidget))
            setattr(self, f'stopButton{i}', Button(self, self.centralwidget))
            setattr(self, f'reset{i}', Button(self, self.centralwidget))
            setattr(self, f'stop{step[i]}', False)
            getCounter = getattr(self, f'counter{i}')
            getLabel = getattr(self, f'label{i}')
            getStart = getattr(self, f'start{i}')
            getStop = getattr(self, f'stopButton{i}')
            getReset = getattr(self, f'reset{i}')

            self.gridLayout.addWidget(getCounter, i, 0, 1, 1)
            self.gridLayout.addWidget(getLabel, i, 1, 1, 1)
            self.gridLayout.addWidget(getStart, i, 2, 1, 1)
            self.gridLayout.addWidget(getStop, i, 3, 1, 1)
            self.gridLayout.addWidget(getReset, i, 4, 1, 1)

            getCounter.setText(f"Process {i + 1} ({step[i] - 2500}-{step[i]})")
            getLabel.setText(f"{step[i] - 2500}")
            getStart.setText("Start")
            getStop.setText("Stop")
            getReset.setText("Reset")

            getStart.setObjectName(f"Start {i + 1}")
            getStop.setObjectName(f"Stop {i + 1}")
            getReset.setObjectName(f"Reset {i + 1}")

            ## Connecting the buttons through .connect() will not work as it will always use the last one on the list so therefore
            ## we create a Button class and use a mousePressEvent() method and get the object name to see what type it is and where.

    def startAllCounters(self):
        for i in self.counters:
            getStart = getattr(self, f'start{i}')
            getStart.mousePressEvent(QPushButton.mousePressEvent)

    def stopAllCounters(self):
        for i in self.counters:
            getStop = getattr(self, f'stopButton{i}')
            getStop.mousePressEvent(QPushButton.mousePressEvent)

    def resetAllCounters(self):
        for i in self.counters:
            getReset = getattr(self, f'reset{i}')
            getReset.mousePressEvent(QPushButton.mousePressEvent)

    def task(self, upto, palette, counter):
        to_start = upto-2500
        upto = upto+1
        for i in range(to_start, upto):
            palette.emit("green_palette")
            if getattr(self, f'stop{upto-1}'):
                break
            ## write code
            ## here
            time.sleep(0.005)
            try:
                counter.emit(i)
            except AttributeError:
                break
        palette.emit("normal_palette")
        setattr(self, f'stop{upto-1}', False)

    def updateCounter(self, text, label):
        label.setText(str(text))

    def updatePalette(self, name, label):
        label.setPalette(getattr(self, name))

    def work(self, upto, counterlabel, label):
        setattr(self, f'stop{upto}', False)
        # Pass the function to execute
        worker = Worker(self.task, upto, label)
        worker.signals.progress.connect(lambda x: self.updateCounter(x, label))
        worker.signals.palette.connect(lambda x: self.updatePalette(x, counterlabel))

        # Execute
        self.threadpool.start(worker)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = MainWindow()
    sys.exit(app.exec_())

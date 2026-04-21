import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
import subprocess

class MouseWiggleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.process = None

    def initUI(self):
        layout = QVBoxLayout()

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_process)
        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stop_process)

        self.output_label = QLabel('Output will be displayed here', self)

        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.output_label)

        self.setLayout(layout)
        self.setWindowTitle('Mouse Wiggle GUI')
        self.show()

    def start_process(self):
        if self.process is None:
            self.process = subprocess.Popen(['python', 'mouse-wiggle/move_cursor.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.update_output()

    def stop_process(self):
        if self.process:
            self.process.terminate()
            self.process = None

    def update_output(self):
        if self.process:
            output = self.process.stdout.readline()
            while output:
                self.output_label.setText(output.decode('utf-8').strip())
                output = self.process.stdout.readline()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MouseWiggleApp()
    sys.exit(app.exec_())
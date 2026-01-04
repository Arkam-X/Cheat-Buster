from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer
from process_tracker import get_visible_apps

class Overlay(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interview Transparency Monitor")
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                background-color: rgba(0, 0, 0, 180);
                padding: 10px;
                border-radius: 8px;
            }
        """)

        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.update_apps()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_apps)
        self.timer.start(3000)  # refresh every 3 sec

    def update_apps(self):
        apps = get_visible_apps()
        text = "Active Applications\n-------------------\n"
        text += "\n".join(apps)
        self.label.setText(text)

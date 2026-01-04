from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer, QPoint
from process_tracker import get_visible_apps

class Overlay(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cheat Buster Monitor")
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.drag_position = QPoint()
        self.is_minimized = False

        # 🔹 Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # 🔹 Header (for drag + buttons)
        self.header = QWidget()
        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(8, 4, 8, 4)

        self.title_label = QLabel("Cheat Buster Monitor")
        self.title_label.setStyleSheet("color: white; font-weight: bold;")

        self.minimize_btn = QPushButton("–")
        self.minimize_btn.setFixedSize(20, 20)
        self.minimize_btn.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        self.minimize_btn.clicked.connect(self.toggle_minimize)

        self.header_layout.addWidget(self.title_label)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.minimize_btn)
        self.header.setLayout(self.header_layout)

        self.header.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 200);
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
        """)

        # 🔹 Content label
        self.content = QLabel()
        self.content.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                background-color: rgba(0, 0, 0, 180);
                padding: 12px;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
            }
        """)

        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self.content)
        self.setLayout(self.main_layout)

        # 🔁 Refresh timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_overlay)
        self.timer.start(3000)

        self.update_overlay()

    # 🔄 Update displayed data
    def update_overlay(self):
        os_apps = get_visible_apps()

        text = "Active Applications\n"
        text += "-------------------\n"
        text += "\n".join(os_apps) if os_apps else "No active apps"
        text += "\n\n"

        text += "Active Websites\n"
        text += "---------------\n"
        text += "Chrome:\n • (waiting for browser data…)"

        self.content.setText(text)

    # ➖ Minimize / Expand
    def toggle_minimize(self):
        self.is_minimized = not self.is_minimized

        if self.is_minimized:
            self.content.hide()
            self.minimize_btn.setText("+")
            self.adjustSize() 
        else:
            self.content.show()
            self.minimize_btn.setText("–")
            self.adjustSize() 

    # 🖱️ Dragging logic
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self.drag_position
            self.move(self.pos() + delta)
            self.drag_position = event.globalPosition().toPoint()
            event.accept()
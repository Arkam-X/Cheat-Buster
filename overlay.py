# from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
# from PyQt6.QtCore import Qt, QTimer
# from process_tracker import get_visible_apps

# class Overlay(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("Interview Transparency Monitor")
#         self.setWindowFlags(
#             Qt.WindowType.WindowStaysOnTopHint |
#             Qt.WindowType.FramelessWindowHint
#         )
#         self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

#         self.layout = QVBoxLayout()
#         self.label = QLabel()
#         self.label.setStyleSheet("""
#             QLabel {
#                 color: white;
#                 font-size: 14px;
#                 background-color: rgba(0, 0, 0, 180);
#                 padding: 10px;
#                 border-radius: 8px;
#             }
#         """)

#         self.layout.addWidget(self.label)
#         self.setLayout(self.layout)

#         self.update_apps()

#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_apps)
#         self.timer.start(3000)  # refresh every 3 sec

#     def update_apps(self):
#         apps = get_visible_apps()
#         text = "Active Applications\n-------------------\n"
#         text += "\n".join(apps)
#         self.label.setText(text)

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
                padding: 12px;
                border-radius: 8px;
            }
        """)

        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_overlay)
        self.timer.start(3000)

        self.update_overlay()

    def update_overlay(self):
        os_apps = get_visible_apps()

        # 🔹 Placeholder browser data (will come from extension later)
        browser_data = {
            "Chrome": []  # Empty for now
        }

        text = "Active Applications\n"
        text += "-------------------\n"
        text += "\n".join(os_apps) if os_apps else "No active apps"
        text += "\n\n"

        text += "Active Websites\n"
        text += "---------------\n"

        for browser, tabs in browser_data.items():
            text += f"{browser}:\n"
            if tabs:
                for tab in tabs:
                    text += f" • {tab}\n"
            else:
                text += " • (waiting for browser data…)\n"

        self.label.setText(text)

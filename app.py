import sys
import threading
from PyQt6.QtWidgets import QApplication
from overlay import Overlay
from ws_server import start_ws_server

if __name__ == "__main__":
    # 🔌 Start WebSocket server in background
    ws_thread = threading.Thread(target=start_ws_server, daemon=True)
    ws_thread.start()

    app = QApplication(sys.argv)
    overlay = Overlay()
    overlay.show()
    sys.exit(app.exec())

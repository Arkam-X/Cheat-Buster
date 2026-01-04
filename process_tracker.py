import win32gui
import win32process
import psutil

SYSTEM_TITLES = {
    "",
    "Program Manager"
}

def get_visible_apps():
    apps = set()

    def enum_handler(hwnd, _):
        if not win32gui.IsWindowVisible(hwnd):
            return

        title = win32gui.GetWindowText(hwnd)
        if title in SYSTEM_TITLES:
            return

        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            apps.add(process.name().replace(".exe", ""))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    win32gui.EnumWindows(enum_handler, None)
    return sorted(apps)

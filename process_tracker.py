# import win32gui
# import win32process
# import psutil

# SYSTEM_TITLES = {
#     "",
#     "Program Manager"
# }

# def get_visible_apps():
#     apps = set()

#     def enum_handler(hwnd, _):
#         if not win32gui.IsWindowVisible(hwnd):
#             return

#         title = win32gui.GetWindowText(hwnd)
#         if title in SYSTEM_TITLES:
#             return

#         try:
#             _, pid = win32process.GetWindowThreadProcessId(hwnd)
#             process = psutil.Process(pid)
#             apps.add(process.name().replace(".exe", ""))
#         except (psutil.NoSuchProcess, psutil.AccessDenied):
#             pass

#     win32gui.EnumWindows(enum_handler, None)
#     return sorted(apps)

import win32gui
import win32process
import psutil

IGNORED_APPS = {
    "ApplicationFrameHost",
    "TextInputHost",
    "SystemSettings",
    "SearchApp",
    "ShellExperienceHost",
    "StartMenuExperienceHost",
    "python",
    "Nahimic3",
}

SYSTEM_TITLES = {
    "",
    "Program Manager"
}

def normalize_app_name(name: str) -> str:
    mapping = {
        "chrome": "Google Chrome",
        "msedge": "Microsoft Edge",
        "code": "Visual Studio Code",
        "whatsapp.root": "WhatsApp"
    }
    return mapping.get(name.lower(), name)

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
            name = process.name().replace(".exe", "")

            if name in IGNORED_APPS:
                return

            apps.add(normalize_app_name(name))

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    win32gui.EnumWindows(enum_handler, None)
    return sorted(apps)


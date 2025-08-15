"""
Entry point for the Personalized Virtual Desktop Environment.
"""


import sys
sys.excepthook = lambda t, v, tb: print(f"Exception: {t.__name__}: {v}")

from PyQt5.QtWidgets import QApplication, QShortcut
from PyQt5.QtGui import QKeySequence
from login import LoginWindow
import socket

try:
    from backend import log
    log("App started")
except Exception:
    pass

import sys
import os
# تم حذف كود فتح الكونسول حتى لا تظهر نافذة CMD عند تشغيل التطبيق

def main():
    # تسجيل اسم الحاسبة في قاعدة البيانات عند أول تشغيل
    try:
        from supabase_client import supabase
        computer_name = socket.gethostname()
        # تحقق إذا كان الحاسبة مسجلة مسبقاً
        resp = supabase.table("computers").select("computer_name").eq("computer_name", computer_name).execute()
        exists = resp.data if resp and hasattr(resp, 'data') else []
        if not exists:
            supabase.table("computers").insert({"computer_name": computer_name}).execute()
    except Exception as e:
        print(f"Error registering computer name: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginWindow()
    # Accessibility: set accessible name and description
    login.setAccessibleName("Login Window")
    login.setAccessibleDescription("Main login screen for user authentication")

    # Keyboard shortcut: Ctrl+Q to quit
    quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), login)
    quit_shortcut.activated.connect(app.quit)

    login.showFullScreen()
    main()
    sys.exit(app.exec_())

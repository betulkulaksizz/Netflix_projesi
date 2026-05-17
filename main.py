import sys
from PyQt6.QtWidgets import QApplication
from ui.login_page import LoginPage


def on_login_success(user):
    """Giriş başarılı olduğunda role göre yönlendir."""
    if user["rol_id"] == 2:
        from ui.admin_panel import AdminPanel
        window = AdminPanel(user)
    else:
        from ui.home_page import HomePage
        window = HomePage(user)
    window.show()
    app._login_window.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    login = LoginPage(on_login_success=on_login_success)
    app._login_window = login
    login.show()
    sys.exit(app.exec())

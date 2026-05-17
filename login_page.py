from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from auth import login_user, validate_email


class LoginPage(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.setWindowTitle("Netflix Platform - Giriş")
        self.setFixedSize(460, 520)
        self.setStyleSheet("background-color: #141414;")
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.setSpacing(0)
        root.setContentsMargins(0, 0, 0, 0)

        # ── Başlık ──────────────────────────────────────────
        title = QLabel("N")
        title.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        title.setStyleSheet("color: #E50914; letter-spacing: 2px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(title)

        subtitle = QLabel("İçerik Platformu")
        subtitle.setFont(QFont("Arial", 13))
        subtitle.setStyleSheet("color: #aaaaaa; margin-bottom: 30px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(subtitle)

        # ── Form kartı ──────────────────────────────────────
        card = QFrame()
        card.setFixedWidth(380)
        card.setStyleSheet("""
            QFrame {
                background-color: #1f1f1f;
                border-radius: 12px;
                padding: 10px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(14)
        card_layout.setContentsMargins(30, 30, 30, 30)

        # E-mail
        self.email_input = self._make_input("E-mail", False)
        card_layout.addWidget(QLabel("E-mail", styleSheet="color:#ccc; font-size:13px;"))
        card_layout.addWidget(self.email_input)

        # Şifre
        self.pass_input = self._make_input("Şifre", True)
        card_layout.addWidget(QLabel("Şifre", styleSheet="color:#ccc; font-size:13px;"))
        card_layout.addWidget(self.pass_input)

        # Hata mesajı
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #ff4444; font-size: 12px;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setWordWrap(True)
        card_layout.addWidget(self.error_label)

        # Giriş Yap butonu
        btn_login = QPushButton("Giriş Yap")
        btn_login.setFixedHeight(44)
        btn_login.setStyleSheet("""
            QPushButton {
                background-color: #E50914;
                color: white;
                border-radius: 6px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #f40612; }
            QPushButton:pressed { background-color: #b2070f; }
        """)
        btn_login.clicked.connect(self._handle_login)
        card_layout.addWidget(btn_login)

        # Kayıt Ol butonu
        btn_register = QPushButton("Hesabın yok mu? Kayıt Ol")
        btn_register.setFixedHeight(38)
        btn_register.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #aaaaaa;
                border: 1px solid #444;
                border-radius: 6px;
                font-size: 13px;
            }
            QPushButton:hover { color: white; border-color: #888; }
        """)
        btn_register.clicked.connect(self._open_register)
        card_layout.addWidget(btn_register)

        root.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)

        # Enter tuşu bağlantısı
        self.pass_input.returnPressed.connect(self._handle_login)

    def _make_input(self, placeholder: str, is_password: bool) -> QLineEdit:
        inp = QLineEdit()
        inp.setPlaceholderText(placeholder)
        inp.setFixedHeight(40)
        if is_password:
            inp.setEchoMode(QLineEdit.EchoMode.Password)
        inp.setStyleSheet("""
            QLineEdit {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 0 12px;
                font-size: 14px;
            }
            QLineEdit:focus { border: 1px solid #E50914; }
        """)
        return inp

    def _set_error(self, msg: str):
        self.error_label.setText(msg)

    def _handle_login(self):
        email    = self.email_input.text().strip()
        password = self.pass_input.text()

        # Boş alan kontrolü
        if not email or not password:
            self._set_error("E-mail ve şifre alanları boş bırakılamaz.")
            return

        # E-mail format kontrolü
        if not validate_email(email):
            self._set_error("Geçerli bir e-mail adresi giriniz.")
            return

        self._set_error("")

        # Kimlik doğrulama
        user, err = login_user(email, password)
        if err:
            self._set_error(err)
            return

        # Role göre yönlendirme
        self.on_login_success(user)

    def _open_register(self):
        from ui.register_page import RegisterPage
        self.register_window = RegisterPage(on_back=self._show_self)
        self.register_window.show()
        self.hide()

    def _show_self(self):
        self.email_input.clear()
        self.pass_input.clear()
        self._set_error("")
        self.show()

from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QComboBox,
    QVBoxLayout, QHBoxLayout, QFrame, QScrollArea,
    QCheckBox, QDateEdit, QMessageBox, QGridLayout
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from auth import (
    register_user, get_all_genres, validate_email,
    validate_country, validate_name, get_recommendations_by_genres
)
from datetime import date


STYLE_INPUT = """
    QLineEdit, QComboBox, QDateEdit {
        background-color: #2b2b2b;
        color: white;
        border: 1px solid #444;
        border-radius: 6px;
        padding: 0 12px;
        font-size: 13px;
        min-height: 36px;
    }
    QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
        border: 1px solid #E50914;
    }
    QComboBox QAbstractItemView {
        background-color: #2b2b2b;
        color: white;
        selection-background-color: #E50914;
    }
    QComboBox::drop-down { border: none; }
    QComboBox::down-arrow { image: none; width: 0; }
    QDateEdit::up-button, QDateEdit::down-button { width: 0; }
"""

STYLE_LABEL = "color: #cccccc; font-size: 12px; margin-bottom: 2px;"

STYLE_ERROR = "color: #ff4444; font-size: 12px;"

STYLE_BTN_PRIMARY = """
    QPushButton {
        background-color: #E50914;
        color: white;
        border-radius: 6px;
        font-size: 14px;
        font-weight: bold;
        min-height: 42px;
    }
    QPushButton:hover  { background-color: #f40612; }
    QPushButton:pressed{ background-color: #b2070f; }
"""

STYLE_BTN_SECONDARY = """
    QPushButton {
        background-color: transparent;
        color: #aaaaaa;
        border: 1px solid #444;
        border-radius: 6px;
        font-size: 13px;
        min-height: 36px;
    }
    QPushButton:hover { color: white; border-color: #888; }
"""


class RegisterPage(QWidget):
    def __init__(self, on_back):
        super().__init__()
        self.on_back = on_back
        self.genre_checkboxes = {}   # tur_id -> QCheckBox
        self.setWindowTitle("Netflix Platform - Kayıt Ol")
        self.setFixedSize(520, 700)
        self.setStyleSheet("background-color: #141414;")
        self._build_ui()
        self._load_genres()

    # ──────────────────────────────────────────────────────────
    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Başlık
        title = QLabel("Kayıt Ol")
        title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: white; margin: 20px 0 4px 0;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(title)

        # Scroll alanı
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }"
                             "QScrollBar:vertical { background:#1a1a1a; width:8px; border-radius:4px; }"
                             "QScrollBar::handle:vertical { background:#444; border-radius:4px; }"
                             "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height:0; }")

        container = QWidget()
        container.setStyleSheet("background-color: transparent;")
        form = QVBoxLayout(container)
        form.setContentsMargins(60, 10, 60, 20)
        form.setSpacing(8)

        # Ad / Soyad (yan yana)
        row_ad = QHBoxLayout()
        ad_col = QVBoxLayout()
        ad_col.addWidget(QLabel("Ad *", styleSheet=STYLE_LABEL))
        self.inp_ad = self._input("Adınız")
        ad_col.addWidget(self.inp_ad)

        soyad_col = QVBoxLayout()
        soyad_col.addWidget(QLabel("Soyad *", styleSheet=STYLE_LABEL))
        self.inp_soyad = self._input("Soyadınız")
        soyad_col.addWidget(self.inp_soyad)

        row_ad.addLayout(ad_col)
        row_ad.addSpacing(10)
        row_ad.addLayout(soyad_col)
        form.addLayout(row_ad)

        # E-mail
        form.addWidget(QLabel("E-mail *", styleSheet=STYLE_LABEL))
        self.inp_email = self._input("E-mail adresiniz")
        form.addWidget(self.inp_email)

        # Şifre / Şifre tekrar (yan yana)
        row_sifre = QHBoxLayout()
        s1 = QVBoxLayout()
        s1.addWidget(QLabel("Şifre *", styleSheet=STYLE_LABEL))
        self.inp_sifre = self._input("En az 6 karakter", password=True)
        s1.addWidget(self.inp_sifre)

        s2 = QVBoxLayout()
        s2.addWidget(QLabel("Şifre Tekrar *", styleSheet=STYLE_LABEL))
        self.inp_sifre2 = self._input("Şifreyi tekrar girin", password=True)
        s2.addWidget(self.inp_sifre2)

        row_sifre.addLayout(s1)
        row_sifre.addSpacing(10)
        row_sifre.addLayout(s2)
        form.addLayout(row_sifre)

        # Doğum tarihi
        form.addWidget(QLabel("Doğum Tarihi *", styleSheet=STYLE_LABEL))
        self.inp_dogum = QDateEdit()
        self.inp_dogum.setCalendarPopup(True)
        self.inp_dogum.setDate(QDate(2000, 1, 1))
        self.inp_dogum.setMaximumDate(QDate.currentDate())
        self.inp_dogum.setDisplayFormat("dd/MM/yyyy")
        self.inp_dogum.setStyleSheet(STYLE_INPUT)
        form.addWidget(self.inp_dogum)

        # Cinsiyet / Ülke (yan yana)
        row_cu = QHBoxLayout()
        cins_col = QVBoxLayout()
        cins_col.addWidget(QLabel("Cinsiyet *", styleSheet=STYLE_LABEL))
        self.cmb_cinsiyet = QComboBox()
        self.cmb_cinsiyet.addItems(["Seçiniz", "Erkek", "Kadın", "Diğer"])
        self.cmb_cinsiyet.setStyleSheet(STYLE_INPUT)
        cins_col.addWidget(self.cmb_cinsiyet)

        ulke_col = QVBoxLayout()
        ulke_col.addWidget(QLabel("Ülke *", styleSheet=STYLE_LABEL))
        self.inp_ulke = self._input("Ülkeniz")
        ulke_col.addWidget(self.inp_ulke)

        row_cu.addLayout(cins_col)
        row_cu.addSpacing(10)
        row_cu.addLayout(ulke_col)
        form.addLayout(row_cu)

        # Favori Türler
        form.addSpacing(4)
        tur_lbl = QLabel("Favori Türler * (tam 3 tür seçin)", styleSheet=STYLE_LABEL)
        form.addWidget(tur_lbl)

        self.genre_frame = QFrame()
        self.genre_frame.setStyleSheet(
            "QFrame { background:#1e1e1e; border:1px solid #333; border-radius:8px; padding:6px; }")
        self.genre_grid = QGridLayout(self.genre_frame)
        self.genre_grid.setSpacing(6)
        form.addWidget(self.genre_frame)

        # Hata etiketi
        self.lbl_error = QLabel("")
        self.lbl_error.setStyleSheet(STYLE_ERROR)
        self.lbl_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_error.setWordWrap(True)
        form.addWidget(self.lbl_error)

        # Kayıt Ol butonu
        btn_kayit = QPushButton("Kayıt Ol")
        btn_kayit.setStyleSheet(STYLE_BTN_PRIMARY)
        btn_kayit.clicked.connect(self._handle_register)
        form.addWidget(btn_kayit)

        # Geri dön
        btn_back = QPushButton("← Giriş sayfasına dön")
        btn_back.setStyleSheet(STYLE_BTN_SECONDARY)
        btn_back.clicked.connect(self._go_back)
        form.addWidget(btn_back)

        scroll.setWidget(container)
        outer.addWidget(scroll)

    # ──────────────────────────────────────────────────────────
    def _input(self, placeholder, password=False) -> QLineEdit:
        w = QLineEdit()
        w.setPlaceholderText(placeholder)
        w.setStyleSheet(STYLE_INPUT)
        if password:
            w.setEchoMode(QLineEdit.EchoMode.Password)
        return w

    def _load_genres(self):
        genres = get_all_genres()
        cols = 2
        for i, g in enumerate(genres):
            cb = QCheckBox(g["tur_adi"])
            cb.setStyleSheet("""
                QCheckBox { color: #cccccc; font-size: 13px; }
                QCheckBox::indicator { width:16px; height:16px; border-radius:3px;
                                       border:1px solid #555; background:#2b2b2b; }
                QCheckBox::indicator:checked { background:#E50914; border-color:#E50914; }
            """)
            cb.stateChanged.connect(self._enforce_max_three)
            self.genre_checkboxes[g["tur_id"]] = cb
            self.genre_grid.addWidget(cb, i // cols, i % cols)

    def _enforce_max_three(self):
        selected = [cb for cb in self.genre_checkboxes.values() if cb.isChecked()]
        if len(selected) > 3:
            # Son işaretleneni bul ve geri al
            self.sender().setChecked(False)

    def _selected_genre_ids(self):
        return [tid for tid, cb in self.genre_checkboxes.items() if cb.isChecked()]

    def _set_error(self, msg):
        self.lbl_error.setText(msg)

    # ──────────────────────────────────────────────────────────
    def _handle_register(self):
        ad      = self.inp_ad.text().strip()
        soyad   = self.inp_soyad.text().strip()
        email   = self.inp_email.text().strip()
        sifre   = self.inp_sifre.text()
        sifre2  = self.inp_sifre2.text()
        cinsiyet = self.cmb_cinsiyet.currentText()
        ulke    = self.inp_ulke.text().strip()
        qdate   = self.inp_dogum.date()
        dogum   = date(qdate.year(), qdate.month(), qdate.day())
        tur_ids = self._selected_genre_ids()

        # Boş alan
        if not all([ad, soyad, email, sifre, sifre2, ulke]):
            self._set_error("Tüm alanlar doldurulmalıdır.")
            return

        # Ad doğrulama
        if not validate_name(ad):
            self._set_error("Ad sadece harfler, boşluklar ve kesme işareti içermelidir.")
            return

        # Soyad doğrulama
        if not validate_name(soyad):
            self._set_error("Soyad sadece harfler, boşluklar ve kesme işareti içermelidir.")
            return

        # Cinsiyet seçimi
        if cinsiyet == "Seçiniz":
            self._set_error("Lütfen cinsiyet seçiniz.")
            return

        # E-mail format
        if not validate_email(email):
            self._set_error("Geçerli bir e-mail adresi giriniz.")
            return

        # Ülke format
        if not validate_country(ulke):
            self._set_error("Geçerli bir ülke adı giriniz.")
            return

        # Şifre uzunluğu
        if len(sifre) < 6:
            self._set_error("Şifre en az 6 karakter olmalıdır.")
            return

        # Şifre eşleşme
        if sifre != sifre2:
            self._set_error("Şifreler eşleşmiyor.")
            return

        # Doğum tarihi
        if dogum > date.today():
            self._set_error("Doğum tarihi bugünden ileri olamaz.")
            return

        # Tür sayısı
        if len(tur_ids) != 3:
            self._set_error("Lütfen tam olarak 3 favori tür seçiniz.")
            return

        self._set_error("")

        success, err = register_user(ad, soyad, email, sifre, dogum, cinsiyet, ulke, tur_ids)
        if not success:
            self._set_error(err)
            return

        # Kayıt başarılı → öneri sayfasına yönlendir
        recommendations = get_recommendations_by_genres(tur_ids)
        from ui.recommendation_page import RecommendationPage
        self.rec_window = RecommendationPage(
            user_name=ad,
            recommendations=recommendations,
            on_continue=self._go_back
        )
        self.rec_window.show()
        self.hide()

    def _go_back(self):
        self.close()
        self.on_back()

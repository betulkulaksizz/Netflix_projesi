from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QLineEdit, QDateEdit,
    QVBoxLayout, QHBoxLayout, QFrame, QScrollArea, QComboBox,
    QCheckBox, QGridLayout, QMessageBox, QTabWidget
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from queries import get_profil, update_profil, update_sifre, update_favori_turler
from auth import get_all_genres, validate_email, validate_country, validate_name
from datetime import date

BG     = "#141414"
BG2    = "#1e1e1e"
BG3    = "#2b2b2b"
RED    = "#E50914"
TEXT   = "#ffffff"
MUTED  = "#aaaaaa"
GOLD   = "#ffd54f"
GREEN  = "#a5d6a7"
BORDER = "#333333"

STYLE_INPUT = f"""
    QLineEdit, QDateEdit {{
        background:{BG3}; color:white; border:1px solid {BORDER};
        border-radius:6px; padding:0 12px; font-size:13px; min-height:36px;
    }}
    QLineEdit:focus, QDateEdit:focus {{ border-color:{RED}; }}
    QDateEdit::up-button, QDateEdit::down-button {{ width:0; }}
"""
STYLE_BTN_RED = f"""
    QPushButton {{
        background:{RED}; color:white; border-radius:6px;
        font-size:13px; font-weight:bold; min-height:40px; padding:0 24px;
    }}
    QPushButton:hover  {{ background:#f40612; }}
    QPushButton:pressed{{ background:#b2070f; }}
"""
STYLE_BTN_GRAY = f"""
    QPushButton {{
        background:{BG3}; color:{TEXT}; border:1px solid {BORDER};
        border-radius:6px; font-size:13px; min-height:40px; padding:0 24px;
    }}
    QPushButton:hover {{ border-color:#666; }}
"""
STYLE_ERROR   = "color:#ff4444; font-size:12px;"
STYLE_SUCCESS = f"color:{GREEN}; font-size:12px;"


def _lbl(text, size=13, bold=False, color=TEXT) -> QLabel:
    l = QLabel(text)
    l.setStyleSheet(f"color:{color}; font-size:{size}px;")
    if bold:
        l.setFont(QFont("Arial", size, QFont.Weight.Bold))
    return l


def _divider():
    f = QFrame()
    f.setFrameShape(QFrame.Shape.HLine)
    f.setStyleSheet(f"background:{BORDER}; max-height:1px;")
    return f


class ProfilePage(QWidget):
    def __init__(self, user: dict, on_user_update=None):
        super().__init__()
        self.user = user
        self.on_user_update = on_user_update   # ad/soyad değişince topbar'ı güncelle
        self.genre_checkboxes = {}             # tur_id -> QCheckBox

        self.setWindowTitle("Profil")
        self.setFixedSize(580, 720)
        self.setStyleSheet(f"background:{BG}; color:{TEXT};")
        self._load_and_build()

    # ═══════════════════════════════════════════════════════════
    def _load_and_build(self):
        self.profil = get_profil(self.user["kullanici_id"])
        old = self.layout()
        if old:
            while old.count():
                w = old.takeAt(0)
                if w.widget():
                    w.widget().deleteLater()
            QWidget().setLayout(old)
        self._build_ui()

    # ═══════════════════════════════════════════════════════════
    def _build_ui(self):
        p = self.profil
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Başlık ──────────────────────────────────────────
        header = QFrame()
        header.setStyleSheet(f"background:{BG2}; border-bottom:1px solid {BORDER};")
        header.setFixedHeight(64)
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(24, 0, 24, 0)
        avatar = QLabel("👤")
        avatar.setFont(QFont("Arial", 28))
        h_layout.addWidget(avatar)
        title_col = QVBoxLayout()
        name_lbl = _lbl(f"{p['ad']} {p['soyad']}", size=16, bold=True)
        title_col.addWidget(name_lbl)
        title_col.addWidget(_lbl(p["email"], color=MUTED, size=12))
        h_layout.addLayout(title_col)
        h_layout.addStretch()
        root.addWidget(header)

        # ── Tab widget ──────────────────────────────────────
        tabs = QTabWidget()
        tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border:none; background:{BG};
            }}
            QTabBar::tab {{
                background:{BG2}; color:{MUTED}; padding:10px 20px;
                border:none; font-size:13px;
            }}
            QTabBar::tab:selected {{
                color:white; border-bottom:2px solid {RED};
            }}
            QTabBar::tab:hover {{ color:white; }}
        """)

        tabs.addTab(self._tab_istatistik(), "📊  İstatistikler")
        tabs.addTab(self._tab_bilgiler(),   "✏️  Bilgileri Düzenle")
        tabs.addTab(self._tab_sifre(),      "🔒  Şifre Değiştir")
        tabs.addTab(self._tab_turler(),     "🎬  Favori Türler")

        root.addWidget(tabs)

    # ═══════════════════════════════════════════════════════════
    # TAB 1 — İstatistikler
    # ═══════════════════════════════════════════════════════════
    def _tab_istatistik(self) -> QWidget:
        p = self.profil
        w = QWidget()
        w.setStyleSheet(f"background:{BG};")
        layout = QVBoxLayout(w)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(14)

        # Stat kartları
        stats = [
            ("⏱", "Toplam İzleme Süresi",
             f"{int(p['toplam_sure_dk'] or 0)} dakika  "
             f"({int((p['toplam_sure_dk'] or 0) // 60)} saat)"),
            ("🎬", "İzlenen İçerik Sayısı",
             str(int(p["izlenen_icerik"] or 0))),
            ("⭐", "Verilen Ortalama Puan",
             f"{float(p['ortalama_puan']):.1f} / 10"
             if p["ortalama_puan"] else "Henüz puan verilmedi"),
            ("📅", "Kayıt Tarihi",
             str(p["kayit_tarihi"])[:10] if p["kayit_tarihi"] else "—"),
            ("🌍", "Ülke", p["ulke"] or "—"),
            ("🎂", "Doğum Tarihi", str(p["dogum_tarihi"]) if p["dogum_tarihi"] else "—"),
        ]

        for icon, key, val in stats:
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background:{BG2}; border-radius:8px;
                    border:1px solid {BORDER};
                }}
            """)
            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(16, 12, 16, 12)
            icon_lbl = QLabel(icon)
            icon_lbl.setFont(QFont("Arial", 20))
            icon_lbl.setFixedWidth(36)
            card_layout.addWidget(icon_lbl)
            col = QVBoxLayout()
            col.addWidget(_lbl(key, size=11, color=MUTED))
            col.addWidget(_lbl(val, size=14, bold=True))
            card_layout.addLayout(col)
            card_layout.addStretch()
            layout.addWidget(card)

        # Favori türler rozeti
        if p.get("favori_turler"):
            layout.addWidget(_divider())
            layout.addWidget(_lbl("Favori Türler", size=13, bold=True))
            badge_row = QHBoxLayout()
            badge_row.setSpacing(8)
            for t in p["favori_turler"]:
                badge = QLabel(f"  {t['tur_adi']}  ")
                badge.setStyleSheet(f"""
                    background:{RED}; color:white; border-radius:4px;
                    font-size:12px; font-weight:bold; padding:4px 0;
                """)
                badge.setFixedHeight(26)
                badge_row.addWidget(badge)
            badge_row.addStretch()
            layout.addLayout(badge_row)

        layout.addStretch()
        return w

    # ═══════════════════════════════════════════════════════════
    # TAB 2 — Bilgileri Düzenle
    # ═══════════════════════════════════════════════════════════
    def _tab_bilgiler(self) -> QWidget:
        p = self.profil
        w = QWidget()
        w.setStyleSheet(f"background:{BG};")
        layout = QVBoxLayout(w)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(12)

        # Ad / Soyad
        row_ad = QHBoxLayout()
        ad_col = QVBoxLayout()
        ad_col.addWidget(_lbl("Ad", color=MUTED, size=12))
        self.inp_ad = self._input(p["ad"])
        ad_col.addWidget(self.inp_ad)

        soyad_col = QVBoxLayout()
        soyad_col.addWidget(_lbl("Soyad", color=MUTED, size=12))
        self.inp_soyad = self._input(p["soyad"])
        soyad_col.addWidget(self.inp_soyad)

        row_ad.addLayout(ad_col)
        row_ad.addSpacing(12)
        row_ad.addLayout(soyad_col)
        layout.addLayout(row_ad)

        # E-mail
        layout.addWidget(_lbl("E-mail", color=MUTED, size=12))
        self.inp_email = self._input(p["email"])
        layout.addWidget(self.inp_email)

        # Cinsiyet
        layout.addWidget(_lbl("Cinsiyet", color=MUTED, size=12))
        self.cmb_cinsiyet = QComboBox()
        self.cmb_cinsiyet.addItems(["Seçiniz", "Erkek", "Kadın", "Diğer"])
        self.cmb_cinsiyet.setStyleSheet(STYLE_INPUT)
        current_gender = p.get("cinsiyet") or "Seçiniz"
        idx = self.cmb_cinsiyet.findText(current_gender)
        if idx >= 0:
            self.cmb_cinsiyet.setCurrentIndex(idx)
        layout.addWidget(self.cmb_cinsiyet)

        # Doğum tarihi
        layout.addWidget(_lbl("Doğum Tarihi", color=MUTED, size=12))
        self.inp_dogum = QDateEdit()
        self.inp_dogum.setCalendarPopup(True)
        self.inp_dogum.setDisplayFormat("dd/MM/yyyy")
        self.inp_dogum.setMaximumDate(QDate.currentDate())
        self.inp_dogum.setStyleSheet(STYLE_INPUT)
        if p["dogum_tarihi"]:
            d = p["dogum_tarihi"]
            self.inp_dogum.setDate(QDate(d.year, d.month, d.day))
        layout.addWidget(self.inp_dogum)

        # Ülke
        layout.addWidget(_lbl("Ülke", color=MUTED, size=12))
        self.inp_ulke = self._input(p["ulke"] or "")
        layout.addWidget(self.inp_ulke)

        # Mesaj etiketi
        self.lbl_bilgi_msg = QLabel("")
        self.lbl_bilgi_msg.setStyleSheet(STYLE_ERROR)
        self.lbl_bilgi_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_bilgi_msg)

        # Kaydet butonu
        btn = QPushButton("💾  Bilgileri Kaydet")
        btn.setStyleSheet(STYLE_BTN_RED)
        btn.clicked.connect(self._handle_bilgi_guncelle)
        layout.addWidget(btn)

        layout.addStretch()
        return w

    # ═══════════════════════════════════════════════════════════
    # TAB 3 — Şifre Değiştir
    # ═══════════════════════════════════════════════════════════
    def _tab_sifre(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet(f"background:{BG};")
        layout = QVBoxLayout(w)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(12)

        layout.addWidget(_lbl("Mevcut Şifre", color=MUTED, size=12))
        self.inp_eski_sifre = self._input("Mevcut şifreniz", password=True)
        layout.addWidget(self.inp_eski_sifre)

        layout.addWidget(_lbl("Yeni Şifre", color=MUTED, size=12))
        self.inp_yeni_sifre = self._input("En az 6 karakter", password=True)
        layout.addWidget(self.inp_yeni_sifre)

        layout.addWidget(_lbl("Yeni Şifre Tekrar", color=MUTED, size=12))
        self.inp_yeni_sifre2 = self._input("Yeni şifreyi tekrar girin", password=True)
        layout.addWidget(self.inp_yeni_sifre2)

        self.lbl_sifre_msg = QLabel("")
        self.lbl_sifre_msg.setStyleSheet(STYLE_ERROR)
        self.lbl_sifre_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_sifre_msg)

        btn = QPushButton("🔒  Şifreyi Güncelle")
        btn.setStyleSheet(STYLE_BTN_RED)
        btn.clicked.connect(self._handle_sifre_guncelle)
        layout.addWidget(btn)

        layout.addStretch()
        return w

    # ═══════════════════════════════════════════════════════════
    # TAB 4 — Favori Türler
    # ═══════════════════════════════════════════════════════════
    def _tab_turler(self) -> QWidget:
        p = self.profil
        mevcut_ids = {t["tur_id"] for t in (p.get("favori_turler") or [])}

        w = QWidget()
        w.setStyleSheet(f"background:{BG};")
        layout = QVBoxLayout(w)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(12)

        layout.addWidget(_lbl("Tam olarak 3 tür seçin", color=MUTED, size=12))

        genre_frame = QFrame()
        genre_frame.setStyleSheet(
            f"QFrame{{background:{BG2}; border:1px solid {BORDER}; border-radius:8px; padding:6px;}}"
        )
        grid = QGridLayout(genre_frame)
        grid.setSpacing(8)
        genres = get_all_genres()
        cols = 2
        self.genre_checkboxes = {}
        for i, g in enumerate(genres):
            cb = QCheckBox(g["tur_adi"])
            cb.setChecked(g["tur_id"] in mevcut_ids)
            cb.setStyleSheet(f"""
                QCheckBox {{ color:#cccccc; font-size:13px; }}
                QCheckBox::indicator {{ width:16px; height:16px; border-radius:3px;
                                        border:1px solid #555; background:{BG3}; }}
                QCheckBox::indicator:checked {{ background:{RED}; border-color:{RED}; }}
            """)
            cb.stateChanged.connect(self._enforce_max_three_tur)
            self.genre_checkboxes[g["tur_id"]] = cb
            grid.addWidget(cb, i // cols, i % cols)
        layout.addWidget(genre_frame)

        self.lbl_tur_msg = QLabel("")
        self.lbl_tur_msg.setStyleSheet(STYLE_ERROR)
        self.lbl_tur_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_tur_msg)

        btn = QPushButton("💾  Türleri Kaydet")
        btn.setStyleSheet(STYLE_BTN_RED)
        btn.clicked.connect(self._handle_tur_guncelle)
        layout.addWidget(btn)

        layout.addStretch()
        return w

    # ═══════════════════════════════════════════════════════════
    # YARDIMCI
    # ═══════════════════════════════════════════════════════════
    def _input(self, value="", password=False) -> QLineEdit:
        inp = QLineEdit(value)
        inp.setStyleSheet(STYLE_INPUT)
        if password:
            inp.setEchoMode(QLineEdit.EchoMode.Password)
        return inp

    def _enforce_max_three_tur(self):
        selected = [cb for cb in self.genre_checkboxes.values() if cb.isChecked()]
        if len(selected) > 3:
            self.sender().setChecked(False)

    # ═══════════════════════════════════════════════════════════
    # AKSİYONLAR
    # ═══════════════════════════════════════════════════════════
    def _handle_bilgi_guncelle(self):
        ad    = self.inp_ad.text().strip()
        soyad = self.inp_soyad.text().strip()
        email = self.inp_email.text().strip()
        cinsiyet = self.cmb_cinsiyet.currentText()
        ulke  = self.inp_ulke.text().strip()
        qd    = self.inp_dogum.date()
        dogum = date(qd.year(), qd.month(), qd.day())

        if not all([ad, soyad, email, ulke]):
            self.lbl_bilgi_msg.setStyleSheet(STYLE_ERROR)
            self.lbl_bilgi_msg.setText("Tüm alanlar doldurulmalıdır.")
            return
        if not validate_name(ad):
            self.lbl_bilgi_msg.setStyleSheet(STYLE_ERROR)
            self.lbl_bilgi_msg.setText("Ad sadece harfler, boşluklar ve kesme işareti içermelidir.")
            return
        if not validate_name(soyad):
            self.lbl_bilgi_msg.setStyleSheet(STYLE_ERROR)
            self.lbl_bilgi_msg.setText("Soyad sadece harfler, boşluklar ve kesme işareti içermelidir.")
            return
        if cinsiyet == "Seçiniz":
            self.lbl_bilgi_msg.setStyleSheet(STYLE_ERROR)
            self.lbl_bilgi_msg.setText("Lütfen cinsiyet seçiniz.")
            return
        if not validate_email(email):
            self.lbl_bilgi_msg.setStyleSheet(STYLE_ERROR)
            self.lbl_bilgi_msg.setText("Geçerli bir e-mail giriniz.")
            return
        if not validate_country(ulke):
            self.lbl_bilgi_msg.setStyleSheet(STYLE_ERROR)
            self.lbl_bilgi_msg.setText("Geçerli bir ülke adı giriniz.")
            return
        if dogum > date.today():
            self.lbl_bilgi_msg.setStyleSheet(STYLE_ERROR)
            self.lbl_bilgi_msg.setText("Doğum tarihi bugünden ileri olamaz.")
            return

        ok, err = update_profil(
            self.user["kullanici_id"], ad, soyad, email, dogum, ulke, cinsiyet
        )
        if not ok:
            self.lbl_bilgi_msg.setStyleSheet(STYLE_ERROR)
            self.lbl_bilgi_msg.setText(err)
            return

        self.lbl_bilgi_msg.setStyleSheet(STYLE_SUCCESS)
        self.lbl_bilgi_msg.setText("✅  Bilgiler başarıyla güncellendi.")

        # user dict'ini güncelle
        self.user["ad"]    = ad
        self.user["soyad"] = soyad
        self.user["email"] = email
        self.user["cinsiyet"] = cinsiyet
        if self.on_user_update:
            self.on_user_update(self.user)

    def _handle_sifre_guncelle(self):
        eski   = self.inp_eski_sifre.text()
        yeni   = self.inp_yeni_sifre.text()
        yeni2  = self.inp_yeni_sifre2.text()

        if not all([eski, yeni, yeni2]):
            self.lbl_sifre_msg.setStyleSheet(STYLE_ERROR)
            self.lbl_sifre_msg.setText("Tüm şifre alanları doldurulmalıdır.")
            return
        if yeni != yeni2:
            self.lbl_sifre_msg.setStyleSheet(STYLE_ERROR)
            self.lbl_sifre_msg.setText("Yeni şifreler eşleşmiyor.")
            return
        if len(yeni) < 6:
            self.lbl_sifre_msg.setStyleSheet(STYLE_ERROR)
            self.lbl_sifre_msg.setText("Yeni şifre en az 6 karakter olmalıdır.")
            return

        ok, err = update_sifre(self.user["kullanici_id"], eski, yeni)
        if not ok:
            self.lbl_sifre_msg.setStyleSheet(STYLE_ERROR)
            self.lbl_sifre_msg.setText(err)
            return

        self.lbl_sifre_msg.setStyleSheet(STYLE_SUCCESS)
        self.lbl_sifre_msg.setText("✅  Şifre başarıyla güncellendi.")
        self.inp_eski_sifre.clear()
        self.inp_yeni_sifre.clear()
        self.inp_yeni_sifre2.clear()

    def _handle_tur_guncelle(self):
        ids = [tid for tid, cb in self.genre_checkboxes.items() if cb.isChecked()]
        if len(ids) != 3:
            self.lbl_tur_msg.setStyleSheet(STYLE_ERROR)
            self.lbl_tur_msg.setText("Lütfen tam olarak 3 tür seçiniz.")
            return

        ok, err = update_favori_turler(self.user["kullanici_id"], ids)
        if not ok:
            self.lbl_tur_msg.setStyleSheet(STYLE_ERROR)
            self.lbl_tur_msg.setText(err)
            return

        self.lbl_tur_msg.setStyleSheet(STYLE_SUCCESS)
        self.lbl_tur_msg.setText("✅  Favori türler güncellendi.")

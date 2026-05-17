from PyQt6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QComboBox,
    QVBoxLayout, QHBoxLayout, QTextEdit, QSpinBox,
    QCheckBox, QGridLayout, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from auth import get_all_genres

BG     = "#141414"
BG2    = "#1e1e1e"
BG3    = "#2b2b2b"
RED    = "#E50914"
TEXT   = "#ffffff"
MUTED  = "#aaaaaa"
BORDER = "#333333"

STYLE_INPUT = f"""
    QLineEdit, QComboBox, QSpinBox, QTextEdit {{
        background:{BG3}; color:white; border:1px solid {BORDER};
        border-radius:6px; padding:4px 12px; font-size:13px;
    }}
    QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QTextEdit:focus {{
        border-color:{RED};
    }}
    QComboBox QAbstractItemView {{
        background:{BG3}; color:white; selection-background-color:{RED};
    }}
    QComboBox::drop-down {{ border:none; width:20px; }}
    QSpinBox::up-button, QSpinBox::down-button {{ background:{BG3}; border:none; width:20px; }}
"""
STYLE_BTN_RED = f"""
    QPushButton {{
        background:{RED}; color:white; border-radius:6px;
        font-size:13px; font-weight:bold; min-height:38px; padding:0 20px;
    }}
    QPushButton:hover  {{ background:#f40612; }}
    QPushButton:pressed{{ background:#b2070f; }}
"""
STYLE_BTN_GRAY = f"""
    QPushButton {{
        background:{BG3}; color:{TEXT}; border:1px solid {BORDER};
        border-radius:6px; font-size:13px; min-height:38px; padding:0 20px;
    }}
    QPushButton:hover {{ border-color:#666; }}
"""


def _lbl(text, color=MUTED, size=12) -> QLabel:
    l = QLabel(text)
    l.setStyleSheet(f"color:{color}; font-size:{size}px;")
    return l


class ProgramDialog(QDialog):
    """Program ekleme / güncelleme dialog'u."""

    def __init__(self, parent=None, program: dict = None):
        super().__init__(parent)
        self.program = program  # None ise yeni ekleme, dolu ise güncelleme
        self.genre_checkboxes = {}

        self.setWindowTitle("Program Ekle" if not program else "Program Güncelle")
        self.setFixedSize(540, 620)
        self.setStyleSheet(f"background:{BG}; color:{TEXT};")
        self._build_ui()
        if program:
            self._fill_fields()

    # ───────────────────────────────────────────────────────
    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(12)

        # Program Adı
        layout.addWidget(_lbl("Program Adı *"))
        self.inp_adi = QLineEdit()
        self.inp_adi.setStyleSheet(STYLE_INPUT)
        self.inp_adi.setFixedHeight(36)
        layout.addWidget(self.inp_adi)

        # Tip + Yıl
        row1 = QHBoxLayout()
        tip_col = QVBoxLayout()
        tip_col.addWidget(_lbl("Program Tipi *"))
        self.cmb_tip = QComboBox()
        self.cmb_tip.addItems(["Film", "Dizi"])
        self.cmb_tip.setFixedHeight(36)
        self.cmb_tip.setStyleSheet(STYLE_INPUT)
        tip_col.addWidget(self.cmb_tip)

        yil_col = QVBoxLayout()
        yil_col.addWidget(_lbl("Yayın Yılı *"))
        self.spin_yil = QSpinBox()
        self.spin_yil.setRange(1900, 2100)
        self.spin_yil.setValue(2024)
        self.spin_yil.setFixedHeight(36)
        self.spin_yil.setStyleSheet(STYLE_INPUT)
        yil_col.addWidget(self.spin_yil)

        row1.addLayout(tip_col)
        row1.addSpacing(12)
        row1.addLayout(yil_col)
        layout.addLayout(row1)

        # Bölüm sayısı + Uzunluk
        row2 = QHBoxLayout()
        bs_col = QVBoxLayout()
        bs_col.addWidget(_lbl("Bölüm Sayısı *"))
        self.spin_bolum = QSpinBox()
        self.spin_bolum.setRange(1, 9999)
        self.spin_bolum.setValue(1)
        self.spin_bolum.setFixedHeight(36)
        self.spin_bolum.setStyleSheet(STYLE_INPUT)
        bs_col.addWidget(self.spin_bolum)

        dk_col = QVBoxLayout()
        dk_col.addWidget(_lbl("Bölüm Uzunluğu (dk) *"))
        self.spin_dk = QSpinBox()
        self.spin_dk.setRange(1, 999)
        self.spin_dk.setValue(90)
        self.spin_dk.setFixedHeight(36)
        self.spin_dk.setStyleSheet(STYLE_INPUT)
        dk_col.addWidget(self.spin_dk)

        row2.addLayout(bs_col)
        row2.addSpacing(12)
        row2.addLayout(dk_col)
        layout.addLayout(row2)

        # Açıklama
        layout.addWidget(_lbl("Açıklama"))
        self.inp_aciklama = QTextEdit()
        self.inp_aciklama.setFixedHeight(72)
        self.inp_aciklama.setStyleSheet(STYLE_INPUT)
        layout.addWidget(self.inp_aciklama)

        # Türler
        layout.addWidget(_lbl("Türler * (en az 1 seçin)"))
        genre_frame = QFrame()
        genre_frame.setStyleSheet(
            f"QFrame{{background:{BG2}; border:1px solid {BORDER}; border-radius:8px;}}"
        )
        grid = QGridLayout(genre_frame)
        grid.setContentsMargins(12, 8, 12, 8)
        grid.setSpacing(6)
        genres = get_all_genres()
        for i, g in enumerate(genres):
            cb = QCheckBox(g["tur_adi"])
            cb.setStyleSheet(f"""
                QCheckBox {{ color:#cccccc; font-size:12px; }}
                QCheckBox::indicator {{ width:15px; height:15px; border-radius:3px;
                                        border:1px solid #555; background:{BG3}; }}
                QCheckBox::indicator:checked {{ background:{RED}; border-color:{RED}; }}
            """)
            self.genre_checkboxes[g["tur_id"]] = cb
            grid.addWidget(cb, i // 3, i % 3)
        layout.addWidget(genre_frame)

        # Hata etiketi
        self.lbl_err = QLabel("")
        self.lbl_err.setStyleSheet("color:#ff4444; font-size:12px;")
        self.lbl_err.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_err)

        # Butonlar
        btn_row = QHBoxLayout()
        btn_iptal = QPushButton("İptal")
        btn_iptal.setStyleSheet(STYLE_BTN_GRAY)
        btn_iptal.clicked.connect(self.reject)
        btn_row.addWidget(btn_iptal)

        self.btn_kaydet = QPushButton("💾  Kaydet")
        self.btn_kaydet.setStyleSheet(STYLE_BTN_RED)
        self.btn_kaydet.clicked.connect(self._validate)
        btn_row.addWidget(self.btn_kaydet)
        layout.addLayout(btn_row)

    def _fill_fields(self):
        p = self.program
        self.inp_adi.setText(p["program_adi"])
        self.cmb_tip.setCurrentText(p["program_tipi"])
        self.spin_yil.setValue(int(p["yayin_yili"]))
        self.spin_bolum.setValue(int(p["bolum_sayisi"]))
        self.spin_dk.setValue(int(p["bolum_uzunluk_dk"] or 1))
        if p.get("aciklama"):
            self.inp_aciklama.setText(p["aciklama"])

        # Mevcut türleri işaretle
        if p.get("turler"):
            mevcut = {t.strip() for t in p["turler"].split(",")}
            for tid, cb in self.genre_checkboxes.items():
                if cb.text() in mevcut:
                    cb.setChecked(True)

    def _validate(self):
        adi  = self.inp_adi.text().strip()
        tids = [tid for tid, cb in self.genre_checkboxes.items() if cb.isChecked()]

        if not adi:
            self.lbl_err.setText("Program adı boş bırakılamaz.")
            return
        if not tids:
            self.lbl_err.setText("En az bir tür seçilmelidir.")
            return

        self.result_data = {
            "program_adi":      adi,
            "aciklama":         self.inp_aciklama.toPlainText().strip(),
            "program_tipi":     self.cmb_tip.currentText(),
            "yayin_yili":       self.spin_yil.value(),
            "bolum_sayisi":     self.spin_bolum.value(),
            "bolum_uzunluk_dk": self.spin_dk.value(),
            "tur_ids":          tids,
        }
        self.accept()

    def get_data(self) -> dict:
        return getattr(self, "result_data", {})


class TurDialog(QDialog):
    """Tür ekleme / güncelleme dialog'u."""

    def __init__(self, parent=None, tur: dict = None):
        super().__init__(parent)
        self.tur = tur
        self.setWindowTitle("Tür Ekle" if not tur else "Tür Güncelle")
        self.setFixedSize(360, 200)
        self.setStyleSheet(f"background:{BG}; color:{TEXT};")
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        layout.addWidget(_lbl("Tür Adı *"))
        self.inp_adi = QLineEdit()
        self.inp_adi.setFixedHeight(36)
        self.inp_adi.setStyleSheet(STYLE_INPUT)
        if self.tur:
            self.inp_adi.setText(self.tur["tur_adi"])
        layout.addWidget(self.inp_adi)

        self.lbl_err = QLabel("")
        self.lbl_err.setStyleSheet("color:#ff4444; font-size:12px;")
        layout.addWidget(self.lbl_err)

        btn_row = QHBoxLayout()
        btn_iptal = QPushButton("İptal")
        btn_iptal.setStyleSheet(STYLE_BTN_GRAY)
        btn_iptal.clicked.connect(self.reject)
        btn_row.addWidget(btn_iptal)

        btn_kaydet = QPushButton("💾  Kaydet")
        btn_kaydet.setStyleSheet(STYLE_BTN_RED)
        btn_kaydet.clicked.connect(self._validate)
        btn_row.addWidget(btn_kaydet)
        layout.addLayout(btn_row)

    def _validate(self):
        adi = self.inp_adi.text().strip()
        if not adi:
            self.lbl_err.setText("Tür adı boş bırakılamaz.")
            return
        self.result_adi = adi
        self.accept()

    def get_adi(self) -> str:
        return getattr(self, "result_adi", "")

from PyQt6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QSlider, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt
from queries import kaydet_puan, get_kullanici_program

BG     = "#141414"
BG2    = "#1e1e1e"
BG3    = "#2b2b2b"
RED    = "#E50914"
BORDER = "#333333"
TEXT_MUTED = "#aaaaaa"


class RatingDialog(QDialog):
    def __init__(self, user, program, parent=None):
        super().__init__(parent)
        self.user    = user
        self.program = program
        self.setWindowTitle("⭐ Puan Ver")
        self.setFixedSize(400, 280)
        self.setStyleSheet(f"background:{BG}; color:white;")
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        # Başlık
        title = QLabel(self.program["program_adi"])
        title.setStyleSheet("font-size:16px; font-weight:bold; color:white;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color:{BORDER};")
        layout.addWidget(sep)

        # Mevcut puan bilgisi
        kp = get_kullanici_program(self.user["kullanici_id"], self.program["program_id"])
        mevcut = int(kp["puan"]) if kp and kp.get("puan") else 5
        info_lbl = QLabel(f"Mevcut puanınız: {kp['puan']}" if (kp and kp.get("puan")) else "Henüz puan vermediniz")
        info_lbl.setStyleSheet(f"color:{TEXT_MUTED}; font-size:12px;")
        info_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_lbl)

        # Puan göstergesi
        self.puan_lbl = QLabel(f"⭐ {mevcut}")
        self.puan_lbl.setStyleSheet("font-size:32px; font-weight:bold; color:#E50914;")
        self.puan_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.puan_lbl)

        # Slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(1, 10)
        self.slider.setValue(mevcut)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                height:6px; background:{BG3}; border-radius:3px;
            }}
            QSlider::handle:horizontal {{
                background:{RED}; width:18px; height:18px;
                margin:-6px 0; border-radius:9px;
            }}
            QSlider::sub-page:horizontal {{
                background:{RED}; border-radius:3px;
            }}
        """)
        self.slider.valueChanged.connect(lambda v: self.puan_lbl.setText(f"⭐ {v}"))
        layout.addWidget(self.slider)

        # 1-10 etiketleri
        tick_row = QHBoxLayout()
        for i in range(1, 11):
            lbl = QLabel(str(i))
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet(f"color:{TEXT_MUTED}; font-size:10px;")
            tick_row.addWidget(lbl)
        layout.addLayout(tick_row)

        # Butonlar
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        btn_iptal = QPushButton("İptal")
        btn_iptal.setFixedHeight(36)
        btn_iptal.setStyleSheet(f"""
            QPushButton {{ background:{BG3}; color:{TEXT_MUTED}; border-radius:6px;
                font-size:13px; border:1px solid {BORDER}; }}
            QPushButton:hover {{ color:white; }}
        """)
        btn_iptal.clicked.connect(self.reject)

        btn_kaydet = QPushButton("💾 Puanı Kaydet")
        btn_kaydet.setFixedHeight(36)
        btn_kaydet.setStyleSheet(f"""
            QPushButton {{ background:{RED}; color:white; border-radius:6px;
                font-size:13px; font-weight:bold; }}
            QPushButton:hover {{ background:#f40612; }}
        """)
        btn_kaydet.clicked.connect(self._kaydet)

        btn_row.addWidget(btn_iptal)
        btn_row.addWidget(btn_kaydet)
        layout.addLayout(btn_row)

    def _kaydet(self):
        puan = self.slider.value()
        ok, msg = kaydet_puan(
            self.user["kullanici_id"],
            self.program["program_id"],
            puan
        )
        if ok:
            QMessageBox.information(self, "Başarılı", f"Puanınız ({puan}) kaydedildi.")
            self.accept()
        else:
            QMessageBox.warning(self, "Hata", msg)

from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QSpinBox, QSlider, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from queries import kaydet_izleme, kaydet_puan

BG    = "#141414"
BG2   = "#1e1e1e"
BG3   = "#2b2b2b"
RED   = "#E50914"
TEXT  = "#ffffff"
MUTED = "#aaaaaa"
GOLD  = "#ffd54f"
BORDER = "#333333"

STYLE_BTN_RED = f"""
    QPushButton {{
        background:{RED}; color:white; border-radius:6px;
        font-size:13px; font-weight:bold; min-height:42px; padding:0 24px;
    }}
    QPushButton:hover  {{ background:#f40612; }}
    QPushButton:pressed{{ background:#b2070f; }}
"""
STYLE_BTN_GRAY = f"""
    QPushButton {{
        background:{BG3}; color:{TEXT}; border:1px solid {BORDER};
        border-radius:6px; font-size:13px; min-height:42px; padding:0 24px;
    }}
    QPushButton:hover {{ border-color:#666; }}
"""
STYLE_BTN_GREEN = """
    QPushButton {
        background:#2e7d32; color:white; border-radius:6px;
        font-size:13px; font-weight:bold; min-height:42px; padding:0 24px;
    }
    QPushButton:hover { background:#388e3c; }
"""


def _lbl(text, size=13, bold=False, color=TEXT, align=Qt.AlignmentFlag.AlignLeft) -> QLabel:
    l = QLabel(text)
    l.setStyleSheet(f"color:{color}; font-size:{size}px;")
    l.setAlignment(align)
    if bold:
        l.setFont(QFont("Arial", size, QFont.Weight.Bold))
    return l


def _divider():
    f = QFrame()
    f.setFrameShape(QFrame.Shape.HLine)
    f.setStyleSheet(f"background:{BORDER}; max-height:1px;")
    return f


class WatchPage(QWidget):
    def __init__(self, user: dict, program: dict, devam: bool,
                 devam_state: dict | None, on_close):
        super().__init__()
        self.user        = user
        self.program     = program
        self.devam_state = devam_state
        self.on_close    = on_close

        # Başlangıç bölüm/dakika
        if devam and devam_state:
            self.baslangic_bolum = devam_state["son_bolum_no"]
            self.baslangic_dk    = devam_state["son_izleme_dk"]
        else:
            self.baslangic_bolum = program.get("secili_bolum", 1)
            self.baslangic_dk    = 0

        self.setWindowTitle("▶  İzleme Ekranı")
        self.setFixedSize(560, 620)
        self.setStyleSheet(f"background:{BG}; color:{TEXT};")
        self._build_ui()

    # ═══════════════════════════════════════════════════════════
    def _build_ui(self):
        p = self.program
        is_dizi = p["program_tipi"] == "Dizi"
        bolum_sayisi = int(p.get("bolum_sayisi") or 1)

        root = QVBoxLayout(self)
        root.setContentsMargins(36, 28, 36, 28)
        root.setSpacing(18)

        # ── Başlık ──────────────────────────────────────────
        title = _lbl(p["program_adi"], size=20, bold=True,
                     align=Qt.AlignmentFlag.AlignCenter)
        root.addWidget(title)

        # Tip rozeti
        tip_lbl = QLabel(f"  {p['program_tipi']}  ")
        tip_lbl.setFixedHeight(24)
        tip_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tip_lbl.setStyleSheet(f"""
            background:{"#1565c0" if p["program_tipi"]=="Film" else "#2e7d32"};
            color:white; border-radius:4px; font-size:11px; font-weight:bold;
        """)
        row_tip = QHBoxLayout()
        row_tip.addStretch()
        row_tip.addWidget(tip_lbl)
        row_tip.addStretch()
        root.addLayout(row_tip)

        root.addWidget(_divider())

        # ── Bölüm bilgisi ───────────────────────────────────
        card = QFrame()
        card.setStyleSheet(f"background:{BG2}; border-radius:10px;")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 16, 20, 16)
        card_layout.setSpacing(12)

        # Bölüm no (Dizi)
        if is_dizi:
            bolum_row = QHBoxLayout()
            bolum_row.addWidget(_lbl("İzlenen Bölüm:", color=MUTED))
            self.spin_bolum = QSpinBox()
            self.spin_bolum.setRange(1, bolum_sayisi)
            self.spin_bolum.setValue(self.baslangic_bolum)
            self.spin_bolum.setStyleSheet(f"""
                QSpinBox {{
                    background:{BG3}; color:white; border:1px solid {BORDER};
                    border-radius:6px; padding:4px 10px; font-size:14px; min-width:80px;
                }}
                QSpinBox::up-button, QSpinBox::down-button {{
                    background:{BG3}; border:none; width:20px;
                }}
            """)
            bolum_row.addWidget(self.spin_bolum)
            bolum_row.addWidget(_lbl(f"/ {bolum_sayisi}", color=MUTED))
            bolum_row.addStretch()
            card_layout.addLayout(bolum_row)
        else:
            card_layout.addWidget(_lbl("Film (tek bölüm)", color=MUTED))

        # İzleme süresi
        sure_row = QHBoxLayout()
        sure_row.addWidget(_lbl("İzleme Süresi (dakika):", color=MUTED))
        self.spin_sure = QSpinBox()
        max_sure = int(p.get("bolum_uzunluk_dk") or 300)
        self.spin_sure.setRange(1, max_sure)
        self.spin_sure.setValue(self.baslangic_dk if self.baslangic_dk > 0
                                else max_sure)
        self.spin_sure.setStyleSheet(f"""
            QSpinBox {{
                background:{BG3}; color:white; border:1px solid {BORDER};
                border-radius:6px; padding:4px 10px; font-size:14px; min-width:80px;
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                background:{BG3}; border:none; width:20px;
            }}
        """)
        sure_row.addWidget(self.spin_sure)
        sure_row.addWidget(_lbl("dk", color=MUTED))
        sure_row.addStretch()
        card_layout.addLayout(sure_row)

        # Başlangıç bilgisi (devam modunda)
        if self.baslangic_dk > 0:
            bolum_no = self.baslangic_bolum
            info = _lbl(
                f"⏸  {bolum_no}. bölüm {self.baslangic_dk}. dakikadan devam ediyorsunuz",
                color=GOLD, size=12
            )
            card_layout.addWidget(info)

        root.addWidget(card)
        root.addWidget(_divider())

        # ── Puan ver ────────────────────────────────────────
        puan_frame = QFrame()
        puan_frame.setStyleSheet(f"background:{BG2}; border-radius:10px;")
        puan_layout = QVBoxLayout(puan_frame)
        puan_layout.setContentsMargins(20, 14, 20, 14)
        puan_layout.setSpacing(10)
        puan_layout.addWidget(_lbl("⭐  İçeriğe Puan Ver (1-10)", size=13, bold=True))

        slider_row = QHBoxLayout()
        self.puan_slider = QSlider(Qt.Orientation.Horizontal)
        self.puan_slider.setRange(1, 10)
        self.puan_slider.setValue(7)
        self.puan_slider.setTickInterval(1)
        self.puan_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.puan_slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                background:{BG3}; height:6px; border-radius:3px;
            }}
            QSlider::handle:horizontal {{
                background:{RED}; width:18px; height:18px;
                margin:-6px 0; border-radius:9px;
            }}
            QSlider::sub-page:horizontal {{
                background:{RED}; border-radius:3px;
            }}
        """)
        self.puan_slider.valueChanged.connect(
            lambda v: self.puan_val_lbl.setText(str(v))
        )
        slider_row.addWidget(self.puan_slider)

        self.puan_val_lbl = _lbl("7", size=16, bold=True, color=GOLD)
        self.puan_val_lbl.setFixedWidth(28)
        self.puan_val_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        slider_row.addWidget(self.puan_val_lbl)
        puan_layout.addLayout(slider_row)

        # 1–10 etiketleri
        ticks_row = QHBoxLayout()
        ticks_row.setContentsMargins(0, 0, 28, 0)
        for i in range(1, 11):
            t = QLabel(str(i))
            t.setStyleSheet(f"color:{MUTED}; font-size:10px;")
            t.setAlignment(Qt.AlignmentFlag.AlignCenter)
            ticks_row.addWidget(t)
        puan_layout.addLayout(ticks_row)

        root.addWidget(puan_frame)

        # ── Butonlar ────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        btn_kaydet = QPushButton("💾  Kaldığım Yere Kaydet")
        btn_kaydet.setStyleSheet(STYLE_BTN_GRAY)
        btn_kaydet.clicked.connect(self._handle_kaydet)
        btn_row.addWidget(btn_kaydet)

        btn_tamamla = QPushButton("✅  İzlemeyi Tamamla")
        btn_tamamla.setStyleSheet(STYLE_BTN_GREEN)
        btn_tamamla.clicked.connect(self._handle_tamamla)
        btn_row.addWidget(btn_tamamla)

        root.addLayout(btn_row)

    # ═══════════════════════════════════════════════════════════
    # AKSİYONLAR
    # ═══════════════════════════════════════════════════════════
    def _get_values(self):
        bolum_no = self.spin_bolum.value() \
            if hasattr(self, "spin_bolum") else 1
        sure_dk  = self.spin_sure.value()
        puan     = self.puan_slider.value()
        return bolum_no, sure_dk, puan

    def _validate_sure(self, sure_dk):
        """İzleme süresini bölüm süresine göre kontrol et."""
        max_sure = self._max_sure()
        if max_sure > 0 and sure_dk > max_sure:
            QMessageBox.warning(
                self, "Geçersiz Süre",
                f"⚠️  İzleme süresi {max_sure} dakikayı aşamaz!\n"
                f"Girilen süre: {sure_dk} dakika"
            )
            return False
        return True

    def _max_sure(self):
        """İzlenecek program/bölümün maksimum süresini getir."""
        # Dizi ise seçilen bölümün süresi, film ise program süresi
        if self.program["program_tipi"] == "Dizi":
            # Bölüm süresi: spin_bolum'dan alınan bölüm numarasıyla eşleş
            # Basit şekilde: program'ın genel bölüm_süresi_dk kullan
            return int(self.program.get("bolum_suresi_dk") or 120)
        else:
            # Film: program süresi
            return int(self.program.get("bolum_suresi_dk") or 120)

    def _handle_kaydet(self):
        bolum_no, sure_dk, puan = self._get_values()
        if not self._validate_sure(sure_dk):
            return
        ok, err = kaydet_izleme(
            self.user["kullanici_id"], self.program["program_id"],
            bolum_no, sure_dk, tamamlandi=False
        )
        if not ok:
            QMessageBox.critical(self, "Hata", f"Kaydedilemedi: {err}")
            return
        # Puan varsa kaydet
        kaydet_puan(self.user["kullanici_id"], self.program["program_id"], puan)
        QMessageBox.information(
            self, "Kaydedildi",
            f"✅  {bolum_no}. bölüm {sure_dk}. dakika kaydedildi.\n"
            f"⭐  Puanınız: {puan}/10"
        )
        self.close()

    def _handle_tamamla(self):
        bolum_no, sure_dk, puan = self._get_values()
        if not self._validate_sure(sure_dk):
            return
        ok, err = kaydet_izleme(
            self.user["kullanici_id"], self.program["program_id"],
            bolum_no, sure_dk, tamamlandi=True
        )
        if not ok:
            QMessageBox.critical(self, "Hata", f"Kaydedilemedi: {err}")
            return
        kaydet_puan(self.user["kullanici_id"], self.program["program_id"], puan)
        QMessageBox.information(
            self, "Tamamlandı",
            f"🎉  İzleme tamamlandı!\n⭐  Puanınız: {puan}/10"
        )
        self.close()

    def closeEvent(self, event):
        self.on_close()
        super().closeEvent(event)


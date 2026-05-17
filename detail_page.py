from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QScrollArea, QComboBox, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from queries import (
    get_program_detail, get_kullanici_program,
    get_bolumler, get_watching_state, toggle_favori
)

# ── Renkler ─────────────────────────────────────────────────
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
        font-size:13px; font-weight:bold; min-height:40px; padding:0 20px;
    }}
    QPushButton:hover  {{ background:#f40612; }}
    QPushButton:pressed{{ background:#b2070f; }}
"""
STYLE_BTN_OUTLINE = f"""
    QPushButton {{
        background:transparent; color:{TEXT}; border:1px solid #555;
        border-radius:6px; font-size:13px; min-height:40px; padding:0 20px;
    }}
    QPushButton:hover {{ border-color:{RED}; color:{RED}; }}
"""
STYLE_BTN_GREEN = """
    QPushButton {
        background:#2e7d32; color:white; border-radius:6px;
        font-size:13px; font-weight:bold; min-height:40px; padding:0 20px;
    }
    QPushButton:hover { background:#388e3c; }
"""


def _lbl(text, size=13, bold=False, color=TEXT, wrap=False) -> QLabel:
    l = QLabel(text)
    l.setStyleSheet(f"color:{color}; font-size:{size}px;")
    if bold:
        l.setFont(QFont("Arial", size, QFont.Weight.Bold))
    if wrap:
        l.setWordWrap(True)
    return l


def _divider():
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setStyleSheet(f"background:{BORDER}; max-height:1px;")
    return line


class DetailPage(QWidget):
    def __init__(self, user: dict, program_id: int, on_izle, on_close_cb=None):
        super().__init__()
        self.user       = user
        self.program_id = program_id
        self.on_izle    = on_izle      # (prog, devam, devam_state) callback
        self.on_close_cb = on_close_cb

        self.setWindowTitle("İçerik Detayı")
        self.setMinimumSize(620, 680)
        self.setStyleSheet(f"background:{BG}; color:{TEXT};")
        self._refresh()

    # ═══════════════════════════════════════════════════════════
    def _refresh(self):
        # Veriyi çek
        self.prog   = get_program_detail(self.program_id)
        self.kp     = get_kullanici_program(self.user["kullanici_id"], self.program_id)
        self.bolumler = []
        if self.prog and self.prog["program_tipi"] == "Dizi":
            self.bolumler = get_bolumler(self.program_id)

        # Eski widget'ı temizle
        old = self.layout()
        if old:
            while old.count():
                item = old.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            QWidget().setLayout(old)

        self._build_ui()

    # ═══════════════════════════════════════════════════════════
    def _build_ui(self):
        if not self.prog:
            layout = QVBoxLayout(self)
            layout.addWidget(_lbl("İçerik bulunamadı.", color=MUTED))
            return

        p  = self.prog
        kp = self.kp

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Scroll ──────────────────────────────────────────
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            "QScrollArea{border:none; background:transparent;}"
            "QScrollBar:vertical{background:#1a1a1a;width:8px;border-radius:4px;}"
            "QScrollBar::handle:vertical{background:#444;border-radius:4px;}"
            "QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{height:0;}"
        )

        container = QWidget()
        container.setStyleSheet("background:transparent;")
        body = QVBoxLayout(container)
        body.setContentsMargins(36, 28, 36, 28)
        body.setSpacing(16)

        # ── Başlık satırı ───────────────────────────────────
        title_row = QHBoxLayout()
        title_lbl = _lbl(p["program_adi"], size=22, bold=True)
        title_row.addWidget(title_lbl)
        title_row.addStretch()

        # Favori butonu
        is_fav = self._is_favori()
        self.btn_fav = QPushButton("❤️  Favoriden Çıkar" if is_fav else "🤍  Favoriye Ekle")
        self.btn_fav.setStyleSheet(STYLE_BTN_OUTLINE)
        self.btn_fav.clicked.connect(self._handle_favori)
        title_row.addWidget(self.btn_fav)
        body.addLayout(title_row)

        # ── Tip + Tür rozetleri ─────────────────────────────
        badge_row = QHBoxLayout()
        badge_row.setSpacing(8)
        self._add_badge(badge_row, p["program_tipi"],
                        "#1565c0" if p["program_tipi"] == "Film" else "#2e7d32")
        for tur in (p["turler"] or "").split(","):
            tur = tur.strip()
            if tur:
                self._add_badge(badge_row, tur, "#4a4a4a")
        badge_row.addStretch()
        body.addLayout(badge_row)

        body.addWidget(_divider())

        # ── Bilgi grid ──────────────────────────────────────
        grid = QHBoxLayout()
        grid.setSpacing(40)

        left_col = QVBoxLayout()
        left_col.setSpacing(8)
        left_col.addWidget(self._info_row("📅 Yayın Yılı", str(p["yayin_yili"])))
        left_col.addWidget(self._info_row("📺 Bölüm Sayısı", str(p["bolum_sayisi"])))
        left_col.addWidget(self._info_row("⏱ Bölüm Uzunluğu",
                                          f"{p['bolum_uzunluk_dk']} dk" if p["bolum_uzunluk_dk"] else "—"))

        right_col = QVBoxLayout()
        right_col.setSpacing(8)
        puan_str = f"{float(p['ortalama_puan']):.1f} / 10" if p["ortalama_puan"] else "—"
        right_col.addWidget(self._info_row("⭐ Ortalama Puan", puan_str, val_color=GOLD))
        right_col.addWidget(self._info_row("👁 Toplam İzlenme", str(p["toplam_izlenme"])))

        # Kullanıcı izleme durumu
        if kp:
            izlendi_str = "✅ İzlediniz"
            right_col.addWidget(self._info_row("🎬 İzleme Durumu", izlendi_str, val_color="#a5d6a7"))
        else:
            right_col.addWidget(self._info_row("🎬 İzleme Durumu", "Henüz izlenmedi", val_color=MUTED))

        # Kullanıcının verdiği puan
        if kp and kp.get("puan"):
            right_col.addWidget(self._info_row("🌟 Puanınız",
                                               f"{kp['puan']} / 10", val_color=GOLD))
        else:
            right_col.addWidget(self._info_row("🌟 Puanınız", "Puan verilmedi", val_color=MUTED))

        grid.addLayout(left_col)
        grid.addLayout(right_col)
        body.addLayout(grid)

        body.addWidget(_divider())

        # ── Açıklama ────────────────────────────────────────
        body.addWidget(_lbl("Açıklama", size=14, bold=True))
        aciklama = p.get("aciklama") or "Açıklama bulunmuyor."
        body.addWidget(_lbl(aciklama, size=13, color=MUTED, wrap=True))

        # ── Dizi ise bölüm seçimi ───────────────────────────
        if p["program_tipi"] == "Dizi" and self.bolumler:
            body.addWidget(_divider())
            body.addWidget(_lbl("Bölüm Seçimi", size=14, bold=True))

            # Kaldığı bölüm bilgisi
            if kp and kp["son_bolum_no"]:
                bolum_no = kp["son_bolum_no"]
                dk       = kp["son_izleme_dk"]
                info = _lbl(
                    f"⏸  Kaldığınız yer: {bolum_no}. bölüm — {dk}. dakika",
                    color=GOLD, size=13
                )
                body.addWidget(info)

            # Bölüm combo
            bolum_row = QHBoxLayout()
            self.cmb_bolum = QComboBox()
            self.cmb_bolum.setFixedWidth(320)
            self.cmb_bolum.setStyleSheet(f"""
                QComboBox {{
                    background:{BG3}; color:white; border:1px solid {BORDER};
                    border-radius:6px; padding:0 12px; font-size:13px; min-height:36px;
                }}
                QComboBox QAbstractItemView {{
                    background:{BG3}; color:white; selection-background-color:{RED};
                }}
                QComboBox::drop-down {{ border:none; width:20px; }}
            """)
            for b in self.bolumler:
                label = f"Bölüm {b['bolum_no']}"
                if b.get("bolum_adi"):
                    label += f"  —  {b['bolum_adi']}"
                if b.get("sure_dk"):
                    label += f"  ({b['sure_dk']} dk)"
                self.cmb_bolum.addItem(label, b["bolum_no"])

            # Kaldığı bölümü varsayılan seç
            if kp and kp["son_bolum_no"]:
                idx = kp["son_bolum_no"] - 1
                if 0 <= idx < self.cmb_bolum.count():
                    self.cmb_bolum.setCurrentIndex(idx)

            bolum_row.addWidget(self.cmb_bolum)
            bolum_row.addStretch()
            body.addLayout(bolum_row)

        body.addWidget(_divider())

        # ── Alt buton satırı ────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        # Kaldığı yerden devam et (dizi + kp varsa)
        if p["program_tipi"] == "Dizi" and kp and kp["son_izleme_dk"] and not kp["tamamlandi"]:
            btn_devam = QPushButton("⏩  Kaldığımdan Devam Et")
            btn_devam.setStyleSheet(STYLE_BTN_GREEN)
            btn_devam.clicked.connect(lambda: self._handle_izle(devam=True))
            btn_row.addWidget(btn_devam)

        # Normal izle butonu
        btn_izle = QPushButton("▶  İzle")
        btn_izle.setStyleSheet(STYLE_BTN_RED)
        btn_izle.clicked.connect(lambda: self._handle_izle(devam=False))
        btn_row.addWidget(btn_izle)

        btn_row.addStretch()
        body.addLayout(btn_row)

        scroll.setWidget(container)
        root.addWidget(scroll)

    # ═══════════════════════════════════════════════════════════
    # YARDIMCI WIDGET'LAR
    # ═══════════════════════════════════════════════════════════
    def _info_row(self, key: str, value: str, val_color=TEXT) -> QFrame:
        frame = QFrame()
        frame.setStyleSheet("background:transparent;")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        layout.addWidget(_lbl(key, color=MUTED, size=12))
        layout.addWidget(_lbl(value, color=val_color, size=13, bold=True))
        layout.addStretch()
        return frame

    def _add_badge(self, layout, text, bg_color):
        lbl = QLabel(f"  {text}  ")
        lbl.setStyleSheet(f"""
            background:{bg_color}; color:white; border-radius:4px;
            font-size:11px; font-weight:bold; padding:3px 0;
        """)
        lbl.setFixedHeight(22)
        layout.addWidget(lbl)

    def _is_favori(self) -> bool:
        try:
            from database import get_connection
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT favori_id FROM Favori WHERE kullanici_id=%s AND program_id=%s",
                (self.user["kullanici_id"], self.program_id)
            )
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            return row is not None
        except Exception:
            return False

    # ═══════════════════════════════════════════════════════════
    # AKSİYONLAR
    # ═══════════════════════════════════════════════════════════
    def _handle_favori(self):
        new_state = toggle_favori(self.user["kullanici_id"], self.program_id)
        self.btn_fav.setText("❤️  Favoriden Çıkar" if new_state else "🤍  Favoriye Ekle")

    def _handle_izle(self, devam: bool):
        # Seçili bölümü al (dizi ise)
        selected_bolum = 1
        if hasattr(self, "cmb_bolum"):
            selected_bolum = self.cmb_bolum.currentData() or 1

        kp = self.kp
        devam_state = None
        if devam and kp:
            devam_state = {
                "son_bolum_no": kp["son_bolum_no"],
                "son_izleme_dk": kp["son_izleme_dk"],
                "tamamlandi": kp["tamamlandi"]
            }

        prog_with_bolum = dict(self.prog)
        prog_with_bolum["secili_bolum"] = kp["son_bolum_no"] if devam and kp else selected_bolum

        self.on_izle(prog_with_bolum, devam, devam_state)
        self.close()

    def closeEvent(self, event):
        if self.on_close_cb:
            self.on_close_cb()
        super().closeEvent(event)

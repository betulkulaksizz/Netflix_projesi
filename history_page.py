from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from queries import get_izleme_gecmisi

BG     = "#141414"
BG2    = "#1e1e1e"
BG3    = "#2b2b2b"
RED    = "#E50914"
TEXT   = "#ffffff"
MUTED  = "#aaaaaa"
GOLD   = "#ffd54f"
GREEN  = "#a5d6a7"
BORDER = "#333333"

STYLE_BTN_GRAY = f"""
    QPushButton {{
        background:{BG3}; color:{MUTED}; border:1px solid {BORDER};
        border-radius:5px; font-size:12px; padding:5px 16px;
    }}
    QPushButton:hover {{ color:white; border-color:#666; }}
"""


class HistoryPage(QWidget):
    def __init__(self, user: dict):
        super().__init__()
        self.user = user
        self.setWindowTitle("📋  İzleme Geçmişi")
        self.setMinimumSize(900, 580)
        self.setStyleSheet(f"background:{BG}; color:{TEXT};")
        self._build_ui()
        self._load_data()

    # ═══════════════════════════════════════════════════════════
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Top bar ─────────────────────────────────────────
        bar = QFrame()
        bar.setStyleSheet(f"background:{BG2}; border-bottom:1px solid {BORDER};")
        bar.setFixedHeight(52)
        bar_layout = QHBoxLayout(bar)
        bar_layout.setContentsMargins(20, 0, 20, 0)

        title = QLabel("📋  İzleme Geçmişi")
        title.setFont(QFont("Arial", 15, QFont.Weight.Bold))
        title.setStyleSheet(f"color:{TEXT};")
        bar_layout.addWidget(title)
        bar_layout.addStretch()

        btn_yenile = QPushButton("🔄  Yenile")
        btn_yenile.setStyleSheet(STYLE_BTN_GRAY)
        btn_yenile.clicked.connect(self._load_data)
        bar_layout.addWidget(btn_yenile)

        btn_kapat = QPushButton("✕  Kapat")
        btn_kapat.setStyleSheet(STYLE_BTN_GRAY)
        btn_kapat.clicked.connect(self.close)
        bar_layout.addWidget(btn_kapat)

        root.addWidget(bar)

        # ── Tablo ───────────────────────────────────────────
        cols = ["Program Adı", "Tip", "İzleme Tarihi",
                "Bölüm", "Süre (dk)", "Puan", "Tamamlandı"]
        self.table = QTableWidget(0, len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background:{BG}; color:{TEXT}; gridline-color:{BORDER};
                border:none; font-size:13px;
            }}
            QHeaderView::section {{
                background:{BG2}; color:{MUTED}; border:none;
                border-bottom:1px solid {BORDER}; padding:8px;
                font-size:12px; font-weight:bold;
            }}
            QTableWidget::item {{ padding:6px 8px; }}
            QTableWidget::item:selected {{ background:#2a2a2a; color:white; }}
        """)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(44)

        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)

        root.addWidget(self.table)

        # ── Durum çubuğu ────────────────────────────────────
        self.status_lbl = QLabel("")
        self.status_lbl.setStyleSheet(f"color:{MUTED}; font-size:12px; padding:6px 16px;")
        root.addWidget(self.status_lbl)

    # ═══════════════════════════════════════════════════════════
    def _load_data(self):
        rows = get_izleme_gecmisi(self.user["kullanici_id"])
        self.table.setRowCount(0)

        for r in rows:
            row = self.table.rowCount()
            self.table.insertRow(row)

            tarih = str(r["izleme_tarihi"])[:16] if r["izleme_tarihi"] else "—"
            puan  = str(r["puan"]) if r["puan"] else "—"
            tamamlandi = "✅ Evet" if r["tamamlandi"] else "⏸ Hayır"

            self._item(row, 0, r["program_adi"])
            self._item(row, 1, r["program_tipi"],
                       "#4fc3f7" if r["program_tipi"] == "Film" else "#a5d6a7")
            self._item(row, 2, tarih, MUTED)
            self._item(row, 3, str(r["bolum_no"]))
            self._item(row, 4, str(r["izlenen_dk"]))
            self._item(row, 5, puan, GOLD if r["puan"] else MUTED)
            self._item(row, 6, tamamlandi,
                       GREEN if r["tamamlandi"] else "#ffb74d")

        toplam_dk = sum(r["izlenen_dk"] for r in rows)
        self.status_lbl.setText(
            f"{len(rows)} izleme kaydı  |  "
            f"Toplam: {toplam_dk} dakika ({toplam_dk // 60} saat)"
        )

    def _item(self, row, col, text, color=None):
        item = QTableWidgetItem(str(text))
        item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        if color:
            item.setForeground(QColor(color))
        self.table.setItem(row, col, item)


from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QScrollArea, QComboBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QAbstractItemView, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from queries import get_favoriler, toggle_favori
from auth import get_all_genres

BG     = "#141414"
BG2    = "#1e1e1e"
BG3    = "#2b2b2b"
RED    = "#E50914"
TEXT   = "#ffffff"
MUTED  = "#aaaaaa"
GOLD   = "#ffd54f"
BORDER = "#333333"

STYLE_BTN_RED = f"""
    QPushButton {{
        background:{RED}; color:white; border-radius:5px;
        font-size:11px; font-weight:bold; padding:4px 12px;
    }}
    QPushButton:hover {{ background:#f40612; }}
"""
STYLE_BTN_GRAY = f"""
    QPushButton {{
        background:{BG3}; color:{MUTED}; border:1px solid {BORDER};
        border-radius:5px; font-size:11px; padding:4px 12px;
    }}
    QPushButton:hover {{ color:white; border-color:#666; }}
"""
STYLE_FILTER_ACTIVE = f"""
    QPushButton {{
        background:{RED}; color:white; border-radius:14px;
        font-size:12px; font-weight:bold; padding:5px 16px;
    }}
"""
STYLE_FILTER_INACTIVE = f"""
    QPushButton {{
        background:{BG3}; color:{MUTED}; border-radius:14px;
        font-size:12px; padding:5px 16px; border:1px solid {BORDER};
    }}
    QPushButton:hover {{ color:white; }}
"""


class FavoritesPage(QWidget):
    def __init__(self, user: dict, on_izle=None):
        super().__init__()
        self.user    = user
        self.on_izle = on_izle
        self.all_favorites   = []
        self.filtered_favorites = []
        self._active_tip = ""

        self.setWindowTitle("❤️  Favorilerim")
        self.setMinimumSize(960, 620)
        self.setStyleSheet(f"background:{BG}; color:{TEXT};")
        self._build_ui()
        self._load_data()

    # ═══════════════════════════════════════════════════════════
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._make_topbar())
        root.addWidget(self._make_filter_bar())
        root.addWidget(self._make_table())

        self.status_lbl = QLabel("")
        self.status_lbl.setStyleSheet(f"color:{MUTED}; font-size:12px; padding:6px 16px;")
        root.addWidget(self.status_lbl)

    # ── Top bar ─────────────────────────────────────────────
    def _make_topbar(self):
        bar = QFrame()
        bar.setStyleSheet(f"background:{BG2}; border-bottom:1px solid {BORDER};")
        bar.setFixedHeight(52)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(20, 0, 20, 0)

        title = QLabel("❤️  Favorilerim")
        title.setFont(QFont("Arial", 15, QFont.Weight.Bold))
        title.setStyleSheet(f"color:{TEXT};")
        layout.addWidget(title)
        layout.addStretch()

        btn_kapat = QPushButton("✕  Kapat")
        btn_kapat.setStyleSheet(STYLE_BTN_GRAY)
        btn_kapat.clicked.connect(self.close)
        layout.addWidget(btn_kapat)
        return bar

    # ── Filtre çubuğu ───────────────────────────────────────
    def _make_filter_bar(self):
        bar = QFrame()
        bar.setStyleSheet(f"background:{BG2}; border-bottom:1px solid {BORDER};")
        bar.setFixedHeight(50)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(10)

        # Tür filtresi
        self.cmb_tur = QComboBox()
        self.cmb_tur.setFixedWidth(160)
        self.cmb_tur.setStyleSheet(f"""
            QComboBox {{
                background:{BG3}; color:white; border:1px solid {BORDER};
                border-radius:6px; padding:0 10px; font-size:12px; min-height:32px;
            }}
            QComboBox QAbstractItemView {{
                background:{BG3}; color:white; selection-background-color:{RED};
            }}
            QComboBox::drop-down {{ border:none; width:20px; }}
        """)
        self.cmb_tur.addItem("Tüm Türler", "")
        for g in get_all_genres():
            self.cmb_tur.addItem(g["tur_adi"], g["tur_adi"])
        self.cmb_tur.currentIndexChanged.connect(self._apply_filters)
        layout.addWidget(self.cmb_tur)

        layout.addSpacing(6)

        # Tip filtre butonları
        self.btn_hepsi = self._fbtn("Hepsi", True,  lambda: self._set_tip(""))
        self.btn_film  = self._fbtn("Film",  False, lambda: self._set_tip("Film"))
        self.btn_dizi  = self._fbtn("Dizi",  False, lambda: self._set_tip("Dizi"))
        layout.addWidget(self.btn_hepsi)
        layout.addWidget(self.btn_film)
        layout.addWidget(self.btn_dizi)
        layout.addStretch()
        return bar

    def _fbtn(self, text, active, cb):
        btn = QPushButton(text)
        btn.setStyleSheet(STYLE_FILTER_ACTIVE if active else STYLE_FILTER_INACTIVE)
        btn.clicked.connect(cb)
        return btn

    def _set_tip(self, tip):
        self._active_tip = tip
        self.btn_hepsi.setStyleSheet(STYLE_FILTER_ACTIVE if tip == ""     else STYLE_FILTER_INACTIVE)
        self.btn_film.setStyleSheet( STYLE_FILTER_ACTIVE if tip == "Film" else STYLE_FILTER_INACTIVE)
        self.btn_dizi.setStyleSheet( STYLE_FILTER_ACTIVE if tip == "Dizi" else STYLE_FILTER_INACTIVE)
        self._apply_filters()

    # ── Tablo ───────────────────────────────────────────────
    def _make_table(self):
        cols = ["Program Adı", "Tip", "Türler", "Yıl", "⭐ Puan", "👁 İzlenme",
                "Eklenme Tarihi", "İşlemler"]
        self.table = QTableWidget(0, len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background:{BG}; color:{TEXT}; gridline-color:{BORDER}; border:none; font-size:13px;
            }}
            QHeaderView::section {{
                background:{BG2}; color:{MUTED}; border:none;
                border-bottom:1px solid {BORDER}; padding:8px; font-size:12px; font-weight:bold;
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
        hh.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(7, 180)

        self.table.cellDoubleClicked.connect(self._open_detail)
        return self.table

    # ═══════════════════════════════════════════════════════════
    def _load_data(self):
        self.all_favorites = get_favoriler(self.user["kullanici_id"])
        self._apply_filters()

    def _apply_filters(self):
        tur  = self.cmb_tur.currentData()
        tip  = self._active_tip
        result = self.all_favorites

        if tur:
            result = [f for f in result
                      if f["turler"] and tur in [t.strip() for t in f["turler"].split(",")]]
        if tip:
            result = [f for f in result if f["program_tipi"] == tip]

        self.filtered_favorites = result
        self._fill_table()

    def _fill_table(self):
        self.table.setRowCount(0)
        for fav in self.filtered_favorites:
            row = self.table.rowCount()
            self.table.insertRow(row)

            puan_str  = f"{float(fav['ortalama_puan']):.1f}" if fav["ortalama_puan"] else "—"
            tarih_str = str(fav["ekleme_tarihi"])[:10] if fav["ekleme_tarihi"] else "—"

            self._item(row, 0, fav["program_adi"])
            self._item(row, 1, fav["program_tipi"],
                       "#4fc3f7" if fav["program_tipi"] == "Film" else "#a5d6a7")
            self._item(row, 2, fav["turler"] or "—")
            self._item(row, 3, str(fav["yayin_yili"]))
            self._item(row, 4, puan_str, GOLD)
            self._item(row, 5, str(fav["toplam_izlenme"]))
            self._item(row, 6, tarih_str, MUTED)
            self.table.setCellWidget(row, 7, self._action_buttons(fav))

        self.status_lbl.setText(
            f"{len(self.filtered_favorites)} favori  |  Toplam: {len(self.all_favorites)}"
        )

    def _item(self, row, col, text, color=None):
        item = QTableWidgetItem(str(text))
        item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        if color:
            item.setForeground(QColor(color))
        self.table.setItem(row, col, item)

    def _action_buttons(self, fav) -> QWidget:
        w = QWidget()
        w.setStyleSheet(f"background:{BG};")
        layout = QHBoxLayout(w)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(6)

        btn_cikar = QPushButton("🗑  Çıkar")
        btn_cikar.setStyleSheet(STYLE_BTN_GRAY)
        btn_cikar.clicked.connect(lambda _, f=fav: self._handle_cikar(f))
        layout.addWidget(btn_cikar)

        btn_izle = QPushButton("▶ İzle")
        btn_izle.setStyleSheet(STYLE_BTN_RED)
        btn_izle.clicked.connect(lambda _, f=fav: self._handle_izle(f))
        layout.addWidget(btn_izle)
        return w

    # ═══════════════════════════════════════════════════════════
    def _handle_cikar(self, fav):
        reply = QMessageBox.question(
            self, "Favoriden Çıkar",
            f"'{fav['program_adi']}' favorilerden çıkarılsın mı?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            toggle_favori(self.user["kullanici_id"], fav["program_id"])
            self._load_data()

    def _handle_izle(self, fav):
        if self.on_izle:
            self.on_izle(fav, False, None)

    def _open_detail(self, row, col):
        if col == 7:
            return
        if row >= len(self.filtered_favorites):
            return
        fav = self.filtered_favorites[row]
        from ui.detail_page import DetailPage
        self.detail_window = DetailPage(
            user=self.user,
            program_id=fav["program_id"],
            on_izle=lambda p, d, s: self._handle_izle(p),
            on_close_cb=self._load_data
        )
        self.detail_window.show()

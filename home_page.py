from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QComboBox,
    QVBoxLayout, QHBoxLayout, QFrame, QScrollArea,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QSizePolicy, QAbstractItemView,
    QSpinBox, QCheckBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor
from queries import get_all_programs, toggle_favori, get_watching_state
from auth import get_all_genres

# ── Renkler ─────────────────────────────────────────────────
BG         = "#141414"
BG2        = "#1e1e1e"
BG3        = "#2b2b2b"
RED        = "#E50914"
TEXT       = "#ffffff"
TEXT_MUTED = "#aaaaaa"
BORDER     = "#333333"

STYLE_BTN_RED = f"""
    QPushButton {{
        background:{RED}; color:white; border-radius:5px;
        font-size:11px; font-weight:bold; padding:4px 10px;
    }}
    QPushButton:hover {{ background:#f40612; }}
    QPushButton:pressed {{ background:#b2070f; }}
"""
STYLE_BTN_GRAY = f"""
    QPushButton {{
        background:{BG3}; color:{TEXT_MUTED}; border-radius:5px;
        font-size:11px; padding:4px 10px; border:1px solid {BORDER};
    }}
    QPushButton:hover {{ color:white; border-color:#666; }}
"""
STYLE_BTN_GOLD = """
    QPushButton {
        background:#b8860b; color:white; border-radius:5px;
        font-size:11px; font-weight:bold; padding:4px 10px;
    }
    QPushButton:hover { background:#daa520; }
"""
STYLE_FILTER_ACTIVE = f"""
    QPushButton {{
        background:{RED}; color:white; border-radius:14px;
        font-size:12px; font-weight:bold; padding:5px 16px;
    }}
"""
STYLE_FILTER_INACTIVE = f"""
    QPushButton {{
        background:{BG3}; color:{TEXT_MUTED}; border-radius:14px;
        font-size:12px; padding:5px 16px; border:1px solid {BORDER};
    }}
    QPushButton:hover {{ color:white; }}
"""


class HomePage(QWidget):
    def __init__(self, user: dict):
        super().__init__()
        self.user = user
        self.all_programs = []      # ham liste
        self.filtered_programs = [] # gösterilen liste
        self._sort_mode = "default" # default | puan | izlenme

        self.setWindowTitle(f"Netflix Platform — {user['ad']} {user['soyad']}")
        self.setMinimumSize(1100, 700)
        self.setStyleSheet(f"background-color:{BG}; color:{TEXT};")
        self._build_ui()
        self._load_data()

    # ═══════════════════════════════════════════════════════════
    # UI KURULUMU
    # ═══════════════════════════════════════════════════════════
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._make_topbar())
        root.addWidget(self._make_filter_bar())

        # İçerik tablosu
        self.table = self._make_table()
        root.addWidget(self.table)

        # Durum çubuğu
        self.status_lbl = QLabel("Yükleniyor...")
        self.status_lbl.setStyleSheet(f"color:{TEXT_MUTED}; font-size:12px; padding:6px 16px;")
        root.addWidget(self.status_lbl)

    # ── Top bar ─────────────────────────────────────────────
    def _make_topbar(self):
        bar = QFrame()
        bar.setStyleSheet(f"background:{BG2}; border-bottom:1px solid {BORDER};")
        bar.setFixedHeight(56)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(20, 0, 20, 0)

        logo = QLabel("N  Platform")
        logo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        logo.setStyleSheet(f"color:{RED};")
        layout.addWidget(logo)

        layout.addStretch()

        # Kullanıcı adı
        self.user_lbl = QLabel(f"👤  {self.user['ad']} {self.user['soyad']}")
        self.user_lbl.setStyleSheet(f"color:{TEXT_MUTED}; font-size:13px;")
        layout.addWidget(self.user_lbl)

        # Profil butonu
        btn_profil = QPushButton("⚙️  Profil")
        btn_profil.setStyleSheet(STYLE_BTN_GRAY)
        btn_profil.clicked.connect(self._open_profil)
        layout.addWidget(btn_profil)

        # Geçmiş butonu
        btn_gecmis = QPushButton("📋  İzleme Geçmişi")
        btn_gecmis.setStyleSheet(STYLE_BTN_GRAY)
        btn_gecmis.clicked.connect(self._open_gecmis)
        layout.addWidget(btn_gecmis)

        # Favoriler butonu
        btn_favori = QPushButton("❤️  Favoriler")
        btn_favori.setStyleSheet(STYLE_BTN_GRAY)
        btn_favori.clicked.connect(self._open_favoriler)
        layout.addWidget(btn_favori)

        # Öneri butonu
        btn_oneri = QPushButton("💡  Öneriler")
        btn_oneri.setStyleSheet(STYLE_BTN_GRAY)
        btn_oneri.clicked.connect(self._open_oneri)
        layout.addWidget(btn_oneri)

        # Çıkış
        btn_cikis = QPushButton("Çıkış")
        btn_cikis.setStyleSheet(STYLE_BTN_RED)
        btn_cikis.clicked.connect(self._logout)
        layout.addWidget(btn_cikis)

        return bar

    # ── Filtre çubuğu ───────────────────────────────────────
    def _make_filter_bar(self):
        bar = QFrame()
        bar.setStyleSheet(f"background:{BG2}; border-bottom:1px solid {BORDER};")
        outer = QVBoxLayout(bar)
        outer.setContentsMargins(16, 6, 16, 6)
        outer.setSpacing(6)

        # ── Satır 1: Arama + Tür + Tip filtreleri ──
        row1 = QHBoxLayout()
        row1.setSpacing(10)

        # Arama kutusu
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍  İçerik adına göre ara...")
        self.search_input.setFixedWidth(240)
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                background:{BG3}; color:white; border:1px solid {BORDER};
                border-radius:16px; padding:0 14px; font-size:13px; min-height:32px;
            }}
            QLineEdit:focus {{ border-color:{RED}; }}
        """)
        self.search_input.textChanged.connect(self._apply_filters)
        row1.addWidget(self.search_input)

        # Tür filtresi
        self.cmb_tur = QComboBox()
        self.cmb_tur.setFixedWidth(150)
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
        self.cmb_tur.addItem("Tüm Türler", 0)
        for g in get_all_genres():
            self.cmb_tur.addItem(g["tur_adi"], g["tur_id"])
        self.cmb_tur.currentIndexChanged.connect(self._apply_filters)
        row1.addWidget(self.cmb_tur)

        row1.addSpacing(6)

        # Tip filtre butonları
        self.btn_hepsi = self._filter_btn("Hepsi",  True,  lambda: self._set_tip(""))
        self.btn_film  = self._filter_btn("Film",   False, lambda: self._set_tip("Film"))
        self.btn_dizi  = self._filter_btn("Dizi",   False, lambda: self._set_tip("Dizi"))
        row1.addWidget(self.btn_hepsi)
        row1.addWidget(self.btn_film)
        row1.addWidget(self.btn_dizi)
        self._active_tip = ""

        row1.addStretch()

        # Sıralama butonları
        lbl = QLabel("Sırala:")
        lbl.setStyleSheet(f"color:{TEXT_MUTED}; font-size:12px;")
        row1.addWidget(lbl)

        self.btn_sort_default = self._sort_btn("Varsayılan", "default")
        self.btn_sort_puan    = self._sort_btn("⭐ En Yüksek Puan", "puan")
        self.btn_sort_izlenme = self._sort_btn("👁 En Çok İzlenen", "izlenme")
        row1.addWidget(self.btn_sort_default)
        row1.addWidget(self.btn_sort_puan)
        row1.addWidget(self.btn_sort_izlenme)

        outer.addLayout(row1)

        # ── Satır 2: Yayın yılı + Min puan + Sadece favoriler ──
        row2 = QHBoxLayout()
        row2.setSpacing(14)

        spin_style = f"""
            QSpinBox {{
                background:{BG3}; color:white; border:1px solid {BORDER};
                border-radius:6px; padding:0 8px; font-size:12px; min-height:28px; min-width:80px;
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                background:{BG3}; border:none; width:16px;
            }}
            QSpinBox:focus {{ border-color:{RED}; }}
        """

        # Yayın yılı
        lbl_yil = QLabel("📅 Yayın Yılı:")
        lbl_yil.setStyleSheet(f"color:{TEXT_MUTED}; font-size:12px;")
        row2.addWidget(lbl_yil)

        self.spin_yil = QSpinBox()
        self.spin_yil.setRange(0, 2026)
        self.spin_yil.setValue(0)
        self.spin_yil.setSpecialValueText("Tümü")
        self.spin_yil.setStyleSheet(spin_style)
        self.spin_yil.valueChanged.connect(self._apply_filters)
        row2.addWidget(self.spin_yil)

        row2.addSpacing(8)

        # Min puan
        lbl_puan = QLabel("⭐ Min Puan:")
        lbl_puan.setStyleSheet(f"color:{TEXT_MUTED}; font-size:12px;")
        row2.addWidget(lbl_puan)

        self.spin_min_puan = QSpinBox()
        self.spin_min_puan.setRange(0, 10)
        self.spin_min_puan.setValue(0)
        self.spin_min_puan.setSpecialValueText("Tümü")
        self.spin_min_puan.setStyleSheet(spin_style)
        self.spin_min_puan.valueChanged.connect(self._apply_filters)
        row2.addWidget(self.spin_min_puan)

        row2.addSpacing(8)

        # Sadece favoriler checkbox
        self.chk_favori = QCheckBox("❤️ Sadece Favoriler")
        self.chk_favori.setStyleSheet(f"""
            QCheckBox {{ color:{TEXT_MUTED}; font-size:12px; }}
            QCheckBox:hover {{ color:white; }}
            QCheckBox::indicator {{
                width:16px; height:16px; border-radius:3px;
                border:1px solid {BORDER}; background:{BG3};
            }}
            QCheckBox::indicator:checked {{ background:{RED}; border-color:{RED}; }}
        """)
        self.chk_favori.stateChanged.connect(self._apply_filters)
        row2.addWidget(self.chk_favori)

        # Filtreleri sıfırla
        btn_reset = QPushButton("🔄 Sıfırla")
        btn_reset.setStyleSheet(f"""
            QPushButton {{ background:{BG3}; color:{TEXT_MUTED}; border-radius:12px;
                font-size:11px; padding:4px 12px; border:1px solid {BORDER}; }}
            QPushButton:hover {{ color:white; border-color:#666; }}
        """)
        btn_reset.clicked.connect(self._reset_filters)
        row2.addWidget(btn_reset)

        row2.addStretch()

        # Sonuç sayacı
        self.result_lbl = QLabel("")
        self.result_lbl.setStyleSheet(f"color:{TEXT_MUTED}; font-size:11px;")
        row2.addWidget(self.result_lbl)

        outer.addLayout(row2)

        return bar

    def _filter_btn(self, text, active, callback):
        btn = QPushButton(text)
        btn.setStyleSheet(STYLE_FILTER_ACTIVE if active else STYLE_FILTER_INACTIVE)
        btn.clicked.connect(callback)
        return btn

    def _sort_btn(self, text, mode):
        btn = QPushButton(text)
        btn.setStyleSheet(STYLE_FILTER_ACTIVE if mode == "default" else STYLE_FILTER_INACTIVE)
        btn.clicked.connect(lambda: self._set_sort(mode))
        return btn

    # ── Tablo ───────────────────────────────────────────────
    def _make_table(self):
        cols = ["Program Adı", "Tip", "Türler", "Bölüm", "Süre (dk)", "⭐ Puan", "👁 İzlenme", "İşlemler"]
        table = QTableWidget(0, len(cols))
        table.setHorizontalHeaderLabels(cols)
        table.setStyleSheet(f"""
            QTableWidget {{
                background:{BG}; color:{TEXT};
                gridline-color:{BORDER}; border:none;
                font-size:13px;
            }}
            QHeaderView::section {{
                background:{BG2}; color:{TEXT_MUTED};
                border:none; border-bottom:1px solid {BORDER};
                padding:8px; font-size:12px; font-weight:bold;
            }}
            QTableWidget::item {{ padding:6px 8px; }}
            QTableWidget::item:selected {{ background:#2a2a2a; color:white; }}
        """)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setAlternatingRowColors(True)
        table.setAlternatingRowColors(False)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(True)

        hh = table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)
        table.setColumnWidth(7, 260)
        table.verticalHeader().setDefaultSectionSize(44)

        # Satıra tıklayınca detay sayfası aç
        table.cellDoubleClicked.connect(self._open_detail)

        return table

    # ═══════════════════════════════════════════════════════════
    # VERİ YÖNETİMİ
    # ═══════════════════════════════════════════════════════════
    def _load_data(self):
        self.all_programs = get_all_programs(self.user["kullanici_id"])
        self._apply_filters()

    def _apply_filters(self):
        text    = self.search_input.text().strip().lower()
        tur_id  = self.cmb_tur.currentData()
        tip     = self._active_tip
        yil     = self.spin_yil.value()
        min_puan = self.spin_min_puan.value()
        sadece_favori = self.chk_favori.isChecked()

        result = self.all_programs

        if text:
            result = [p for p in result if text in p["program_adi"].lower()]

        if tur_id:
            result = [p for p in result
                      if p["turler"] and
                      any(t.strip() == self.cmb_tur.currentText()
                          for t in p["turler"].split(","))]

        if tip:
            result = [p for p in result if p["program_tipi"] == tip]

        if yil > 0:
            result = [p for p in result if str(p.get("yayin_yili", "")) == str(yil)]

        if min_puan > 0:
            result = [p for p in result if float(p["ortalama_puan"] or 0) >= min_puan]

        if sadece_favori:
            result = [p for p in result if p.get("favori")]

        if self._sort_mode == "puan":
            result = sorted(result, key=lambda x: float(x["ortalama_puan"] or 0), reverse=True)
        elif self._sort_mode == "izlenme":
            result = sorted(result, key=lambda x: int(x["toplam_izlenme"] or 0), reverse=True)

        self.filtered_programs = result
        self.result_lbl.setText(f"{len(result)} içerik")
        self._fill_table()

    def _reset_filters(self):
        self.search_input.clear()
        self.cmb_tur.setCurrentIndex(0)
        self._set_tip("")
        self.spin_yil.setValue(0)
        self.spin_min_puan.setValue(0)
        self.chk_favori.setChecked(False)
        self._set_sort("default")

    def _set_tip(self, tip: str):
        self._active_tip = tip
        self.btn_hepsi.setStyleSheet(STYLE_FILTER_ACTIVE if tip == ""      else STYLE_FILTER_INACTIVE)
        self.btn_film.setStyleSheet( STYLE_FILTER_ACTIVE if tip == "Film"  else STYLE_FILTER_INACTIVE)
        self.btn_dizi.setStyleSheet( STYLE_FILTER_ACTIVE if tip == "Dizi"  else STYLE_FILTER_INACTIVE)
        self._apply_filters()

    def _set_sort(self, mode: str):
        self._sort_mode = mode
        self.btn_sort_default.setStyleSheet(STYLE_FILTER_ACTIVE if mode == "default"  else STYLE_FILTER_INACTIVE)
        self.btn_sort_puan.setStyleSheet(   STYLE_FILTER_ACTIVE if mode == "puan"     else STYLE_FILTER_INACTIVE)
        self.btn_sort_izlenme.setStyleSheet(STYLE_FILTER_ACTIVE if mode == "izlenme"  else STYLE_FILTER_INACTIVE)
        self._apply_filters()

    # ═══════════════════════════════════════════════════════════
    # TABLO DOLDURMA
    # ═══════════════════════════════════════════════════════════
    def _fill_table(self):
        self.table.setRowCount(0)
        for prog in self.filtered_programs:
            row = self.table.rowCount()
            self.table.insertRow(row)

            puan_str    = f"{float(prog['ortalama_puan']):.1f}" if prog['ortalama_puan'] else "—"
            sure_str    = str(prog["bolum_uzunluk_dk"]) if prog["bolum_uzunluk_dk"] else "—"

            self._set_item(row, 0, prog["program_adi"])
            self._set_item(row, 1, prog["program_tipi"],
                           color="#4fc3f7" if prog["program_tipi"] == "Film" else "#a5d6a7")
            self._set_item(row, 2, prog["turler"] or "—")
            self._set_item(row, 3, str(prog["bolum_sayisi"]))
            self._set_item(row, 4, sure_str)
            self._set_item(row, 5, puan_str,
                           color="#ffd54f" if prog["ortalama_puan"] else TEXT_MUTED)
            self._set_item(row, 6, str(prog["toplam_izlenme"]))

            # İşlem butonları
            self.table.setCellWidget(row, 7, self._make_action_buttons(prog, row))

        self.status_lbl.setText(
            f"{len(self.filtered_programs)} içerik listeleniyor  |  "
            f"Toplam: {len(self.all_programs)}"
        )

    def _set_item(self, row, col, text, color=None):
        item = QTableWidgetItem(str(text))
        item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        if color:
            item.setForeground(QColor(color))
        self.table.setItem(row, col, item)

    def _make_action_buttons(self, prog, row) -> QWidget:
        w = QWidget()
        w.setStyleSheet(f"background:{BG};")
        layout = QHBoxLayout(w)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(4)

        # Favori butonu
        is_fav = bool(prog["favori"])
        btn_fav = QPushButton("❤️" if is_fav else "🤍")
        btn_fav.setFixedWidth(36)
        btn_fav.setStyleSheet(STYLE_BTN_GRAY)
        btn_fav.setToolTip("Favoriye ekle / çıkar")
        btn_fav.clicked.connect(lambda _, p=prog, b=btn_fav: self._handle_favori(p, b))
        layout.addWidget(btn_fav)

        # İzle butonu — duruma göre metni belirle
        is_complete = bool(prog.get("tamamlandi"))
        
        # Tamamlanmış mı kontrol et
        if is_complete:
            btn_text = "✅ İzlendi Tamamlandı"
        else:
            # Kaldığı yer var mı kontrol et
            state = get_watching_state(self.user["kullanici_id"], prog["program_id"])
            if state and state["son_izleme_dk"] > 0 and not state["tamamlandi"]:
                btn_text = "▶ Devam Et"
            else:
                btn_text = "▶ İzle"
        
        btn_izle = QPushButton(btn_text)
        btn_izle.setStyleSheet(STYLE_BTN_RED)
        btn_izle.clicked.connect(lambda _, p=prog: self._handle_izle(p))
        layout.addWidget(btn_izle)

        # Puan ver butonu
        btn_puan = QPushButton("⭐ Puan")
        btn_puan.setStyleSheet(STYLE_BTN_GOLD)
        btn_puan.setEnabled(bool(prog["izlendi"]))
        btn_puan.setToolTip("Puan vermek için önce izlemelisiniz.")
        btn_puan.clicked.connect(lambda _, p=prog: self._handle_puan(p))
        layout.addWidget(btn_puan)

        return w

    # ═══════════════════════════════════════════════════════════
    # AKSIYONLAR
    # ═══════════════════════════════════════════════════════════
    def _handle_favori(self, prog, btn):
        new_state = toggle_favori(self.user["kullanici_id"], prog["program_id"])
        prog["favori"] = 1 if new_state else 0
        btn.setText("❤️" if new_state else "🤍")

    def _handle_izle(self, prog):
        state = get_watching_state(self.user["kullanici_id"], prog["program_id"])
        if state and not state["tamamlandi"] and state["son_izleme_dk"] > 0:
            bolum = state["son_bolum_no"]
            dk    = state["son_izleme_dk"]
            reply = QMessageBox.question(
                self, "Kaldığın Yerden Devam Et",
                f"{prog['program_adi']} — {bolum}. bölüm {dk}. dakikadan devam etmek ister misiniz?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            devam = reply == QMessageBox.StandardButton.Yes
        else:
            devam = False

        from ui.watch_page import WatchPage
        self.watch_window = WatchPage(
            user=self.user,
            program=prog,
            devam=devam,
            devam_state=state,
            on_close=self._on_watch_closed
        )
        self.watch_window.show()

    def _handle_puan(self, prog):
        from ui.rating_dialog import RatingDialog
        dlg = RatingDialog(
            user=self.user,
            program=prog,
            parent=self
        )
        dlg.exec()
        self._load_data()

    def _on_watch_closed(self):
        self._load_data()

    def _open_detail(self, row, col):
        if col == 7:   # İşlemler sütununa çift tıklama → yok say
            return
        if row >= len(self.filtered_programs):
            return
        prog = self.filtered_programs[row]
        from ui.detail_page import DetailPage
        self.detail_window = DetailPage(
            user=self.user,
            program_id=prog["program_id"],
            on_izle=self._detail_on_izle,
            on_close_cb=self._load_data
        )
        self.detail_window.show()

    def _detail_on_izle(self, prog, devam, devam_state):
        from ui.watch_page import WatchPage
        self.watch_window = WatchPage(
            user=self.user,
            program=prog,
            devam=devam,
            devam_state=devam_state,
            on_close=self._on_watch_closed
        )
        self.watch_window.show()

    def _open_profil(self):
        from ui.profile_page import ProfilePage
        self.profile_window = ProfilePage(
            user=self.user,
            on_user_update=self._on_user_update
        )
        self.profile_window.show()

    def _on_user_update(self, updated_user):
        self.user = updated_user
        self.user_lbl.setText(f"👤  {updated_user['ad']} {updated_user['soyad']}")

    def _open_gecmis(self):
        from ui.history_page import HistoryPage
        self.history_window = HistoryPage(user=self.user)
        self.history_window.show()

    def _open_favoriler(self):
        from ui.favorites_page import FavoritesPage
        self.favorites_window = FavoritesPage(
            user=self.user,
            on_izle=self._detail_on_izle
        )
        self.favorites_window.show()

    def _open_oneri(self):
        from ui.user_recommendation_page import UserRecommendationPage
        self.oneri_window = UserRecommendationPage(
            user=self.user,
            on_izle=self._detail_on_izle
        )
        self.oneri_window.show()

    def _logout(self):
        reply = QMessageBox.question(
            self, "Çıkış", "Çıkış yapmak istediğinizden emin misiniz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            from ui.login_page import LoginPage
            self.login_window = LoginPage(on_login_success=self._on_relogin)
            self.login_window.show()
            self.close()

    def _on_relogin(self, user):
        self.close()
        new_home = HomePage(user)
        new_home.show()

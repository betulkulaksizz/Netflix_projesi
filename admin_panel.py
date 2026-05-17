from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QTabWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QMessageBox, QDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from queries_admin import (
    admin_get_programs, admin_add_program, admin_update_program, admin_delete_program,
    admin_get_turler, admin_add_tur, admin_update_tur, admin_delete_tur,
    admin_get_kullanicilar, admin_get_kullanici_detay,
    admin_get_kullanici_gecmis, admin_toggle_aktif
)

BG     = "#141414"
BG2    = "#1e1e1e"
BG3    = "#2b2b2b"
RED    = "#E50914"
TEXT   = "#ffffff"
MUTED  = "#aaaaaa"
GOLD   = "#ffd54f"
GREEN  = "#a5d6a7"
BORDER = "#333333"

STYLE_BTN_RED = f"""
    QPushButton {{
        background:{RED}; color:white; border-radius:5px;
        font-size:12px; font-weight:bold; padding:5px 14px;
    }}
    QPushButton:hover  {{ background:#f40612; }}
    QPushButton:pressed{{ background:#b2070f; }}
"""
STYLE_BTN_GRAY = f"""
    QPushButton {{
        background:{BG3}; color:{TEXT}; border:1px solid {BORDER};
        border-radius:5px; font-size:12px; padding:5px 14px;
    }}
    QPushButton:hover {{ border-color:#666; }}
"""
STYLE_BTN_ORANGE = """
    QPushButton {
        background:#e65100; color:white; border-radius:5px;
        font-size:12px; font-weight:bold; padding:5px 14px;
    }
    QPushButton:hover { background:#f57c00; }
"""
STYLE_BTN_GREEN = """
    QPushButton {
        background:#2e7d32; color:white; border-radius:5px;
        font-size:12px; font-weight:bold; padding:5px 14px;
    }
    QPushButton:hover { background:#388e3c; }
"""
TABLE_STYLE = f"""
    QTableWidget {{
        background:{BG}; color:{TEXT}; gridline-color:{BORDER}; border:none; font-size:13px;
    }}
    QHeaderView::section {{
        background:{BG2}; color:{MUTED}; border:none;
        border-bottom:1px solid {BORDER}; padding:8px; font-size:12px; font-weight:bold;
    }}
    QTableWidget::item {{ padding:6px 8px; }}
    QTableWidget::item:selected {{ background:#2a2a2a; color:white; }}
"""


def _tbl(cols: list) -> QTableWidget:
    t = QTableWidget(0, len(cols))
    t.setHorizontalHeaderLabels(cols)
    t.setStyleSheet(TABLE_STYLE)
    t.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    t.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    t.verticalHeader().setVisible(False)
    t.verticalHeader().setDefaultSectionSize(44)
    t.horizontalHeader().setStretchLastSection(True)
    return t


def _item(text, color=None) -> QTableWidgetItem:
    it = QTableWidgetItem(str(text))
    it.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
    if color:
        it.setForeground(QColor(color))
    return it


def _action_widget(bg, *buttons) -> QWidget:
    w = QWidget()
    w.setStyleSheet(f"background:{bg};")
    layout = QHBoxLayout(w)
    layout.setContentsMargins(4, 2, 4, 2)
    layout.setSpacing(6)
    for btn in buttons:
        layout.addWidget(btn)
    return w


class AdminPanel(QWidget):
    def __init__(self, user: dict):
        super().__init__()
        self.user = user
        self.setWindowTitle("⚙️  Yönetici Paneli")
        self.setMinimumSize(1100, 700)
        self.setStyleSheet(f"background:{BG}; color:{TEXT};")
        self._build_ui()

    # ═══════════════════════════════════════════════════════════
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Top bar ─────────────────────────────────────────
        bar = QFrame()
        bar.setStyleSheet(f"background:{BG2}; border-bottom:1px solid {BORDER};")
        bar.setFixedHeight(56)
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(20, 0, 20, 0)
        logo = QLabel("N  Yönetici Paneli")
        logo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        logo.setStyleSheet(f"color:{RED};")
        bl.addWidget(logo)
        bl.addStretch()
        user_lbl = QLabel(f"👤  {self.user['ad']} {self.user['soyad']}")
        user_lbl.setStyleSheet(f"color:{MUTED}; font-size:13px;")
        bl.addWidget(user_lbl)
        btn_cikis = QPushButton("Çıkış")
        btn_cikis.setStyleSheet(STYLE_BTN_RED)
        btn_cikis.clicked.connect(self._logout)
        bl.addWidget(btn_cikis)
        root.addWidget(bar)

        # ── Sekmeler ────────────────────────────────────────
        tabs = QTabWidget()
        tabs.setStyleSheet(f"""
            QTabWidget::pane {{ border:none; background:{BG}; }}
            QTabBar::tab {{
                background:{BG2}; color:{MUTED}; padding:11px 22px;
                border:none; font-size:13px;
            }}
            QTabBar::tab:selected {{ color:white; border-bottom:2px solid {RED}; }}
            QTabBar::tab:hover {{ color:white; }}
        """)
        tabs.addTab(self._tab_programs(), "🎬  İçerik Yönetimi")
        tabs.addTab(self._tab_genres(),   "🏷️  Tür Yönetimi")
        tabs.addTab(self._tab_users(),    "👥  Kullanıcı Yönetimi")
        root.addWidget(tabs)

    # ═══════════════════════════════════════════════════════════
    # TAB 1 — İÇERİK YÖNETİMİ
    # ═══════════════════════════════════════════════════════════
    def _tab_programs(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet(f"background:{BG};")
        layout = QVBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Toolbar
        tb = QFrame()
        tb.setStyleSheet(f"background:{BG2}; border-bottom:1px solid {BORDER};")
        tb.setFixedHeight(48)
        tbl = QHBoxLayout(tb)
        tbl.setContentsMargins(16, 0, 16, 0)
        btn_ekle = QPushButton("➕  Yeni Program")
        btn_ekle.setStyleSheet(STYLE_BTN_RED)
        btn_ekle.clicked.connect(self._add_program)
        tbl.addWidget(btn_ekle)
        tbl.addStretch()
        btn_yenile = QPushButton("🔄  Yenile")
        btn_yenile.setStyleSheet(STYLE_BTN_GRAY)
        btn_yenile.clicked.connect(self._load_programs)
        tbl.addWidget(btn_yenile)
        layout.addWidget(tb)

        # Tablo
        cols = ["ID", "Program Adı", "Tip", "Yıl", "Bölüm", "Süre(dk)",
                "⭐ Puan", "👁 İzlenme", "Türler", "İşlemler"]
        self.tbl_programs = _tbl(cols)
        self.tbl_programs.setColumnWidth(9, 200)
        hh = self.tbl_programs.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(8, QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(9, QHeaderView.ResizeMode.Fixed)
        layout.addWidget(self.tbl_programs)

        self.lbl_prog_status = QLabel("")
        self.lbl_prog_status.setStyleSheet(f"color:{MUTED}; font-size:12px; padding:5px 16px;")
        layout.addWidget(self.lbl_prog_status)

        self._load_programs()
        return w

    def _load_programs(self):
        self.programs = admin_get_programs()
        self.tbl_programs.setRowCount(0)
        for p in self.programs:
            r = self.tbl_programs.rowCount()
            self.tbl_programs.insertRow(r)
            puan = f"{float(p['ortalama_puan']):.1f}" if p["ortalama_puan"] else "—"
            self.tbl_programs.setItem(r, 0, _item(p["program_id"], MUTED))
            self.tbl_programs.setItem(r, 1, _item(p["program_adi"]))
            self.tbl_programs.setItem(r, 2, _item(p["program_tipi"],
                "#4fc3f7" if p["program_tipi"] == "Film" else "#a5d6a7"))
            self.tbl_programs.setItem(r, 3, _item(p["yayin_yili"]))
            self.tbl_programs.setItem(r, 4, _item(p["bolum_sayisi"]))
            self.tbl_programs.setItem(r, 5, _item(p["bolum_uzunluk_dk"] or "—"))
            self.tbl_programs.setItem(r, 6, _item(puan, GOLD))
            self.tbl_programs.setItem(r, 7, _item(p["toplam_izlenme"]))
            self.tbl_programs.setItem(r, 8, _item(p["turler"] or "—"))

            btn_guncelle = QPushButton("✏️")
            btn_guncelle.setToolTip("Güncelle")
            btn_guncelle.setStyleSheet(STYLE_BTN_ORANGE)
            btn_guncelle.clicked.connect(lambda _, prog=p: self._edit_program(prog))

            btn_sil = QPushButton("🗑")
            btn_sil.setToolTip("Sil")
            btn_sil.setStyleSheet(STYLE_BTN_GRAY)
            btn_sil.clicked.connect(lambda _, prog=p: self._delete_program(prog))

            self.tbl_programs.setCellWidget(r, 9, _action_widget(BG, btn_guncelle, btn_sil))

        self.lbl_prog_status.setText(f"{len(self.programs)} program")

    def _add_program(self):
        from ui.admin_dialogs import ProgramDialog
        dlg = ProgramDialog(parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            d = dlg.get_data()
            ok, err = admin_add_program(
                d["program_adi"], d["aciklama"], d["program_tipi"],
                d["yayin_yili"], d["bolum_sayisi"], d["bolum_uzunluk_dk"], d["tur_ids"]
            )
            if ok:
                QMessageBox.information(self, "Başarılı", "Program eklendi.")
                self._load_programs()
            else:
                QMessageBox.critical(self, "Hata", err)

    def _edit_program(self, prog):
        from ui.admin_dialogs import ProgramDialog
        dlg = ProgramDialog(parent=self, program=prog)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            d = dlg.get_data()
            ok, err = admin_update_program(
                prog["program_id"], d["program_adi"], d["aciklama"],
                d["program_tipi"], d["yayin_yili"],
                d["bolum_sayisi"], d["bolum_uzunluk_dk"], d["tur_ids"]
            )
            if ok:
                QMessageBox.information(self, "Başarılı", "Program güncellendi.")
                self._load_programs()
            else:
                QMessageBox.critical(self, "Hata", err)

    def _delete_program(self, prog):
        reply = QMessageBox.question(
            self, "Sil", f"'{prog['program_adi']}' silinsin mi?\nBu işlem geri alınamaz.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            ok, err = admin_delete_program(prog["program_id"])
            if ok:
                self._load_programs()
            else:
                QMessageBox.critical(self, "Hata", err)

    # ═══════════════════════════════════════════════════════════
    # TAB 2 — TÜR YÖNETİMİ
    # ═══════════════════════════════════════════════════════════
    def _tab_genres(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet(f"background:{BG};")
        layout = QVBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        tb = QFrame()
        tb.setStyleSheet(f"background:{BG2}; border-bottom:1px solid {BORDER};")
        tb.setFixedHeight(48)
        tbl = QHBoxLayout(tb)
        tbl.setContentsMargins(16, 0, 16, 0)
        btn_ekle = QPushButton("➕  Yeni Tür")
        btn_ekle.setStyleSheet(STYLE_BTN_RED)
        btn_ekle.clicked.connect(self._add_tur)
        tbl.addWidget(btn_ekle)
        tbl.addStretch()
        btn_yenile = QPushButton("🔄  Yenile")
        btn_yenile.setStyleSheet(STYLE_BTN_GRAY)
        btn_yenile.clicked.connect(self._load_genres)
        tbl.addWidget(btn_yenile)
        layout.addWidget(tb)

        cols = ["ID", "Tür Adı", "Bağlı Program Sayısı", "İşlemler"]
        self.tbl_genres = _tbl(cols)
        hh = self.tbl_genres.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.tbl_genres.setColumnWidth(3, 180)
        layout.addWidget(self.tbl_genres)

        self._load_genres()
        return w

    def _load_genres(self):
        self.genres = admin_get_turler()
        self.tbl_genres.setRowCount(0)
        for t in self.genres:
            r = self.tbl_genres.rowCount()
            self.tbl_genres.insertRow(r)
            self.tbl_genres.setItem(r, 0, _item(t["tur_id"], MUTED))
            self.tbl_genres.setItem(r, 1, _item(t["tur_adi"]))
            self.tbl_genres.setItem(r, 2, _item(t["program_sayisi"],
                                                 GREEN if t["program_sayisi"] > 0 else MUTED))

            btn_guncelle = QPushButton("✏️")
            btn_guncelle.setStyleSheet(STYLE_BTN_ORANGE)
            btn_guncelle.clicked.connect(lambda _, tur=t: self._edit_tur(tur))

            btn_sil = QPushButton("🗑")
            btn_sil.setStyleSheet(STYLE_BTN_GRAY)
            btn_sil.clicked.connect(lambda _, tur=t: self._delete_tur(tur))

            self.tbl_genres.setCellWidget(r, 3, _action_widget(BG, btn_guncelle, btn_sil))

    def _add_tur(self):
        from ui.admin_dialogs import TurDialog
        dlg = TurDialog(parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            ok, err = admin_add_tur(dlg.get_adi())
            if ok:
                QMessageBox.information(self, "Başarılı", "Tür eklendi.")
                self._load_genres()
            else:
                QMessageBox.critical(self, "Hata", err)

    def _edit_tur(self, tur):
        from ui.admin_dialogs import TurDialog
        dlg = TurDialog(parent=self, tur=tur)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            ok, err = admin_update_tur(tur["tur_id"], dlg.get_adi())
            if ok:
                self._load_genres()
            else:
                QMessageBox.critical(self, "Hata", err)

    def _delete_tur(self, tur):
        reply = QMessageBox.question(
            self, "Sil", f"'{tur['tur_adi']}' türü silinsin mi?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            ok, err = admin_delete_tur(tur["tur_id"])
            if ok:
                self._load_genres()
            else:
                QMessageBox.warning(self, "Silinemedi", err)

    # ═══════════════════════════════════════════════════════════
    # TAB 3 — KULLANICI YÖNETİMİ
    # ═══════════════════════════════════════════════════════════
    def _tab_users(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet(f"background:{BG};")
        layout = QVBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        tb = QFrame()
        tb.setStyleSheet(f"background:{BG2}; border-bottom:1px solid {BORDER};")
        tb.setFixedHeight(48)
        tbl = QHBoxLayout(tb)
        tbl.setContentsMargins(16, 0, 16, 0)
        tbl.addStretch()
        btn_yenile = QPushButton("🔄  Yenile")
        btn_yenile.setStyleSheet(STYLE_BTN_GRAY)
        btn_yenile.clicked.connect(self._load_users)
        tbl.addWidget(btn_yenile)
        layout.addWidget(tb)

        cols = ["ID", "Ad Soyad", "E-mail", "Ülke", "Rol",
                "İzlenen", "Toplam Süre", "Durum", "İşlemler"]
        self.tbl_users = _tbl(cols)
        hh = self.tbl_users.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(8, QHeaderView.ResizeMode.Fixed)
        self.tbl_users.setColumnWidth(8, 220)
        layout.addWidget(self.tbl_users)

        self.lbl_user_status = QLabel("")
        self.lbl_user_status.setStyleSheet(f"color:{MUTED}; font-size:12px; padding:5px 16px;")
        layout.addWidget(self.lbl_user_status)

        self._load_users()
        return w

    def _load_users(self):
        self.users = admin_get_kullanicilar()
        self.tbl_users.setRowCount(0)
        aktif_sayisi = 0
        for u in self.users:
            r = self.tbl_users.rowCount()
            self.tbl_users.insertRow(r)
            sure_str = f"{u['toplam_sure_dk']} dk ({u['toplam_sure_dk']//60} sa)"
            durum    = "✅ Aktif" if u["aktif"] else "🚫 Pasif"
            if u["aktif"]:
                aktif_sayisi += 1

            self.tbl_users.setItem(r, 0, _item(u["kullanici_id"], MUTED))
            self.tbl_users.setItem(r, 1, _item(f"{u['ad']} {u['soyad']}"))
            self.tbl_users.setItem(r, 2, _item(u["email"], MUTED))
            self.tbl_users.setItem(r, 3, _item(u["ulke"] or "—"))
            self.tbl_users.setItem(r, 4, _item(u["rol_adi"],
                RED if u["rol_adi"] == "yonetici" else MUTED))
            self.tbl_users.setItem(r, 5, _item(u["izlenen_icerik"]))
            self.tbl_users.setItem(r, 6, _item(sure_str))
            self.tbl_users.setItem(r, 7, _item(durum,
                GREEN if u["aktif"] else "#ff7043"))

            btn_detay = QPushButton("🔍 Detay")
            btn_detay.setStyleSheet(STYLE_BTN_GRAY)
            btn_detay.clicked.connect(lambda _, usr=u: self._show_user_detail(usr))

            btn_toggle = QPushButton("🚫 Pasif" if u["aktif"] else "✅ Aktif")
            btn_toggle.setStyleSheet(STYLE_BTN_ORANGE if u["aktif"] else STYLE_BTN_GREEN)
            btn_toggle.clicked.connect(lambda _, usr=u: self._toggle_user(usr))

            self.tbl_users.setCellWidget(r, 8, _action_widget(BG, btn_detay, btn_toggle))

        self.lbl_user_status.setText(
            f"Toplam: {len(self.users)} kullanıcı  |  Aktif: {aktif_sayisi}  |  "
            f"Pasif: {len(self.users) - aktif_sayisi}"
        )

    def _toggle_user(self, usr):
        yeni_durum = not bool(usr["aktif"])
        durum_str  = "aktif" if yeni_durum else "pasif"
        reply = QMessageBox.question(
            self, "Durum Değiştir",
            f"{usr['ad']} {usr['soyad']} kullanıcısı {durum_str} yapılsın mı?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            ok, err = admin_toggle_aktif(usr["kullanici_id"], yeni_durum)
            if ok:
                self._load_users()
            else:
                QMessageBox.critical(self, "Hata", err)

    def _show_user_detail(self, usr):
        from ui.admin_user_detail import UserDetailDialog
        dlg = UserDetailDialog(parent=self, kullanici_id=usr["kullanici_id"])
        dlg.exec()

    # ═══════════════════════════════════════════════════════════
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
        if user["rol_id"] == 2:
            w = AdminPanel(user)
        else:
            from ui.home_page import HomePage
            w = HomePage(user)
        w.show()

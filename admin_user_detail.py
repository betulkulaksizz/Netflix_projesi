from PyQt6.QtWidgets import (
    QDialog, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QTabWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from queries_admin import admin_get_kullanici_detay, admin_get_kullanici_gecmis

BG     = "#141414"
BG2    = "#1e1e1e"
BG3    = "#2b2b2b"
RED    = "#E50914"
TEXT   = "#ffffff"
MUTED  = "#aaaaaa"
GOLD   = "#ffd54f"
GREEN  = "#a5d6a7"
BORDER = "#333333"

TABLE_STYLE = f"""
    QTableWidget {{
        background:{BG}; color:{TEXT}; gridline-color:{BORDER}; border:none; font-size:12px;
    }}
    QHeaderView::section {{
        background:{BG2}; color:{MUTED}; border:none;
        border-bottom:1px solid {BORDER}; padding:6px; font-size:11px; font-weight:bold;
    }}
    QTableWidget::item {{ padding:5px 8px; }}
"""


def _lbl(text, size=12, bold=False, color=TEXT) -> QLabel:
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


class UserDetailDialog(QDialog):
    def __init__(self, parent=None, kullanici_id: int = 0):
        super().__init__(parent)
        self.kullanici_id = kullanici_id
        self.setWindowTitle("Kullanıcı Detayı")
        self.setMinimumSize(760, 580)
        self.setStyleSheet(f"background:{BG}; color:{TEXT};")
        self._build_ui()

    def _build_ui(self):
        profil  = admin_get_kullanici_detay(self.kullanici_id)
        gecmis  = admin_get_kullanici_gecmis(self.kullanici_id)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Başlık ──────────────────────────────────────────
        header = QFrame()
        header.setStyleSheet(f"background:{BG2}; border-bottom:1px solid {BORDER};")
        header.setFixedHeight(60)
        hl = QHBoxLayout(header)
        hl.setContentsMargins(20, 0, 20, 0)

        if profil:
            hl.addWidget(_lbl(f"👤  {profil['ad']} {profil['soyad']}",
                              size=16, bold=True))
            hl.addWidget(_lbl(f"  —  {profil['email']}", color=MUTED))
            durum = "✅ Aktif" if profil["aktif"] else "🚫 Pasif"
            hl.addWidget(_lbl(f"  |  {durum}",
                              color=GREEN if profil["aktif"] else "#ff7043"))
        hl.addStretch()

        btn_kapat = QPushButton("✕  Kapat")
        btn_kapat.setStyleSheet(f"""
            QPushButton {{
                background:{BG3}; color:{MUTED}; border:1px solid {BORDER};
                border-radius:5px; font-size:12px; padding:5px 14px;
            }}
            QPushButton:hover {{ color:white; }}
        """)
        btn_kapat.clicked.connect(self.accept)
        hl.addWidget(btn_kapat)
        root.addWidget(header)

        # ── Sekmeler ────────────────────────────────────────
        tabs = QTabWidget()
        tabs.setStyleSheet(f"""
            QTabWidget::pane {{ border:none; background:{BG}; }}
            QTabBar::tab {{
                background:{BG2}; color:{MUTED}; padding:9px 18px; border:none; font-size:12px;
            }}
            QTabBar::tab:selected {{ color:white; border-bottom:2px solid {RED}; }}
        """)

        if profil:
            tabs.addTab(self._tab_info(profil), "📋  Bilgiler")
        tabs.addTab(self._tab_gecmis(gecmis),   "🎬  İzleme Geçmişi")

        root.addWidget(tabs)

    # ──────────────────────────────────────────────────────────
    def _tab_info(self, p) -> QWidget:
        w = QWidget()
        w.setStyleSheet(f"background:{BG};")
        layout = QVBoxLayout(w)
        layout.setContentsMargins(28, 20, 28, 20)
        layout.setSpacing(10)

        stats = [
            ("👤", "Ad Soyad",       f"{p['ad']} {p['soyad']}"),
            ("📧", "E-mail",         p["email"]),
            ("⚧", "Cinsiyet",       p["cinsiyet"] or "—"),
            ("🌍", "Ülke",           p["ulke"] or "—"),
            ("🎂", "Doğum Tarihi",   str(p["dogum_tarihi"]) if p["dogum_tarihi"] else "—"),
            ("📅", "Kayıt Tarihi",   str(p["kayit_tarihi"])[:10] if p["kayit_tarihi"] else "—"),
            ("🔑", "Rol",            p["rol_adi"]),
            ("⏱", "Toplam Süre",    f"{p['toplam_sure_dk']} dk  ({p['toplam_sure_dk']//60} saat)"),
            ("🎬", "İzlenen İçerik", str(p["izlenen_icerik"])),
            ("⭐", "Ort. Puan",      f"{float(p['ort_puan']):.1f}" if p["ort_puan"] else "—"),
        ]

        for icon, key, val in stats:
            card = QFrame()
            card.setStyleSheet(f"background:{BG2}; border-radius:6px;")
            cl = QHBoxLayout(card)
            cl.setContentsMargins(14, 8, 14, 8)
            cl.addWidget(_lbl(icon, size=16))
            cl.addWidget(_lbl(key, color=MUTED))
            cl.addStretch()
            cl.addWidget(_lbl(val, bold=True))
            layout.addWidget(card)

        # Favori türler
        if p.get("favori_turler"):
            layout.addWidget(_divider())
            layout.addWidget(_lbl("Favori Türler", bold=True))
            badge_row = QHBoxLayout()
            for tur in p["favori_turler"]:
                b = QLabel(f"  {tur}  ")
                b.setStyleSheet(f"""
                    background:{RED}; color:white; border-radius:4px;
                    font-size:11px; font-weight:bold; padding:3px 0;
                """)
                b.setFixedHeight(22)
                badge_row.addWidget(b)
            badge_row.addStretch()
            layout.addLayout(badge_row)

        layout.addStretch()
        return w

    # ──────────────────────────────────────────────────────────
    def _tab_gecmis(self, gecmis: list) -> QWidget:
        w = QWidget()
        w.setStyleSheet(f"background:{BG};")
        layout = QVBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)

        cols = ["Program Adı", "Tip", "İzleme Tarihi",
                "Bölüm", "Süre (dk)", "Puan", "Tamamlandı"]
        tbl = QTableWidget(0, len(cols))
        tbl.setHorizontalHeaderLabels(cols)
        tbl.setStyleSheet(TABLE_STYLE)
        tbl.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        tbl.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        tbl.verticalHeader().setVisible(False)
        tbl.verticalHeader().setDefaultSectionSize(40)
        hh = tbl.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for i in range(1, len(cols)):
            hh.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)

        for r_data in gecmis:
            r = tbl.rowCount()
            tbl.insertRow(r)
            tarih = str(r_data["izleme_tarihi"])[:16] if r_data["izleme_tarihi"] else "—"
            puan  = str(r_data["puan"]) if r_data["puan"] else "—"
            tam   = "✅ Evet" if r_data["tamamlandi"] else "⏸ Hayır"

            def si(text, color=None):
                it = QTableWidgetItem(str(text))
                it.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                if color:
                    it.setForeground(QColor(color))
                return it

            tbl.setItem(r, 0, si(r_data["program_adi"]))
            tbl.setItem(r, 1, si(r_data["program_tipi"],
                "#4fc3f7" if r_data["program_tipi"] == "Film" else "#a5d6a7"))
            tbl.setItem(r, 2, si(tarih, MUTED))
            tbl.setItem(r, 3, si(r_data["bolum_no"]))
            tbl.setItem(r, 4, si(r_data["izlenen_dk"]))
            tbl.setItem(r, 5, si(puan, GOLD if r_data["puan"] else MUTED))
            tbl.setItem(r, 6, si(tam, GREEN if r_data["tamamlandi"] else "#ffb74d"))

        layout.addWidget(tbl)

        # Alt özet
        toplam_dk = sum(r["izlenen_dk"] for r in gecmis)
        ozet = QLabel(f"  {len(gecmis)} kayıt  |  Toplam: {toplam_dk} dk ({toplam_dk//60} saat)")
        ozet.setStyleSheet(f"color:{MUTED}; font-size:11px; padding:5px;")
        layout.addWidget(ozet)
        return w

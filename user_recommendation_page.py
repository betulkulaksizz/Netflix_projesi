from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QScrollArea, QGridLayout, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from queries import get_recommendations_for_user

BG         = "#141414"
BG2        = "#1e1e1e"
BG3        = "#2b2b2b"
RED        = "#E50914"
TEXT       = "#ffffff"
TEXT_MUTED = "#aaaaaa"
BORDER     = "#333333"
GOLD       = "#daa520"


class UserRecommendationPage(QWidget):
    def __init__(self, user: dict, on_izle=None, parent=None):
        super().__init__(parent)
        self.user    = user
        self.on_izle = on_izle
        self.setWindowTitle("💡 Size Özel Öneriler")
        self.resize(900, 620)
        self.setStyleSheet(f"background:{BG}; color:{TEXT};")
        self._build_ui()
        self._load()

    # ──────────────────────────────────────────────────────────
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Başlık barı ──
        topbar = QFrame()
        topbar.setStyleSheet(f"background:{BG2}; border-bottom:1px solid {BORDER};")
        topbar.setFixedHeight(56)
        tb_layout = QHBoxLayout(topbar)
        tb_layout.setContentsMargins(20, 0, 20, 0)

        icon = QLabel("💡")
        icon.setFont(QFont("Arial", 20))
        tb_layout.addWidget(icon)

        title = QLabel("Size Özel Öneriler")
        title.setFont(QFont("Arial", 15, QFont.Weight.Bold))
        title.setStyleSheet(f"color:{RED};")
        tb_layout.addWidget(title)

        tb_layout.addStretch()

        btn_yenile = QPushButton("🔄 Yenile")
        btn_yenile.setStyleSheet(f"""
            QPushButton {{ background:{BG3}; color:{TEXT_MUTED}; border-radius:6px;
                font-size:12px; padding:5px 14px; border:1px solid {BORDER}; }}
            QPushButton:hover {{ color:white; }}
        """)
        btn_yenile.clicked.connect(self._load)
        tb_layout.addWidget(btn_yenile)

        btn_kapat = QPushButton("✕ Kapat")
        btn_kapat.setStyleSheet(f"""
            QPushButton {{ background:{RED}; color:white; border-radius:6px;
                font-size:12px; font-weight:bold; padding:5px 14px; }}
            QPushButton:hover {{ background:#f40612; }}
        """)
        btn_kapat.clicked.connect(self.close)
        tb_layout.addWidget(btn_kapat)

        root.addWidget(topbar)

        # ── Açıklama ──
        info = QLabel(
            f"Merhaba {self.user['ad']}! Favori türleriniz ve izleme geçmişinize göre hazırlanmış öneriler:"
        )
        info.setStyleSheet(f"color:{TEXT_MUTED}; font-size:13px; padding:12px 20px 4px 20px;")
        root.addWidget(info)

        # ── Kart alanı ──
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border:none; }")

        self.grid_widget = QWidget()
        self.grid_widget.setStyleSheet(f"background:{BG};")
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setContentsMargins(16, 12, 16, 16)
        self.grid_layout.setSpacing(14)

        scroll.setWidget(self.grid_widget)
        root.addWidget(scroll)

        # ── Durum etiketi ──
        self.status_lbl = QLabel("Yükleniyor...")
        self.status_lbl.setStyleSheet(f"color:{TEXT_MUTED}; font-size:12px; padding:6px 20px;")
        root.addWidget(self.status_lbl)

    # ──────────────────────────────────────────────────────────
    def _load(self):
        self.status_lbl.setText("Yükleniyor...")
        # Önceki kartları temizle
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        programs = get_recommendations_for_user(self.user["kullanici_id"])

        if not programs:
            lbl = QLabel("Henüz yeterli veri yok. İzleme geçmişiniz arttıkça öneriler kişiselleşir.")
            lbl.setStyleSheet(f"color:{TEXT_MUTED}; font-size:14px;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(lbl, 0, 0, 1, 3)
            self.status_lbl.setText("")
            return

        cols = 3
        for idx, prog in enumerate(programs):
            row = idx // cols
            col = idx % cols
            card = self._make_card(prog)
            self.grid_layout.addWidget(card, row, col)

        self.status_lbl.setText(f"{len(programs)} öneri listelendi.")

    # ──────────────────────────────────────────────────────────
    def _make_card(self, prog: dict) -> QFrame:
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background:{BG2}; border:1px solid {BORDER};
                border-radius:10px;
            }}
            QFrame:hover {{ border-color:#555; }}
        """)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(6)

        # Tür rozeti + kaynak rozeti
        badge_row = QHBoxLayout()
        tip_color = RED if prog["program_tipi"] == "Film" else "#1a6fb5"
        tip_badge = QLabel(prog["program_tipi"])
        tip_badge.setStyleSheet(f"""
            background:{tip_color}; color:white; border-radius:4px;
            padding:2px 8px; font-size:10px; font-weight:bold;
        """)
        badge_row.addWidget(tip_badge)

        if prog.get("kaynak"):
            src_badge = QLabel(prog["kaynak"])
            src_badge.setStyleSheet(f"""
                background:#2a4a2a; color:#7ec87e; border-radius:4px;
                padding:2px 8px; font-size:10px;
            """)
            badge_row.addWidget(src_badge)

        badge_row.addStretch()
        layout.addLayout(badge_row)

        # Program adı
        name_lbl = QLabel(prog["program_adi"])
        name_lbl.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        name_lbl.setStyleSheet(f"color:{TEXT};")
        name_lbl.setWordWrap(True)
        layout.addWidget(name_lbl)

        # Türler
        if prog.get("turler"):
            tur_lbl = QLabel(prog["turler"])
            tur_lbl.setStyleSheet(f"color:{TEXT_MUTED}; font-size:11px;")
            tur_lbl.setWordWrap(True)
            layout.addWidget(tur_lbl)

        # Meta bilgi (yıl, puan, izlenme)
        meta_row = QHBoxLayout()
        yil_lbl = QLabel(f"📅 {prog['yayin_yili']}")
        yil_lbl.setStyleSheet(f"color:{TEXT_MUTED}; font-size:11px;")
        meta_row.addWidget(yil_lbl)

        puan_val = float(prog["ortalama_puan"] or 0)
        puan_lbl = QLabel(f"⭐ {puan_val:.1f}")
        puan_lbl.setStyleSheet(f"color:{GOLD}; font-size:11px;")
        meta_row.addWidget(puan_lbl)

        izlenme_lbl = QLabel(f"👁 {prog['toplam_izlenme'] or 0}")
        izlenme_lbl.setStyleSheet(f"color:{TEXT_MUTED}; font-size:11px;")
        meta_row.addWidget(izlenme_lbl)

        meta_row.addStretch()
        layout.addLayout(meta_row)

        # İzle butonu
        btn_izle = QPushButton("▶ İzle")
        btn_izle.setFixedHeight(32)
        btn_izle.setStyleSheet(f"""
            QPushButton {{ background:{RED}; color:white; border-radius:6px;
                font-size:12px; font-weight:bold; }}
            QPushButton:hover {{ background:#f40612; }}
        """)
        btn_izle.clicked.connect(lambda _, p=prog: self._izle(p))
        layout.addWidget(btn_izle)

        return card

    # ──────────────────────────────────────────────────────────
    def _izle(self, prog: dict):
        if self.on_izle:
            self.on_izle(prog, False, None)

from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QFrame, QPushButton, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


STYLE_CARD = """
    QFrame {
        background-color: #1e1e1e;
        border: 1px solid #333;
        border-radius: 10px;
    }
"""

STYLE_BTN = """
    QPushButton {
        background-color: #E50914;
        color: white;
        border-radius: 6px;
        font-size: 14px;
        font-weight: bold;
        min-height: 42px;
    }
    QPushButton:hover  { background-color: #f40612; }
    QPushButton:pressed{ background-color: #b2070f; }
"""


class RecommendationPage(QWidget):
    def __init__(self, user_name: str, recommendations: list, on_continue):
        """
        recommendations: [{'program_adi', 'program_tipi', 'ortalama_puan',
                            'toplam_izlenme', 'tur_adi'}, ...]
        on_continue: Giriş sayfasına dön callback'i
        """
        super().__init__()
        self.on_continue = on_continue
        self.setWindowTitle("Netflix Platform - Öneriler")
        self.setFixedSize(540, 640)
        self.setStyleSheet("background-color: #141414;")
        self._build_ui(user_name, recommendations)

    def _build_ui(self, user_name, recommendations):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Başlık ──────────────────────────────────────────
        header = QWidget()
        header.setStyleSheet("background-color: #1a1a1a;")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(30, 20, 30, 20)

        welcome = QLabel(f"Hoş geldin, {user_name}! 🎉")
        welcome.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        welcome.setStyleSheet("color: white;")
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(welcome)

        sub = QLabel("Favori türlerine göre seçtiğimiz içerikler:")
        sub.setStyleSheet("color: #aaaaaa; font-size: 13px;")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(sub)

        root.addWidget(header)

        # ── Scroll alan ─────────────────────────────────────
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            "QScrollArea { border: none; background: transparent; }"
            "QScrollBar:vertical { background:#1a1a1a; width:8px; border-radius:4px; }"
            "QScrollBar::handle:vertical { background:#444; border-radius:4px; }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height:0; }"
        )

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        cards_layout = QVBoxLayout(container)
        cards_layout.setContentsMargins(30, 16, 30, 16)
        cards_layout.setSpacing(12)

        if recommendations:
            for rec in recommendations:
                cards_layout.addWidget(self._make_card(rec))
        else:
            no_data = QLabel("Henüz öneri oluşturulamadı.")
            no_data.setStyleSheet("color: #888; font-size: 13px;")
            no_data.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cards_layout.addWidget(no_data)

        cards_layout.addStretch()
        scroll.setWidget(container)
        root.addWidget(scroll)

        # ── Alt buton ───────────────────────────────────────
        footer = QWidget()
        footer.setStyleSheet("background-color: #1a1a1a;")
        footer_layout = QVBoxLayout(footer)
        footer_layout.setContentsMargins(30, 14, 30, 14)

        btn = QPushButton("Giriş Yap →")
        btn.setStyleSheet(STYLE_BTN)
        btn.clicked.connect(self._go)
        footer_layout.addWidget(btn)

        root.addWidget(footer)

    def _make_card(self, rec: dict) -> QFrame:
        card = QFrame()
        card.setStyleSheet(STYLE_CARD)
        layout = QHBoxLayout(card)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)

        # Tür rozeti
        badge = QLabel(rec.get("tur_adi", ""))
        badge.setFixedWidth(90)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet("""
            background-color: #E50914;
            color: white;
            border-radius: 4px;
            font-size: 11px;
            font-weight: bold;
            padding: 4px 6px;
        """)
        layout.addWidget(badge)

        # İçerik bilgisi
        info = QVBoxLayout()
        info.setSpacing(2)

        name_lbl = QLabel(rec.get("program_adi", ""))
        name_lbl.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        name_lbl.setStyleSheet("color: white;")
        info.addWidget(name_lbl)

        tip = rec.get("program_tipi", "")
        puan = rec.get("ortalama_puan", 0)
        izlenme = rec.get("toplam_izlenme", 0)
        detail_lbl = QLabel(f"{tip}  •  ⭐ {puan}  •  👁 {izlenme} izlenme")
        detail_lbl.setStyleSheet("color: #999999; font-size: 12px;")
        info.addWidget(detail_lbl)

        layout.addLayout(info)
        layout.addStretch()
        return card

    def _go(self):
        self.close()
        self.on_continue()

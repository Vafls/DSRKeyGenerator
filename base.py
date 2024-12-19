import sys
import random
import string
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QListWidget,
)
from PyQt5.QtGui import QFont, QMouseEvent
from PyQt5.QtCore import Qt, QPoint


class KeyGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)  # Убираем системное меню
        self.setStyleSheet(
            """
            QWidget {
                background-color: #e0f7ff;  /* Фон окна */
                border: 2px solid #a0a0a0;  /* Окантовка */
                border-radius: 8px;  /* Закругленные углы */
            }
            QLabel {
                color: #333;
                font-size: 12px;
            }
            QPushButton {
                background-color: #c0e7ff;
                border: none;
                padding: 5px 10px;
                font-size: 12px;
                color: #333;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #80d0ff;
            }
            """
        )
        self.offset = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.create_title_bar(layout)

        content_layout = QHBoxLayout()
        layout.addLayout(content_layout)

        self.service_list = QListWidget()
        self.service_list.addItem("Steam")
        self.service_list.addItem("Roblox")
        self.service_list.addItem("Discord")
        self.service_list.setFixedWidth(150)
        content_layout.addWidget(self.service_list)

        center_layout = QVBoxLayout()
        self.key_count_label = QLabel("Количество ключей (от 1 до 25):")
        self.key_count_input = QLineEdit()
        self.key_count_input.setPlaceholderText("Введите число")

        center_layout.addWidget(self.key_count_label)
        center_layout.addWidget(self.key_count_input)

        self.generate_button = QPushButton("Сгенерировать ключи")
        self.generate_button.clicked.connect(self.generate_keys)
        center_layout.addWidget(self.generate_button)

        self.key_output = QTextEdit()
        self.key_output.setReadOnly(True)
        center_layout.addWidget(self.key_output)

        content_layout.addLayout(center_layout)

    def create_title_bar(self, layout):
        """Создаем кастомный заголовок окна с кнопками управления."""
        title_bar = QHBoxLayout()
        title_bar.setContentsMargins(8, 4, 8, 4)
        title_bar.setSpacing(10)

        self.title_label = QLabel("Key Generator by Vafls")
        self.title_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.title_label.setStyleSheet("color: #333;")
        title_bar.addWidget(self.title_label)

        title_bar.addStretch()

        self.minimize_button = QPushButton("—")
        self.minimize_button.setFixedSize(30, 30)
        self.minimize_button.clicked.connect(self.showMinimized)
        title_bar.addWidget(self.minimize_button)

        self.maximize_button = QPushButton("□")
        self.maximize_button.setFixedSize(30, 30)
        self.maximize_button.clicked.connect(self.toggle_maximize)
        title_bar.addWidget(self.maximize_button)

        self.close_button = QPushButton("✕")
        self.close_button.setFixedSize(30, 30)
        self.close_button.clicked.connect(self.close)
        title_bar.addWidget(self.close_button)

        layout.addLayout(title_bar)

    def toggle_maximize(self):
        """Переключение между развёрнутым и нормальным состоянием окна."""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def mousePressEvent(self, event: QMouseEvent):
        """Обработка нажатия мыши для перемещения окна."""
        if event.button() == Qt.LeftButton:
            self.offset = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        """Обработка перемещения мыши для перемещения окна."""
        if event.buttons() == Qt.LeftButton and self.offset:
            self.move(event.globalPos() - self.offset)
            event.accept()

    def generate_keys(self):
        """Генерация ключей в зависимости от выбранного сервиса."""
        try:
            count = int(self.key_count_input.text())
            if not (1 <= count <= 25):
                raise ValueError
        except ValueError:
            self.key_output.setText("Введите корректное число от 1 до 25.")
            return

        selected_item = self.service_list.currentItem()
        if selected_item is None:
            self.key_output.setText("Пожалуйста, выберите сервис из списка.")
            return

        service = selected_item.text()
        self.key_output.clear()

        for _ in range(count):
            if service == "Steam":
                key = self.generate_steam_key()
            elif service == "Roblox":
                key = self.generate_roblox_key()
            else:
                key = self.generate_discord_key()
            self.key_output.append(key)

    def generate_steam_key(self):
        return "-".join(
            "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
            for _ in range(3)
        )

    def generate_roblox_key(self):
        return "-".join(
            "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
            for _ in range(3)
        )

    def generate_discord_key(self):
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=24))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KeyGeneratorApp()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec_())

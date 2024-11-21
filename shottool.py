import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QLabel, QPushButton, QMessageBox, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QImage, QKeyEvent
from PyQt5.QtCore import Qt, QEvent

rootfs = "/studio/project/mochen/source/images/"

class QPicEdit(QTextEdit):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        # 禁用滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def keyPressEvent(self, event: QKeyEvent):
        # 处理 Ctrl+V 粘贴事件
        super().keyPressEvent(event)
        if event.key() == Qt.Key_V and event.modifiers() & Qt.ControlModifier:
            self.clear_and_move_cursor()
            clipboard = QApplication.clipboard()
            mime_data = clipboard.mimeData()
            if mime_data.hasImage():
                self.insertImageIntoTextEdit(clipboard.image())
                self.parent.save_screenshot(clipboard.image())
            else:
                self.setPlainText("Context is not picture!")

    def insertImageIntoTextEdit(self, image):
        text_edit_width = self.width()
        text_edit_height = self.height()

        # 将图片调整为 QTextEdit 的大小
        scaled_image = image.scaled(text_edit_width, text_edit_height, Qt.KeepAspectRatioByExpanding)
        cursor = self.textCursor()  # 获取当前文本光标
        cursor.insertImage(scaled_image)  # 插入图片

    def clear_and_move_cursor(self):
        self.clear()  # 清空文本框内容
        cursor = self.textCursor()  # 获取文本光标
        cursor.movePosition(cursor.Start)  # 将光标移动到文本开头
        self.setTextCursor(cursor)  # 设置光标

class ScreenshotSaver(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.image_counter = 1  # 文件名从起始 ID 开始

    def init_ui(self):
        self.setWindowTitle("shottool")
        self.resize(600, 400)

        # 创建主布局
        main_layout = QVBoxLayout()

        # 第一行布局
        top_layout = QHBoxLayout()
        self.id_input_label = QLabel("Index：", self)
        top_layout.addWidget(self.id_input_label, 1)
        self.id_input = QLineEdit(self)
        top_layout.addWidget(self.id_input, 2)
        self.directory_input_label = QLabel("RootFs：", self)
        top_layout.addWidget(self.directory_input_label, 1)
        self.directory_input = QLineEdit(self)
        self.directory_input.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed
        )
        top_layout.addWidget(self.directory_input, 8)
        main_layout.addLayout(top_layout)

        # 大文本框：用于粘贴截图
        self.image_paste_area = QPicEdit(self)
        self.image_paste_area.setAlignment(Qt.AlignCenter)  # 设置文本居中对齐
        main_layout.addWidget(self.image_paste_area)

        # 最后一行布局
        bottom_layout = QHBoxLayout()

        # 保存路径显示
        self.save_path = QLabel("Path：", self)
        bottom_layout.addWidget(self.save_path, 1)
        self.save_path_label = QLabel("", self)
        bottom_layout.addWidget(self.save_path_label, 8)
        # 复制路径按钮
        self.copy_button = QPushButton("Copy", self)
        self.copy_button.clicked.connect(self.copy_save_path, 8)
        bottom_layout.addWidget(self.copy_button)

        main_layout.addLayout(bottom_layout)

        # 设置主布局
        self.setLayout(main_layout)

    

    def save_screenshot(self, image: QImage):
        # 获取目录路径和起始 ID
        directory = rootfs + self.directory_input.text().strip()
        start_id = self.id_input.text().strip()

        if not directory:
            QMessageBox.warning(self, "error", "Please select the path to save!")
            return

        if not start_id.isdigit():
            QMessageBox.warning(self, "error", "Value type is not integer")
            return

        # 转换起始 ID
        self.image_counter = int(start_id)

        # 检查目录是否存在，不存在则创建
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except Exception as e:
                QMessageBox.critical(self, "error", f"faild to create dir: {e}")
                return

        # 保存图片
        while True:
            file_path = os.path.join(directory, f"{self.image_counter}.png")
            if not os.path.exists(file_path):
                break
            self.image_counter += 1

        pixmap = QPixmap.fromImage(image)
        if pixmap.save(file_path, "PNG"):
            self.save_path_label.setText(f"{file_path}")  # 更新保存路径标签
        else:
            QMessageBox.critical(self, "error", f"Picture save faild!")

    def copy_save_path(self):
        # 复制保存路径到剪贴板
        save_path = self.save_path_label.text()[len(rootfs)- 7:]
        if save_path:
            clipboard = QApplication.clipboard()
            clipboard.setText(save_path)
        else:
            QMessageBox.warning(self, "warning", "save nothing")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScreenshotSaver()
    window.show()
    sys.exit(app.exec_())

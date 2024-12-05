import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QVBoxLayout,
    QFileDialog, QMessageBox, QWidget
)
from PyQt6.QtGui import QAction


class NoteEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.text_edit = QTextEdit(self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text_edit)
        self.setLayout(self.layout)
        self.file_path = None

    def save_note_to_file(self):
        if not self.file_path:
            self.file_path, _ = QFileDialog.getSaveFileName(
                self, "Сохранить файл", "", "Текстовые файлы (*.txt);;Все файлы (*)"
            )
        if self.file_path:
            try:
                with open(self.file_path, 'w', encoding='utf-8') as file:
                    file.write(self.text_edit.toPlainText())
                QMessageBox.information(self, "Сохранено", "Заметка сохранена успешно!")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл:\n{e}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Менеджер заметок")
        self.setGeometry(100, 100, 800, 600)
        self.note_editor = None
        self.create_menu()

    def create_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("Файл")

        new_note_action = QAction("Новая заметка", self)
        new_note_action.triggered.connect(self.new_note)
        file_menu.addAction(new_note_action)

        save_note_action = QAction("Сохранить заметку", self)
        save_note_action.triggered.connect(self.save_note)
        file_menu.addAction(save_note_action)

        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def new_note(self):
        self.note_editor = NoteEditor()
        self.setCentralWidget(self.note_editor)

    def save_note(self):
        if self.note_editor:
            self.note_editor.save_note_to_file()
        else:
            QMessageBox.warning(self, "Предупреждение", "Нет открытой заметки для сохранения!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

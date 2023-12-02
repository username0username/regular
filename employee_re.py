import sys
import re
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit

class EmployeeViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        self.load_button = QPushButton('Загрузить файл', self)
        self.name_button = QPushButton('Вывести имена', self)
        self.email_button = QPushButton('Вывести почты', self)
        self.phone_button = QPushButton('Вывести номера телефонов', self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.load_button)
        layout.addWidget(self.name_button)
        layout.addWidget(self.email_button)
        layout.addWidget(self.phone_button)

        self.load_button.clicked.connect(self.load_data)
        self.name_button.clicked.connect(self.display_names)
        self.email_button.clicked.connect(self.display_emails)
        self.phone_button.clicked.connect(self.display_phones)

        self.setWindowTitle('re сотрудники')
        self.setFixedSize(400, 500)

    def load_data(self):
        try:
            script_path = os.path.abspath(sys.argv[0])
            script_directory = os.path.dirname(script_path)
            file_path = os.path.join(script_directory, 'empl.txt')

            with open(file_path, 'r', encoding='utf-8') as file:
                self.employee_data = file.read()
                self.text_edit.setPlainText(self.employee_data)
        except FileNotFoundError:
            self.text_edit.setPlainText('Файл не найден.')
        except UnicodeDecodeError:
            self.text_edit.setPlainText('Ошибка декодирования файла. Пожалуйста, убедитесь, что файл использует корректную кодировку.')

    def display_names(self):
        names = re.findall(r'Имя:\s*([\S\s]+?(?=Почта:|$))', self.employee_data)
        if names:
            names_text = '\n'.join(f'Имя: {name.strip()}' for name in names)
            self.text_edit.setPlainText(names_text)
        else:
            self.text_edit.setPlainText('Имена не найдены.')

    def display_emails(self):
        emails = re.findall(r'Почта:\s*([\w.-]+@[\w.-]+)', self.employee_data)
        if emails:
            emails_text = '\n'.join(f'Почта: {email}' for email in emails)
            self.text_edit.setPlainText(emails_text)
        else:
            self.text_edit.setPlainText('Адреса электронной почты не найдены.')

    def display_phones(self):
        phones = re.findall(r'Номер телефона:\s*(\S+)', self.employee_data)
        if phones:
            phones_text = '\n'.join(f'Номер телефона: {phone}' for phone in phones)
            self.text_edit.setPlainText(phones_text)
        else:
            self.text_edit.setPlainText('Номера телефона не найдены.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = EmployeeViewer()
    viewer.show()
    sys.exit(app.exec_())

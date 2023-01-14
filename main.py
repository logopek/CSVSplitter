import csv
import sys
from PyQt5 import QtGui
from PyQt5 import QtWidgets


class CSVSplitter(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.label = None
        self.resize(300,300)
        self.file_target = ""
        self.path = ""
        self.initUI()

    def initUI(self):
        self.setWindowTitle("CSV Splitter")
        self.open_file_button = QtWidgets.QPushButton(self)
        self.open_file_button.setText("Выбрать csv")
        self.open_file_button.setGeometry(0, 0, 111, 46)
        self.open_file_button.clicked.connect(self.file_select)
        self.save_path_btn = QtWidgets.QPushButton(self)
        self.save_path_btn.setText("Директория сохранения файлов")
        self.save_path_btn.setGeometry(0, 250, 175, 20)
        self.save_path_btn.clicked.connect(self.save_path)
        self.count = QtWidgets.QLineEdit(self)
        self.count.setGeometry(111,0, 200,40)
        self.count.setPlaceholderText("Кол-во строк через которое \n надо разбить файл")
        self.count.setToolTip("Кол-во строк через которое надо разбить файл")
        self.count.setValidator(QtGui.QIntValidator())
        self.file_name = QtWidgets.QLineEdit(self)
        self.file_name.setPlaceholderText("Новое имя файла")
        self.file_name.setToolTip("Новое имя файла")
        self.file_name.move(0, 50)
        self.file_name.setFixedSize(111, 20)
        self.ok_btn = QtWidgets.QPushButton(self)
        self.ok_btn.setText("Начать")
        self.ok_btn.clicked.connect(self.split)
        self.ok_btn.setGeometry(0,270, 175,30)


    def file_select(self):
        self.file_target = QtWidgets.QFileDialog().getOpenFileName(filter="*.csv")

    def save_path(self):
        diag = QtWidgets.QFileDialog()
        diag.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)
        diag.setOption(QtWidgets.QFileDialog.Option.ShowDirsOnly, True)
        self.path = diag.getExistingDirectory()

    def check(self):
        if not self.file_target:
            exchook = QtWidgets.QMessageBox(self)
            exchook.setText("Файл не выбран")
            exchook.exec_()
            return False
        if not self.count.text():
            exchook = QtWidgets.QMessageBox(self)
            exchook.setText("Не выбрано количество строк")
            exchook.exec_()
            return False
        if not self.file_name.text():
            exchook = QtWidgets.QMessageBox(self)
            exchook.setText("Имя файла не выбрано")
            exchook.exec_()
            return False
        if not self.path:
            exchook = QtWidgets.QMessageBox(self)
            exchook.setText("Директория для сохранения не выбрана")
            exchook.exec_()
            return False

        return True
    def split(self):
        if self.check():
            with open(self.file_target[0], newline='\n') as f:
                reader = csv.reader(f, quoting=csv.QUOTE_NONE)
                headers = next(reader)
                print(headers)
                temp = []
                i = 1
                for row in reader:
                    print(f"{row}")
                    if i % int(self.count.text()) == 0:
                        temp.append(row)
                        print(f"{self.path}/{self.file_name.text()}_{i}.csv")
                        with open(f"{self.path}/{self.file_name.text()}_{i}.csv", "w") as n_f:
                            wrt = csv.writer(n_f, lineterminator='\n', quotechar="'", quoting=csv.QUOTE_NONE)
                            wrt.writerow(headers)
                            wrt.writerows(temp)
                            temp.clear()
                    else:
                        temp.append(row)
                    print(temp)
                    i += 1

                with open(f"{self.path}/{self.file_name.text()}_last.csv", "w") as n_f:
                    wrt = csv.writer(n_f, lineterminator='\n', quotechar="'", quoting=csv.QUOTE_NONE)
                    wrt.writerow(headers)
                    wrt.writerows(temp)
                    temp.clear()




def _excepthook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

app = QtWidgets.QApplication(sys.argv)
ex = CSVSplitter()
ex.show()
sys.excepthook = _excepthook
sys.exit(app.exec())

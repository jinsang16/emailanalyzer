import csv

import pandas as pd
from PyQt5 import QtGui
from PyQt5.QtWidgets import *

df = pd.read_csv('emails.csv', encoding='UTF8')


class MyWindow(QWidget):
    def __make_table(self):
        self.model = QtGui.QStandardItemModel(self)
        self.model.setHorizontalHeaderLabels(['reply', 'invite', 'invite date', 'subject'])
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setSelectionMode(QAbstractItemView.SingleSelection)  # 다중 선택 금지
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)  # edit 금지
        self.tableView.clicked.connect(self.__cell_clicked)

        for i in df.index:
            row = df.loc[i, :]
            items = [QtGui.QStandardItem(str(row['labelled'])), QtGui.QStandardItem(str(row['invited'])),
                     QtGui.QStandardItem(str(row['invited_date'])), QtGui.QStandardItem(str(row['subject']))]
            self.model.appendRow(items)

    def __init__(self, data, parent=None):
        super().__init__(parent)

        self.tableView = QTableView(parent)
        self.label = QLabel()
        self.scrollArea = QScrollArea()
        self._mainwin = parent

        self._data = data
        self.__make_layout()
        self.__make_table()

    def __cell_clicked(self, item):
        if item is not None:
            txt = df.loc[item.row(), 'body']
        else:
            txt = 'cell: ({0},{1})'.format(item.row(), item.column())
        self.label.setText(txt)

        self.scrollArea.clearFocus()
        self.scrollArea.setWidget(self.label)

    def __make_layout(self):
        vBox = QVBoxLayout()
        vBox.addWidget(self.tableView)
        vBox.addWidget(self.scrollArea)
        self.scrollArea.setWidgetResizable(True)
        self.setLayout(vBox)


class EmlViewer(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        window = MyWindow(self)
        self.setCentralWidget(window)
        self.csv = csv


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setApplicationName('csv viewer')
    view = EmlViewer()
    view.resize(800, 600)
    view.show()
    sys.exit(app.exec())

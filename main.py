import sys
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
import maps

file_map = 'map.png'


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('on.ui', self)

        self.show_btn.clicked.connect(self.show_map)
        self.scale.textChanged.connect(self.show_map)

    def show_map(self):
        place = self.lineEdit.text()
        coods = maps.geocode_maps(place)
        im_bit = maps.static_api(coods, self.scale.value())
        with open(file_map, 'wb') as f:
            f.write(im_bit)

        self.pixmap = QPixmap(file_map)
        self.label.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.scale.setValue(self.scale.value() + 1)
            self.show_map()
        if event.key() == Qt.Key_PageDown:
            self.scale.setValue(self.scale.value() - 1)
            self.show_map()



def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())

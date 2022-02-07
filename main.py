import sys
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
import maps

from PIL import Image

file_map = 'map.png'
TYPE_MAP = {'схема': 'map',
            'спутник': 'sat',
            'гибрид': 'sat,skl'}


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('on.ui', self)

        self.coords = None

        self.type_map.addItems(TYPE_MAP.keys())

        self.show_btn.clicked.connect(self.new_place)
        self.scale.textChanged.connect(self.show_map)
        self.type_map.currentIndexChanged.connect(self.show_map)

    def new_place(self):
        place = self.lineEdit.text()
        self.coords = maps.geocode_maps(place)
        self.show_map()

    def show_map(self):
        if self.coords is None:
            return
        im_bit = maps.static_api(self.coords, self.scale.value(), TYPE_MAP[self.type_map.currentText()])
        with open(file_map, 'wb') as f:
            f.write(im_bit)

        im = Image.open(file_map)
        im = im.resize((650, 450))
        im.save(file_map)

        self.pixmap = QPixmap(file_map)
        self.label.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        step1 = 0.0012
        step0 = 0.0028
        if event.key() == Qt.Key_PageUp:
            self.scale.setValue(self.scale.value() + 1)
            self.show_map()
        elif event.key() == Qt.Key_PageDown:
            self.scale.setValue(self.scale.value() - 1)
            self.show_map()

        elif event.key() == Qt.Key_W:
            self.coords[1] = str(float(self.coords[1]) + step1 * 2 ** (17 - self.scale.value()))
            self.show_map()

        elif event.key() == Qt.Key_S:
            self.coords[1] = str(float(self.coords[1]) - step1 * 2 ** (17 - self.scale.value()))
            # print(self.coords)
            self.show_map()

        elif event.key() == Qt.Key_A:
            self.coords[0] = str(float(self.coords[0]) - step0 * 2 ** (17 - self.scale.value()))
            # print(self.coords)
            self.show_map()

        elif event.key() == Qt.Key_D:
            self.coords[0] = str(float(self.coords[0]) + step0 * 2 ** (17 - self.scale.value()))
            # print(self.coords)
            self.show_map()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())

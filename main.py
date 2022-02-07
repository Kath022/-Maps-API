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
        self.search_coords = None

        self.type_map.addItems(TYPE_MAP.keys())

        self.show_btn.clicked.connect(self.search_place)
        self.scale.textChanged.connect(self.change_map)
        self.type_map.currentIndexChanged.connect(self.change_map)
        self.resert_btn.clicked.connect(self.resert_mark)

    def search_place(self):
        place = self.lineEdit.text()
        self.coords = maps.geocode_maps(place)
        self.search_coords = ','.join(self.coords)

        self.change_map()

    def resert_mark(self):
        self.search_coords = ''
        self.lineEdit.clear()
        self.change_map()

    def change_map(self):
        if self.coords is None:
            return

        coords_str = ','.join(self.coords)
        im_bit = maps.static_api(coords=coords_str, scale=self.scale.value(), l=TYPE_MAP[self.type_map.currentText()],
                                 pt=self.search_coords)
        with open(file_map, 'wb') as f:
            f.write(im_bit)

        self.show_map()

    def show_map(self):
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
            self.change_map()
        elif event.key() == Qt.Key_PageDown:
            self.scale.setValue(self.scale.value() - 1)
            self.change_map()

        elif event.key() == Qt.Key_W:
            self.coords[1] = str(float(self.coords[1]) + step1 * 2 ** (17 - self.scale.value()))
            self.change_map()

        elif event.key() == Qt.Key_S:
            self.coords[1] = str(float(self.coords[1]) - step1 * 2 ** (17 - self.scale.value()))
            self.change_map()

        elif event.key() == Qt.Key_A:
            self.coords[0] = str(float(self.coords[0]) - step0 * 2 ** (17 - self.scale.value()))
            self.change_map()

        elif event.key() == Qt.Key_D:
            self.coords[0] = str(float(self.coords[0]) + step0 * 2 ** (17 - self.scale.value()))
            self.change_map()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())

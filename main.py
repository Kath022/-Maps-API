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

        self.coords = [0, 0]

        self.show_btn.clicked.connect(self.show_map)
        self.scale.textChanged.connect(self.show_map)

    def show_map(self, change_coords=False):
        place = self.lineEdit.text()
        if not change_coords:
            self.coords = maps.geocode_maps(place)
        im_bit = maps.static_api(self.coords, self.scale.value())
        with open(file_map, 'wb') as f:
            f.write(im_bit)

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
            self.show_map(change_coords=True)

        elif event.key() == Qt.Key_S:
            self.coords[1] = str(float(self.coords[1]) - step1 * 2 ** (17 - self.scale.value()))
            # print(self.coords)
            self.show_map(change_coords=True)

        elif event.key() == Qt.Key_A:
            self.coords[0] = str(float(self.coords[0]) - step0 * 2 ** (17 - self.scale.value()))
            # print(self.coords)
            self.show_map(change_coords=True)

        elif event.key() == Qt.Key_D:
            self.coords[0] = str(float(self.coords[0]) + step0 * 2 ** (17 - self.scale.value()))
            # print(self.coords)
            self.show_map(change_coords=True)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())

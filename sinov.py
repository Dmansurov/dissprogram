import sys
import time
import uuid

import numpy as np

from matplotlib.backends.qt_compat import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)

        layout = QtWidgets.QVBoxLayout(self._main)

        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(static_canvas)
        static_canvas.setFixedHeight(200)

        self._static_ax = static_canvas.figure.subplots()
        t = np.linspace(0, 10, 501)
        self._static_ax.plot(t, np.tan(t), "r.")

        self.textedit = QtWidgets.QTextEdit()
        button = QtWidgets.QPushButton("Add Canvas")
        button.clicked.connect(self.add_image)
        layout.addWidget(button, stretch=0)
        layout.addWidget(self.textedit, stretch=1)

    def add_image(self):
        document = self.textedit.document()

        img = self.canvasToQImage(self._static_ax.figure.canvas)
        url = QtCore.QUrl()
        url.setScheme("mydata")
        url.setHost("image-{uuid}.png".format(uuid=uuid.uuid4()))
        document.addResource(QtGui.QTextDocument.ImageResource, url, img)

        # add image
        cursor = QtGui.QTextCursor(document)
        imageFormat = QtGui.QTextImageFormat()
        imageFormat.setName(url.toString())
        cursor.insertImage(imageFormat)

        # or
        # self.textedit.append('<img src="{url}" />'.format(url=url.toString()))

    @staticmethod
    def canvasToQImage(canvas):
        data = canvas.buffer_rgba()
        ch = 4
        w, h = canvas.get_width_height()
        bytesPerLine = ch * w
        img = QtGui.QImage(data, w, h, bytesPerLine, QtGui.QImage.Format_ARGB32)
        return img.rgbSwapped()


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.resize(640, 480)
    app.show()
    qapp.exec_()
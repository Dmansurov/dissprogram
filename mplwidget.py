import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from statsmodels.distributions.empirical_distribution import ECDF


# main window
# which inherits QDialog
class Window(QWidget):
    # constructor
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # matplotlib.rcParams['figure.figsize'] = [651, 551]  # for square canvas
        matplotlib.rcParams['figure.subplot.left'] = 0.1
        matplotlib.rcParams['figure.subplot.bottom'] = 0.1
        matplotlib.rcParams['figure.subplot.right'] = 0.95
        matplotlib.rcParams['figure.subplot.top'] = 0.95
        matplotlib.rcParams.update({'font.size': 10})

        # a figure instance to plot on
        self.resize(651, 551)
        self.figure = plt.figure()

        # this is the Canvas Widget that
        # displays the 'figure's takes the
        # 'figure' instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to 'plot' method
        # self.button = QPushButton('Plot')

        # adding action to the button
        # self.button.clicked.connect(self.plot)

        # creating a Vertical Box layout
        layout = QVBoxLayout()

        # adding tool bar to the layout
        layout.addWidget(self.toolbar)

        # adding canvas to the layout
        layout.addWidget(self.canvas)

        # adding push button to the layout
        # layout.addWidget(self.button)

        # setting layout to the main window
        self.setLayout(layout)
        self.show()

    # action called by the push button
    def plot(self, data, p, dist=0, param=(0,), loc=0, scale=1):
        # random data
        # data = [random.random() for i in range(10)]

        # clearing old figure
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # plot data
        S = ''
        if dist.numargs != 0:
            bb = dist.shapes.split(', ')
            for i in range(len(bb)):
                S += '{}'.format(bb[i]) + '={}'.format(param[i]) + ','

        H = ECDF(data)
        x = np.linspace(-0.20 * max(data), 1.20 * max(data), num=3 * len(data))
        y = 1 - np.power(1 - H(x), p)
        param = tuple(param)
        y1 = dist.cdf(x, *param, loc=loc, scale=scale)
        ax.plot(x, y, label='ACL-baho')
        ax.plot(x, y1, label='{}({} loc={}, scale={})'.format(dist.name, S, loc, scale))
        ax.legend()

        # refresh canvas
        self.canvas.draw()
        return '{}({} loc={}, scale={})'.format(dist.name, S, loc, scale)

    def plot1(self, data, p, ):
        # random data
        # data = [random.random() for i in range(10)]

        # clearing old figure
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # plot data
        H = ECDF(data)
        x = np.linspace(-0.20 * max(data), 1.20 * max(data), num=3 * len(data))
        y = 1 - np.power(1 - H(x), p)
        ax.plot(x, y, label='ACL-baho')
        ax.legend()
        # refresh canvas
        self.canvas.draw()


# driver code
if __name__ == '__main__':
    # creating apyqt5 application
    app = QApplication(sys.argv)

    # creating a window object
    main = Window()

    # showing the window
    main.show()

    # loop
    sys.exit(app.exec_())

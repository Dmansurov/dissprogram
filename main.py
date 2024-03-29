import sys

import numpy as np
import pandas as pd
import scipy.stats as st
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QPushButton, QFileDialog, QLabel, \
    QComboBox, QDoubleSpinBox, QSpinBox, QMessageBox, QWidget, QPlainTextEdit
from statsmodels.distributions import ECDF

from Criterion import Criterion, Statistika_qiymati
from mplwidget import Window


class Windows(QMainWindow):
    def __init__(self):
        super(Windows, self).__init__()

        self.cursor = None
        self.eee3 = None
        self.senzur3 = None
        self.tt3 = []
        self.fx3 = []
        self.params = tuple([])
        self.df = []
        self.all_data = None
        self.ECDF = []
        self.distributions = ['barchasi', 'alpha', 'arcsine', 'argus', 'beta', 'betaprime', 'bradford', 'burr',
                              'burr12', 'chi',
                              'chi2', 'erlang', 'expon', 'exponpow', 'exponweib', 'f', 'fatiguelife', 'fisk',
                              'foldcauchy', 'foldnorm', 'gamma', 'gausshyper', 'genexpon', 'gengamma',
                              'genhalflogistic', 'geninvgauss', 'genpareto', 'gilbrat', 'gompertz', 'halfcauchy',
                              'halfgennorm', 'halflogistic', 'halfnorm', 'invgamma', 'invgauss', 'invweibull',
                              'johnsonsb', 'kappa3', 'kappa4', 'ksone', 'kstwo', 'kstwobign', 'levy', 'loglaplace',
                              'lognorm', 'lomax', 'maxwell', 'mielke', 'nakagami', 'ncf', 'ncx2', 'pareto', 'powerlaw',
                              'powerlognorm', 'rayleigh', 'recipinvgauss', 'rice', 'trapezoid', 'trapz', 'triang',
                              'truncexpon', 'uniform', 'wald', 'weibull_min']

        # UI faylni o'qib olish
        uic.loadUi('ACL.ui', self)

        self.setWindowTitle('ACL bahosi')
        # Kerakli ob'yektlarni yuklab olish
        self.pushbutton11 = self.findChild(QPushButton, 'pushButton11')
        self.pushbutton12 = self.findChild(QPushButton, 'pushButton12')
        self.pushbutton13 = self.findChild(QPushButton, 'pushButton13')
        self.pushbutton21 = self.findChild(QPushButton, 'pushButton21')
        self.pushbutton22 = self.findChild(QPushButton, 'pushButton22')
        self.pushbutton23 = self.findChild(QPushButton, 'pushButton23')
        self.pushbutton31 = self.findChild(QPushButton, 'pushButton31')
        self.pushbutton32 = self.findChild(QPushButton, 'pushButton32')
        self.pushbutton33 = self.findChild(QPushButton, 'pushButton33')
        self.label13 = self.findChild(QLabel, 'label13')
        self.label14 = self.findChild(QLabel, 'label14')
        self.label15 = self.findChild(QLabel, 'label15')
        self.label16 = self.findChild(QLabel, 'label16')
        self.label21 = self.findChild(QLabel, 'label21')
        self.tableview1 = self.findChild(QTableWidget, 'tableWidget11')
        self.tableview2 = self.findChild(QTableWidget, 'tableWidget21')
        self.tableview3 = self.findChild(QTableWidget, 'tableWidget31')
        self.combobox11 = self.findChild(QComboBox, 'comboBox11')
        self.combobox31 = self.findChild(QComboBox, 'comboBox31')
        self.doublespinbox11 = self.findChild(QDoubleSpinBox, 'doubleSpinBox11')
        self.doublespinbox12 = self.findChild(QDoubleSpinBox, 'doubleSpinBox12')
        self.doublespinbox13 = self.findChild(QDoubleSpinBox, 'doubleSpinBox13')
        self.doublespinbox14 = self.findChild(QDoubleSpinBox, 'doubleSpinBox14')
        self.doublespinbox15 = self.findChild(QDoubleSpinBox, 'doubleSpinBox15')
        self.doublespinbox16 = self.findChild(QDoubleSpinBox, 'doubleSpinBox16')
        self.plainText31 = self.findChild(QPlainTextEdit, 'plainTextEdit31')
        self.spinbox11 = self.findChild(QSpinBox, 'spinBox11')
        self.spinbox12 = self.findChild(QSpinBox, 'spinBox12')
        self.spinbox11.setRange(100, 10000)
        self.MplWidget = self.findChild(QWidget, 'widget')
        self.MplWidget1 = self.findChild(QWidget, 'widget_2')
        self.element = Window(self.MplWidget)
        self.element1 = Window(self.MplWidget1)

        self.combobox11.addItems(self.distributions[1:])
        self.combobox31.addItems(self.distributions)
        self.combobox11.activated.connect(self.Taqsimot)

        self.label13.hide()
        self.label14.hide()
        self.label15.hide()
        self.label16.hide()
        self.label17.hide()
        self.label18.hide()
        self.doublespinbox11.hide()
        self.doublespinbox12.hide()
        self.doublespinbox13.hide()
        self.doublespinbox14.hide()
        self.doublespinbox15.hide()
        self.doublespinbox16.hide()

        self.pushbutton11.setEnabled(False)
        self.pushbutton12.setEnabled(False)
        self.pushbutton22.setEnabled(False)
        self.pushbutton23.setEnabled(False)
        self.pushbutton32.setEnabled(False)
        self.pushbutton33.setEnabled(False)
        self.spinbox11.valueChanged.connect(self.Sensorship)
        self.pushbutton11.clicked.connect(self.Tanlanma)
        self.pushbutton12.clicked.connect(self.Saqlash)
        self.pushbutton21.clicked.connect(self.yuklash)
        self.pushbutton31.clicked.connect(self.yuklash)
        self.pushbutton32.clicked.connect(self.button32)
        self.pushbutton33.clicked.connect(self.button33)

        # self.slider1.valueChanged.connect(self.slide_it1)
        # self.slider2.valueChanged.connect(self.slide_it2)

        # App ni ko'rsatish
        self.show()

    def button33(self):
        try:
            path3 = QFileDialog.getSaveFileName(self, "Tanlanmani saqlash", "", "Text (*.txt)")
            print(path3)
            with open(path3[0], 'w') as yourFile:
                yourFile.write(str(self.plainText31.toPlainText()))
        except:
            QMessageBox.warning(self, "Saqlashdagi xatolik!",
                                "Natijalarni saqlamadingiz yoki saqlashda xatolikga yo'l qo'ydingiz!")

    def button32(self):
        if self.combobox31.currentText() == 'barchasi':
            SSS = "Taqsimot    qiymatdorlik darajasi\n"
            for ij in range(1, 63):
                distributi = getattr(st, self.distributions[ij])
                params = np.ones(distributi.numargs)
                distributio = distributi(*params)
                statcriterion = Statistika_qiymati(self.tt3, np.mean(self.eee3), distributio)
                SSS = SSS + '{}:    {}\n'.format(self.distributions[ij], 1 - self.fx3.distribution.cdf(statcriterion))
            self.plainText31.setPlainText(SSS)
            self.pushbutton33.setEnabled(True)
        else:
            distributi = getattr(st, self.combobox31.currentText())
            params = np.ones(distributi.numargs)
            distributio = distributi(*params)
            statcriterion = Statistika_qiymati(self.tt3, np.mean(self.eee3), distributio)
            SSS = '{}:    {}\n'.format(self.combobox31.currentText(), 1 - self.fx3.distribution.cdf(statcriterion))
            self.plainText31.setPlainText(SSS)
            self.pushbutton33.setEnabled(True)

    def Sensorship(self):
        self.spinbox12.setRange(0, int(0.8 * self.spinbox11.value()))
        self.spinbox12.setValue(0)

    def yuklash(self, data):
        try:
            if self.sender() == self.pushbutton11:
                self.tablevieww = self.tableview1
                self.all_data = data
                self.pushbutton12.setEnabled(True)
            elif self.sender() == self.pushbutton21:
                self.tablevieww = self.tableview2
                path = QFileDialog.getOpenFileName(self, "Tanlanma faylini yuklash", "",
                                                   "Excel file (*.xlsx *.xls)")[0]  # os.getenv('HOME')
                self.all_data = pd.read_excel(path)
                self.element1.plot1(self.all_data['T'], np.mean(self.all_data['E']))
                # self.pushbutton22.setEnabled(True)
            elif self.sender() == self.pushbutton31:
                self.tablevieww = self.tableview3
                path = QFileDialog.getOpenFileName(self, "Tanlanma faylini yuklash", "",
                                                   "Excel file (*.xlsx *.xls)")[0]  # os.getenv('HOME')
                self.all_data = pd.read_excel(path)
                # self.criterion(self.all_data)
                self.tt3 = self.all_data["T"].to_numpy()
                self.eee3 = self.all_data["E"].to_numpy()
                self.senzur3 = len(self.eee3) - np.sum(self.eee3)
                self.plainText31.setPlainText("Iltomos, kuting. Tanlanmaga mos limit taqsimot yaratilmoqda...")
                self.fx3 = Criterion(self.senzur3, len(self.eee3))
                self.pushbutton32.setEnabled(True)
                self.plainText31.setPlainText("'Kriteriyni hisoblash' tugmachasini bosing.")
            NumRows = len(self.all_data.index)
            self.tablevieww.setColumnCount(len(self.all_data.columns))
            self.tablevieww.setRowCount(NumRows)
            self.tablevieww.setHorizontalHeaderLabels(self.all_data.columns)

            for i in range(NumRows):
                for j in range(len(self.all_data.columns)):
                    self.tablevieww.setItem(i, j, QTableWidgetItem(str(self.all_data.iat[i, j])))

            self.tablevieww.resizeColumnsToContents()
            self.tablevieww.resizeRowsToContents()

        except:
            self.tablevieww.clear()
            QMessageBox.warning(self, 'Yuklashdagi xatolik!',
                                "Fayl .xlsx kengaymali emas yoki yuklashda noma'lum xatolik yuz berdi!")

    def Random(self, senzur, n):
        tetta = senzur / (n - senzur)
        Ftanlanma = st.expon.isf(1 - st.uniform.rvs(size=n))
        if tetta != 0:
            Gtanlanma = st.expon.isf(np.power((1 - st.uniform.rvs(size=n)), 1 / tetta))
        else:
            Gtanlanma = np.full(n, np.inf)
        E = np.zeros(n)
        E[Ftanlanma <= Gtanlanma] = 1
        if n - np.sum(E) == senzur:
            T = np.fmin(Ftanlanma, Gtanlanma)
        else:
            self.Random(self, n)
        return T, np.mean(E)

    def criterion(self, data1):
        print(self.combobox31.currentText())
        dis = getattr(st, self.combobox31.currentText())
        print(dis)
        n = len(data1['T'])
        TT = np.array([])
        for i in range(5000):
            T, pn = self.Random(n - np.sum(data1['E']), n)
            H = ECDF(T)
            H1 = ECDF(T, side="left")
            Baho = lambda xx: 1 - np.power(1 - H(xx), pn)
            Baho1 = lambda xx: 1 - np.power(1 - H1(xx), pn)
            a = np.max(np.abs(dis.cdf(T) - Baho(T)))
            b = np.max(np.abs(dis.cdf(T) - Baho1(T)))
            TT = np.append(np.fmax(a, b), TT)
        Z = (np.sqrt(n / np.log(np.log(n)))) * TT
        self.ECDF = ECDF(Z)

    def Taqsimot(self):
        self.params = []
        self.label13.hide()
        self.label14.hide()
        self.label15.hide()
        self.label16.hide()
        self.label17.hide()
        self.label18.hide()
        self.doublespinbox11.hide()
        self.doublespinbox12.hide()
        self.doublespinbox13.hide()
        self.doublespinbox14.hide()
        self.doublespinbox15.hide()
        self.doublespinbox16.hide()
        self.distribution = getattr(st, self.combobox11.currentText())
        if self.distribution.numargs != 0:
            self.aa = self.distribution.shapes.split(', ')
        if self.distribution.numargs == 0:
            self.label17.show()
            self.label18.show()
            self.doublespinbox15.show()
            self.doublespinbox16.show()
        elif self.distribution.numargs == 1:
            self.label13.show()
            self.label13.setText(self.aa[0] + ':')
            self.label17.show()
            self.label18.show()
            self.doublespinbox11.show()
            self.doublespinbox15.show()
            self.doublespinbox16.show()
            self.params.append(self.doublespinbox11.value())
        elif self.distribution.numargs == 2:
            self.label13.show()
            self.label13.setText(self.aa[0] + ':')
            self.label14.show()
            self.label14.setText(self.aa[1] + ':')
            self.label17.show()
            self.label18.show()
            self.doublespinbox11.show()
            self.doublespinbox12.show()
            self.doublespinbox15.show()
            self.doublespinbox16.show()
            self.params.append(self.doublespinbox11.value())
            self.params.append(self.doublespinbox12.value())
        elif self.distribution.numargs == 3:
            self.label13.show()
            self.label13.setText(self.aa[0] + ':')
            self.label14.show()
            self.label14.setText(self.aa[1] + ':')
            self.label15.show()
            self.label15.setText(self.aa[2] + ':')
            self.label17.show()
            self.label18.show()
            self.doublespinbox11.show()
            self.doublespinbox12.show()
            self.doublespinbox13.show()
            self.doublespinbox15.show()
            self.doublespinbox16.show()
            self.params.append(self.doublespinbox11.value())
            self.params.append(self.doublespinbox12.value())
            self.params.append(self.doublespinbox13.value())
        elif self.distribution.numargs == 4:
            self.label13.show()
            self.label13.setText(self.aa[0] + ':')
            self.label14.show()
            self.label14.setText(self.aa[1] + ':')
            self.label15.show()
            self.label15.setText(self.aa[2] + ':')
            self.label16.show()
            self.label16.setText(self.aa[3] + ':')
            self.label17.show()
            self.label18.show()
            self.doublespinbox11.show()
            self.doublespinbox12.show()
            self.doublespinbox13.show()
            self.doublespinbox14.show()
            self.doublespinbox15.show()
            self.doublespinbox16.show()
            self.params.append(self.doublespinbox11.value())
            self.params.append(self.doublespinbox12.value())
            self.params.append(self.doublespinbox13.value())
            self.params.append(self.doublespinbox14.value())
        self.pushbutton11.setEnabled(True)

    def Tanlanma(self):
        n = self.spinbox11.value()
        senzur = self.spinbox12.value()
        tetta = senzur / (n - senzur)
        self.loc = self.doublespinbox15.value()
        self.scale = self.doublespinbox16.value()
        self.paramss = tuple(self.params)
        Ftanlanma = self.distribution.isf(1 - st.uniform.rvs(size=n), *self.paramss, loc=self.loc,
                                          scale=self.scale)
        if tetta != 0:
            Gtanlanma = self.distribution.isf(np.power((1 - st.uniform.rvs(size=n)), 1 / tetta), *self.paramss,
                                              loc=self.loc,
                                              scale=self.scale)
        else:
            Gtanlanma = np.full(n, np.inf)
        E = np.zeros(n)
        E[Ftanlanma <= Gtanlanma] = 1
        if n - np.sum(E) == senzur:
            T = np.fmin(Ftanlanma, Gtanlanma)
            abc = self.element.plot(T, np.mean(E), getattr(st, self.combobox11.currentText()), self.paramss,
                                    self.loc, self.scale)
            d = {'T': T, 'E': E, 'distribution': abc[0], 'paramss': abc[1], 'loc': abc[2], 'scale': abc[3]}
            self.df = pd.DataFrame(d)
            self.yuklash(self.df)

        else:
            self.Tanlanma()

    def Saqlash(self):
        try:
            path1 = QFileDialog.getSaveFileName(self, "Tanlanmani saqlash", "", "Excel (*.xlsx)")
            self.df.to_excel(path1[0])

        except:
            QMessageBox.warning(self, 'Saqlashdagi xatolik!',
                                "Tanlanmani saqlamadingiz yoki saqlashda xatolikga yo'l qo'ydingiz!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Oyna = Windows()
    sys.exit(app.exec_())

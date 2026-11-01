import math
import re
import sys

from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QApplication, QMainWindow

form_class = loadUiType("SimpleCalc.ui")[0]


class CalcClass(QMainWindow, form_class):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        nums = [
            self.b0,
            self.b1,
            self.b2,
            self.b3,
            self.b4,
            self.b5,
            self.b6,
            self.b7,
            self.b8,
            self.b9,
        ]
        for number in nums:
            number.clicked.connect(self.Nums)

        self.bDel.clicked.connect(self.bDelClick)
        self.bClear.clicked.connect(self.bClearClick)
        self.bRun.clicked.connect(self.bRunClick)

        self.bPlus.clicked.connect(self.bPlusClick)
        self.bMinus.clicked.connect(self.bMinusClick)
        self.bMult.clicked.connect(self.bMultClick)
        self.bDivide.clicked.connect(self.bDevideClick)
        self.bDot.clicked.connect(self.bDotClick)

        self.bSqr.clicked.connect(self.bSqrClick)
        self.bNsqr.clicked.connect(self.bNsqrClick)
        self.bAbs.clicked.connect(self.bAbsClick)
        self.bRoot.clicked.connect(self.bRootClick)
        self.bNroot.clicked.connect(self.bNrootClick)
        self.bPie.clicked.connect(self.bPieClick)
        self.bSin.clicked.connect(self.bSinClick)
        self.bCos.clicked.connect(self.bCosClick)
        self.bTan.clicked.connect(self.bTanClick)
        self.bLslide.clicked.connect(self.bLslideClick)
        self.bRslide.clicked.connect(self.bRslideClick)
        self.bCom.clicked.connect(self.bComClick)

    def Nums(self):
        sender = self.sender()
        newNum = sender.text()
        if self.result.text() == "0":
            self.result.setText(newNum)
        else:
            self.result.setText(self.result.text() + newNum)

    def bDotClick(self):
        self.result.setText(self.result.text() + ".")

    def bPlusClick(self):
        self.result.setText(self.result.text() + "+")

    def bMinusClick(self):
        self.result.setText(self.result.text() + "-")

    def bDevideClick(self):
        self.result.setText(self.result.text() + "/")

    def bMultClick(self):
        self.result.setText(self.result.text() + "*")

    def bSqrClick(self):
        self.result.setText(self.result.text() + "^2")

    def bNsqrClick(self):
        self.result.setText(self.result.text() + "^")

    def bAbsClick(self):
        if self.result.text() == "0":
            self.result.setText("|")
        else:
            self.result.setText(self.result.text() + "|")

    def bRootClick(self):
        if self.result.text() == "0":
            self.result.setText("√")
        else:
            self.result.setText(self.result.text() + "√")

    def bNrootClick(self):
        self.result.setText(self.result.text() + "ⁿ√")

    def bPieClick(self):
        if self.result.text() == "0":
            self.result.setText("π")
        else:
            self.result.setText(self.result.text() + "π")

    def bSinClick(self):
        if self.result.text() == "0":
            self.result.setText("sin")
        else:
            self.result.setText(self.result.text() + "sin")

    def bCosClick(self):
        if self.result.text() == "0":
            self.result.setText("cos")
        else:
            self.result.setText(self.result.text() + "cos")

    def bTanClick(self):
        if self.result.text() == "0":
            self.result.setText("tan")
        else:
            self.result.setText(self.result.text() + "tan")

    def bLslideClick(self):
        if self.result.text() == "0":
            self.result.setText("(")
        else:
            self.result.setText(self.result.text() + "(")

    def bRslideClick(self):
        self.result.setText(self.result.text() + ")")

    def bComClick(self):
        self.result.setText(self.result.text() + ",")

    def bDelClick(self):
        text = self.result.text()
        if len(text) <= 1:
            self.result.setText("0")
        else:
            self.result.setText(text[:-1])

    def bClearClick(self):
        self.result.setText("0")

    def bRunClick(self):
        A = self.result.text()

        try:
            A = re.sub(r"(\d)(π|\(|sin|cos|tan|√)", r"\1*\2", A)

            # 2. n제곱근 변환 (예: 3ⁿ√8 -> ((8)**(1/3)))
            A = re.sub(
                r"(\d+)ⁿ√(\()?([^+\-*/()]+|\([^()]+\))(\)?)",
                r"((\3)**(1/\1))",
                A,
            )

            A = re.sub(r"sin(\d+(\.\d+)?)", r"math.sin(math.radians(\1))", A)
            A = re.sub(r"cos(\d+(\.\d+)?)", r"math.cos(math.radians(\1))", A)
            A = re.sub(r"tan(\d+(\.\d+)?)", r"math.tan(math.radians(\1))", A)

            A = re.sub(r"√(\d+(\.\d+)?)", r"math.sqrt(\1)", A)
            A = A.replace("√(", "math.sqrt(")

            A = A.replace("π", "math.pi")
            A = A.replace("^", "**")

            open_b = A.count("(")
            close_b = A.count(")")
            if open_b > close_b:
                A = A + (")" * (open_b - close_b))

            res = eval(A)

            if isinstance(res, float) and res.is_integer():
                self.result.setText(str(int(res)))
            else:
                self.result.setText(str(res))

        except Exception:
            self.result.setText("0")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = CalcClass(None)
    myWindow.show()
    app.exec_()
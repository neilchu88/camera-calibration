import sys
import os
import cv2
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from PyQt5 import QtWidgets, QtGui
from calibrate import Calibration


class MainWindow(QtWidgets.QWidget):  # 建立視窗基底
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("Camera Calibration")  # 設定視窗標題
        self.resize(1320, 720)  # 設定視窗大小(width,height)

    def initUI(self):
        self.a = 11  # 校正版格子數
        self.b = 10  # 校正版格子數
        self.chessboard_size = (self.a, self.b)  # 校正板大小
        self.grid_size = 125  # 校正版一格寬125mm
        self.image_list = pd.Series([1])

        layout = QtWidgets.QVBoxLayout()
        QPushButton = QtWidgets.QPushButton
        QComboBox = QtWidgets.QComboBox
        QLabel = QtWidgets.QLabel
        font = QtGui.QFont()

        self.loadImage = QPushButton("Load Image", self)
        self.loadImage.clicked.connect(
            lambda: Calibration.load_image(self, self.chessboard_size, self.grid_size)
        )
        self.loadImage.setGeometry(50, 50, 150, 30)

        self.intrinsicMatrix = QPushButton("Find Intrinsic Matrix", self)
        self.intrinsicMatrix.clicked.connect(lambda: Calibration.intrinsic_matrix(self))
        self.intrinsicMatrix.setGeometry(50, 100, 150, 30)

        self.showIntrinsicMatrix = QLabel(self)
        self.showIntrinsicMatrix.setGeometry(300, 0, 1000, 200)
        font.setPointSize(20)
        self.showIntrinsicMatrix.setFont(font)

        self.showDistortionCoefficient = QLabel(self)
        self.showDistortionCoefficient.setGeometry(300, 200, 1000, 150)
        font.setPointSize(20)
        self.showDistortionCoefficient.setFont(font)

        self.imageNumber = QComboBox(self)
        Calibration.image_number_adjust(self, self.image_list)
        self.imageNumber.setGeometry(50, 150, 150, 30)

        self.extrinsicMatrix = QPushButton("Find Extrinsic Matrix", self)
        self.extrinsicMatrix.clicked.connect(lambda: Calibration.extrinsic_matrix(self))
        self.extrinsicMatrix.setGeometry(50, 200, 150, 30)

        self.showExtrinsicMatrix = QLabel(self)
        self.showExtrinsicMatrix.setGeometry(300, 350, 1000, 200)
        font.setPointSize(20)
        self.showExtrinsicMatrix.setFont(font)

        self.reprojectionError = QPushButton("Reprojection Error", self)
        self.reprojectionError.clicked.connect(
            lambda: Calibration.reproject_error(self)
        )
        self.reprojectionError.setGeometry(50, 250, 150, 30)

        self.showReprojectionError = QLabel(self)
        self.showReprojectionError.setGeometry(300, 550, 1000, 150)
        font.setPointSize(20)
        self.showReprojectionError.setFont(font)

        self.undistortImage = QPushButton("Undistort Image", self)
        self.undistortImage.clicked.connect(lambda: Calibration.undistort_image(self))
        self.undistortImage.setGeometry(50, 300, 150, 30)

        self.setLayout(layout)
        self.show


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

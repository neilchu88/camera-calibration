import sys
import os
import cv2
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from PyQt5 import QtWidgets, QtGui


class Calibration:
    def __init__(self, chessboard_size, grid_size):
        self.chessboard_size = chessboard_size
        self.grid_size = grid_size
        self.mtx = []
        self.dist = []
        self.rvecs = []
        self.tvecs = []

    def image_number_adjust(self, image_list):
        # 調整下拉選單的照片數量
        self.imageNumber.clear()
        for i in range(image_list.size):
            self.imageNumber.addItem(str(i + 1))

    def load_image(self, chessboard_size, grid_size):
        folder = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Folder", "")
        if folder:
            # image_list是成功被讀取到的照片的路徑
            self.image_list = self.image_list.drop([0])
            found_image_list = pd.Series(
                [
                    os.path.join(folder, file)
                    for file in os.listdir(folder)
                    if file.lower().endswith(
                        (
                            ".jpg",
                            ".png",
                            ".bmp",
                        )
                    )
                ]
            )
            self.image_list = self.image_list.append(
                found_image_list, ignore_index=True
            )
            print(str(self.image_list.size) + "images are loaded")
            Calibration.image_number_adjust(self, self.image_list)

        # 開始計算內外參和畸變
        criteria = (
            cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
            30,
            0.01,
        )  # 細化棋盤影像角點位置的演算法的迭代終止標準 -->30次迭代後或角位置系畫在0.001之內

        objectpoints = np.zeros(
            (self.chessboard_size[0] * self.chessboard_size[1], 3), np.float32
        )  # 創造儲存objectpoints(校正板的世界座標)的空間
        objectpoints[:, :2] = np.mgrid[
            0 : self.chessboard_size[0], 0 : self.chessboard_size[1]
        ].T.reshape(
            -1, 2
        )  # 建立一個適合叫板世界座標的坐標系
        objectpoints = objectpoints * self.grid_size

        self.objpoints = []  # 建立儲存之後照片中三維世界校正板的座標
        self.imgpoints = []  # 建立儲存之後照片中二為世界校正板的座標
        self.corner_deteced = []

        for image in self.image_list:  # 依序讀照片
            img = cv2.imread(image)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (self.chessboard_size), None)
            # if found, add to objpoints and imgpoints
            if (
                ret == True
            ):  # ret為findChessboardCorner回傳的布林值，若回傳是True，代表成功找到規定的所有corners
                self.objpoints.append(objectpoints)
                corners2 = cv2.cornerSubPix(
                    gray, corners, (11, 11), (-1, -1), criteria
                )  # 進一步增加corners的精確性
                self.imgpoints.append(corners2)
                self.corner_deteced.append(1)
            else:
                self.corner_deteced.append(0)
        assert sum(self.corner_deteced) <= len(
            self.corner_deteced
        ), "too many picture cannot find chessboard corner"

        # 布林值、內部參數、畸變矩陣、選轉矩陣、平移矩陣
        ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(
            self.objpoints, self.imgpoints, gray.shape[::-1], None, None
        )  # 若有徒沒有找到corner，是否會出現gray.shape跟objectpoint沒有對上的問題
        return (self.mtx, self.dist, self.rvecs, self.tvecs)

    def intrinsic_matrix(self):
        self.showIntrinsicMatrix.setText("The Intrinsic Matrix is:\n" + str(self.mtx))
        self.showDistortionCoefficient.setText(
            "The Distortion Coefficient is:\n" + str(self.dist)
        )  # k1,k2,p1,p2,k3

    def extrinsic_matrix(self):
        selectedNumber = (
            int(self.imageNumber.currentText()) - 1
        )  # combobox選擇的數字對應回0開始的數列
        true_selected = (
            sum(self.corner_deteced[0 : int(self.imageNumber.currentText())]) - 1
        )  # combobox選擇的數字對應回有找到corner的list(objpoints)中的組
        rvec = self.rvecs[true_selected]
        tvec = self.tvecs[true_selected]

        if self.corner_deteced[selectedNumber] == 0:
            self.showExtrinsicMatrix.setText(
                "This Picture can't Find Chessboard Corners"
            )
        else:
            R, _ = cv2.Rodrigues(rvec)  # 將旋轉向量轉為旋轉矩陣
            extrinsicmatrix = np.hstack((R, tvec))  # 合併旋轉矩陣跟平移矩陣
            self.showExtrinsicMatrix.setText(
                "The Extrinsic Matrix is:\n" + str(extrinsicmatrix)
            )

    # 計算重投影誤差
    def reproject_error(self):
        selectedNumber = (
            int(self.imageNumber.currentText()) - 1
        )  # combobox選擇的數字對應回0開始的數列
        true_selected = (
            sum(self.corner_deteced[0 : int(self.imageNumber.currentText())]) - 1
        )

        error_list = pd.Series([], dtype="float64")

        for i in range(len(self.objpoints)):
            reproject_point, _ = cv2.projectPoints(
                self.objpoints[i], self.rvecs[i], self.tvecs[i], self.mtx, self.dist
            )  # 計算重投影點

            error = cv2.norm(self.imgpoints[i], reproject_point, cv2.NORM_L2) / len(
                reproject_point
            )  # 一張圖片的重投影誤差 =  一張圖片中每個角點的(照片中角點-重投影點)^2相加開根號再取平均
            error_list = error_list.append(pd.Series([error]), ignore_index=True)

        average_error = error_list.mean()  # 所有圖片的重投影誤差的平均
        standard_deviation_error = error_list.std()  # 所有圖片的重投影誤差的標準差

        if self.corner_deteced[selectedNumber] == 0:
            self.showReprojectionError.setText(
                "This Picture can't Find Chessboard Corners" + "\n"
                "The Average Error is:"
                + str(average_error)
                + "\n"
                + "The Standard Deviation Error is:"
                + str(standard_deviation_error)
            )

        else:
            self.showReprojectionError.setText(
                "The "
                + str(self.imageNumber.currentText())
                + " Image Reproject Error is:"
                + str(error_list[true_selected])
                + "\n"
                "The Average Error is:"
                + str(average_error)
                + "\n"
                + "The Standard Deviation Error is:"
                + str(standard_deviation_error)
            )

    # 還原相片
    def undistort_image(self):
        for image in self.image_list:  # 依序讀照片
            img = cv2.imread(image)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            h, w = img.shape[:2]

            newcameramtx, roi = cv2.getOptimalNewCameraMatrix(
                self.mtx, self.dist, (w, h), 1, (w, h)
            )  # alpha 介於0~1之間
            undistort_img = cv2.undistort(img, self.mtx, self.dist, None, newcameramtx)
            combine_img = np.hstack((img, undistort_img))

            plt.figure(figsize=(20, 20))  # set the size of the figure
            plt.imshow(cv2.cvtColor(combine_img, cv2.COLOR_BGR2RGB))
            plt.title("Original and Undistorted Images")
            plt.axis("off")
            plt.show()

# camera-calibration
using photo to calibrate camera
本校正使用張氏校正，參考論文< A Flexible New Technique for Camera Calibration >和 open cv網站:https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html

![image](https://github.com/neilchu88/camera-calibration/assets/156585010/08c981ad-97ff-45c5-ab8f-bc285bf8f858)


使用方法如下
1. 開啟gui.py
2. 按Load Image選擇有照片的檔案，可讀取(.jpg,.png,.bmp)，若超過一半的照片無法順利偵測校正版，會強制停止並印出"too many picture cannot find chessboard corner"
3. 按Find Intrinsic Matrix得到相機的內部參數矩陣和畸變矩陣，其中畸變矩陣為[k1,k2,p1,p2,k3]
4. ComboBox選擇指定的照片
5. 按Find Extrinsic Matrix求得指定照片的外部參數，若該照片校正板無法順利被偵測，會出現"This Picture can't Find Chessboard Corners"
6. 按Reprojection Error求得指定照片的重投影誤差、重投影誤差平均和重投影誤差的標準差，若該照片校正板無法順利被偵測，會出現"This Picture can't Find Chessboard Corners"
7. 按Undistort Image得到按照內部參數及畸變矩陣復原的所有照片，其中alpha 設為1，可依照需求在calibrate.py的undistort_image函式中調整
> alpha = 0 : 校正後的圖像經縮放和移動，為了補滿設定的輸出圖片大小(部分的原始圖像訊息可能被移除)
> 
> alpha = 1 : 校正後的圖片被縮減和移動，以保留原圖像中的所有訊息(可能會有黑邊出現)
> 
> alpha介於0~1 : 保留原始圖像資訊跟不出現黑色邊緣之間




Usage Instructions

1. Open gui.py.
2. Click on 'Load Image' to select a file containing photos. The supported file formats are .jpg, .png, and .bmp. If more than half of the photos cannot be successfully detected or corrected, the process will be forcibly stopped, and the message "too many pictures cannot find chessboard corner" will be displayed.
3. Click on 'Find Intrinsic Matrix' to obtain the camera's intrinsic parameter matrix and distortion matrix. The distortion matrix consists of [k1, k2, p1, p2, k3].
4. Use the ComboBox to select a specific photo.
5. Click on 'Find Extrinsic Matrix' to determine the external parameters of the selected photo. If the calibration board in the photo cannot be successfully detected, the message "This Picture can't Find Chessboard Corners" will appear.
6. Click on 'Reprojection Error' to calculate the reprojection error, the average reprojection error, and the standard deviation of the reprojection error for the selected photo. If the calibration board in the photo cannot be successfully detected, the message "This Picture can't Find Chessboard Corners" will appear.
7. Click on 'Undistort Image' to view all the photos restored according to the intrinsic parameters and distortion matrix. The alpha is set to 1, but you can adjust it in the undistort_image function in calibrate.py as needed.
> alpha=0 means that the rectified images are zoomed and shifted so that only valid pixels are visible (no black areas after rectification). alpha=1 means that the rectified image is decimated and shifted so that all the pixels from the original images from the cameras are retained in the rectified images (no source image pixels are lost). Any intermediate value yields an intermediate result between those two extreme cases

import cv2
import numpy as np
import glob

# 设置棋盘格尺寸
chessboard_size = (5, 5)
# 设置棋盘格角点的世界坐标
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

# 储存所有标定图像的角点
objpoints = []  # 3D点
imgpoints = []  # 2D点

# 加载标定图像
images = glob.glob('./save_image/*.jpg')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 查找棋盘格角点
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)


    if ret:
        objpoints.append(objp)
        imgpoints.append(corners)
        # 绘制角点
        cv2.drawChessboardCorners(img, chessboard_size, corners, ret)
        cv2.imshow('img', img)
        cv2.waitKey(0)

cv2.destroyAllWindows()

# 标定相机
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
print('Following is the valuable you get:')
print('ret  =',ret,'\n')
print('mtx  =',mtx,'\n')
print('dist =',dist,'\n')
print('rvecs=',rvecs,'\n')
print('tvecs=',tvecs,'\n')

# 矫正图像
img = cv2.imread('./save_image/1.jpg')
h, w = img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

# 使用矫正后的相机矩阵
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

# 裁剪图像
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]

cv2.imshow('calibrated', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()

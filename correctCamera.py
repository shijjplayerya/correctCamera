import cv2 as cv
import numpy as np
import glob
import os
import shutil

def check_if_folder_exists(folder_name):  
    # 获取当前工作目录  
    current_directory = os.getcwd()  
      
    # 构造要检查的文件夹的完整路径  
    folder_path = os.path.join(current_directory, folder_name)  
      
    # 使用os.path.isdir()检查路径是否是一个存在的文件夹  
    if os.path.isdir(folder_path):  
        return True  
    else:  
        return False

chessboard_size = (5, 5)
# 设置棋盘格角点的世界坐标
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
# 储存所有标定图像的角点
objpoints = []  # 3D点
imgpoints = []  # 2D点

img_index = 0
save_path = 'save_image1'
if check_if_folder_exists(save_path):
    shutil.rmtree(save_path)
os.makedirs(save_path)

if __name__ == "__main__":

    cap = cv.VideoCapture(2)

    if not cap.isOpened():
        print("opening camera is FAIL")
        exit()
    ##
    print('-------------------------\n')
    print('Step 1 : Geting some images')
    print('-------------------------\n')
    while True:
        ret,frame = cap.read()
        if not ret:
            print("no image")
            break
        cv.imshow("Video", frame)  
        ## keyResponse
        waitkey = cv.waitKey(1)
        if waitkey & 0xFF == ord('s'):
            pic_path = save_path+'/'+str(img_index)+'.jpg'
            success = cv.imwrite(pic_path,frame)
            if success:
                print(str(img_index)+".jpg is successfully saved")
                img_index = img_index+1
            else:
                print("Saveing image is failed")
    
        elif waitkey & 0xFF == ord('q'):
            break
    
    ## Release the resources
    cap.release()
    cv.destroyAllWindows()

    ## 
    print('-------------------------\n')
    print('Step 2 : Geting the value')
    print('-------------------------\n')
    # get the image
    images = glob.glob('./'+save_path+'/*.jpg')
    for fname in images:
        img = cv.imread(fname)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        
        # 查找棋盘格角点
        ret, corners = cv.findChessboardCorners(gray, chessboard_size, None)

        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)
            # 绘制角点
            cv.drawChessboardCorners(img, chessboard_size, corners, ret)
            cv.imshow('img', img)
            cv.waitKey(0)
    
    cv.destroyAllWindows()

    # 标定相机
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    print('Following is the valuable you get:')
    print('ret  =',ret,'\n')
    print('mtx  =',mtx,'\n')
    print('dist =',dist,'\n')
    print('rvecs=',rvecs,'\n')
    print('tvecs=',tvecs,'\n')

    ## 矫正一个实例图像
    img = cv.imread('./'+save_path+'/1.jpg')
    h, w = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

    # 使用矫正后的相机矩阵
    dst = cv.undistort(img, mtx, dist, None, newcameramtx)

    # 裁剪图像
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]

    cv.imshow('calibrated', dst)
    cv.waitKey(0)
    cv.destroyAllWindows()
    
    commend = input('Do you want to save the image generated in this process.(y/N)\n')
    if commend == 'y' or commend == 'Y':
        print('OK, I will save these images')
    else:
        shutil.rmtree(save_path)
    print("\n---------------\nHave Released All Resources!\n-----------------")
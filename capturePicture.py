### 截图 ###
# 运行程序后,按下"s",截取图像
# 运行程序后,按下"q",退出程序
#! 如果运行路径下存在重要的同名的"save_image"记得更改变量save_path
#! 否则会自动删除该文件夹
import cv2 as cv
import numpy as np
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
 
img_index = 0
save_path = 'save_image'
if check_if_folder_exists(save_path):
    shutil.rmtree(save_path)
os.makedirs(save_path)

if __name__ == "__main__":

    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("opening camera is FAIL")
        exit()
    print('------------Instruction-------------\n')
    print('- press \'s\' to save a image in path',save_path)
    print('- press \'q\' to exit the process')
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
    print("\n---------------\nHave Released All Resources!\n-----------------")

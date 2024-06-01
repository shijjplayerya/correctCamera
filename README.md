# 相机图像矫正

## 说明
仓库下有三个Python脚本
### capturePicture.py 
截图,把图像保存到指定路径
### demo_correcCamera.py
单纯地计算畸变参数,如果你已经获取了标定图像,运行该代码
### correctCamera.py
保存标定图像,后计算畸变参数.如果你没有标定图像,运行该代码
这个脚本相当于将前两个脚本结合起来

## 准备工作
+ 安装Opencv-Python
+ 相机(可以是笔记本相机,也可usb连接的相机,但是要注意更改video.capture()这句代码的参数)




# 简介
- 本项目是针对在ROS多机通信从机端订阅原始相机卡顿的问题而衍生的
- 在ROS多机通信的图像传输中使用了JPEG图像压缩
- 投稿于《传感器与微系统》
# 操作步骤
### 发送端（主机端）
```
mkdir compress_img && cd compress_img
mkdir src && cd src
git clone https://github.com/LeonardoDiCaprio1/compressed_image.git
cd /compressed_image/master/compress_image/scripts
chmod +x compress.py
cd
cd compressed_image
catkin_make
```
### 接收端（从机端）
```
mkdir uncompress_img && cd uncompress_img
mkdir src && cd src
git clone https://github.com/LeonardoDiCaprio1/compressed_image.git
cd /compressed_image/serve/uncompress_image/scripts
chmod +x *.py
cd
cd compressed_image
catkin_make
```
# 使用说明
### 主机端
- 压缩原始相机话题
```
source devel/setup.bash
roslaunch compress_image compress.launch
```
### 从机端
- 解压压缩后的相机话题
```
source devel/setup.bash
roslaunch uncompress_image uncompress.launch
```
- 监听压缩后的相机话题或原始相机话题
```
source devel/setup.bash
rosrun uncompress_image img_monitor.py
```

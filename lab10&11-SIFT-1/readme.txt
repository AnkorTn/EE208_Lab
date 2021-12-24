压缩包结构：
519030910100_王煌基_v1.zip
	-\codes
	-\output_with_cv2
	-\output_with_myself
	-\dataset
	-data3.jpg
	-readme.txt
	-report.pdf

本次codes由两份代码构成：
	CV_SIFT.py利用OpenCV自带函数实现SIFT
	SIFT.py利用自己实现的SIFT函数实现
	
	如需运行py文件（imgname1默认是data3.jpg可以不用修改）
	对于CV_SIFT.py则需要改变imgoutname、imgname2
	对于SIFT.py则须改变第175行的imgpkp0以及228行的cv2.write
	


本次还附上\output_with_cv2和\output_with_myself，是输出结果，可直接查看。
本次还附上\dataset，是输入数据，方便直接调用py文件。
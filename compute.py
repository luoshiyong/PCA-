#使用PCA实现人脸识别
from PIL import Image
from PIL import ImageDraw
import numpy
#import cv
from  PyQt5.QtWidgets import *
import os
import sys
train_path = 'D:/pythoncode/PCAface/TrainDatabase/'
test_path = 'D:/pythoncode/PCAface/TestDatabase/'

filename1 = os.listdir(train_path)
filename1.remove('Thumbs.db')
filename1.sort(key= lambda x:int(x[:-4]))
filename2 = os.listdir(test_path)
filename2.remove('Thumbs.db')
filename2.sort(key= lambda x:int(x[:-4]))
class PCA():
    def CreateDataset(self,path, number):
        #读取图片成为一个矩阵
        Matrix = []
        for i in range(0,number):
            img_path = path+filename1[i]
            img = Image.open(img_path)   #256*384
            #print(img_path)
            #print(img.size)
            imgArray = list(img.getdata())#转换为一个一维数组，按照行排列
            #print(len(imgArray))   98304
            Matrix.append(imgArray)        
        #print(len(Matrix))    
        Matrix = numpy.array(Matrix)  #转换为二维矩阵,20*98304
        #print(Matrix.shape)  
        return Matrix
    def eigenfaceCore(self,Matrix):
        ct, lensize = numpy.shape(Matrix) #返回图像的个数，和每个图像的大小
        #print(ct,lensize)
        #
        meanArray = Matrix.mean(0) #0按照列计算平均矩阵 (98304,)
        #计算每个向量与平均向量的差
        dif = Matrix - meanArray       #(20, 98304)
        #计算协方差矩阵
        dif = numpy.mat(dif)#创建矩阵类型的数据
        L = dif * dif.T 
        print("协方差矩阵:",L.shape)
        eigvalues, eigvectors = numpy.linalg.eig(L) #特征向量v[:,i]对应特征值w[i]

        #然后按照特征值大于1来提取特征向量
        eigvectors = list(eigvectors.T) #因为特征向量矩阵的每列是一个特征向量，
                                        #所以需要转置后，变为一个list,然后通过pop方法，
                                        #删除其中的一行，再逆变换转回去
        for i in range(0,20):
            if eigvalues[i] < 1:
                eigvectors.pop(i)
            
        eigvectors = numpy.array(eigvectors) 
        eigvectors = numpy.mat(eigvectors).T        
     
    
        #最后计算特征脸,也就是计算出C

        print(dif.shape)
        #print(eigvectors.shape) #(20, 19)
        eigfaces = dif.T * eigvectors #(98304, 19)
        print("eigfaces = " ,eigfaces.shape)
        return eigfaces   #(98304, 19)
    def recognize(self,testIamge, Matrix, eigenface):
        #testIamge,为进行识别的测试图片
        #Matrix为所有图片构成的矩阵20*98304
        #eigenface为特征脸(98304, 19)
        #返回识别出的文件的行号
       
        #按照列计算平均向量
        meanArray = Matrix.mean(0) #0按照列计算平均  20*98304
    
        #计算每个向量与平均向量的差
        dif = Matrix - meanArray   #20*98304
    
        #确定经过过滤后的图片数目
        perTotal, trainNumber = numpy.shape(eigenface)   #(98304, 19)
        #将每个样本投影到特征空间
        projectedImage = eigenface.T * dif.T  #(19, 20)
        #print("projectedImage = ",projectedImage.shape)
        #处理测试图片，将其映射到特征空间上
        testimage = Image.open(testIamge)
        testImageArray = list(testimage.getdata())#转换为一个一维数组，按照行排列
        testImageArray = numpy.array(testImageArray)
    
        dif_test = testImageArray - meanArray
        #转换为矩阵
        dif_test_array = numpy.array(dif_test)
        dif_test_mat = numpy.mat(dif_test_array)
        #print("dif_test_mat = ",dif_test_mat.shape) #测试图片展成(1, 98304)
        projectedTestImage = eigenface.T * dif_test_mat.T
        print("the testimage size(pca) is ",projectedTestImage.shape)#转换到特征空间(19, 1)
 
        """按照欧式距离计算最匹配的人脸"""
        distance = []
        for i in range(0, 20): #projectedImage【19，20】
            q = projectedImage[:,i]   #样本库中的第第i列（一共20列）
            temp = numpy.linalg.norm(projectedTestImage - q) #计算范数
            distance.append(temp)
  
        minDistance = min(distance)
        index = distance.index(minDistance)     
        return index+1 #数组index是从0开始的 

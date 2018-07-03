# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 20:03:39 2018

@author: admin
"""
import tensorflow as tf
import numpy as np
from tensorflow.python.framework import ops
import matplotlib.pyplot as plt 
import datetime
import os
import csv
#import model0

def accuracy(predictions, labels):
  return (100.0 * np.sum(np.argmax(predictions, 1) == np.argmax(labels, 1))
          / predictions.shape[0])  

if __name__ == '__main__':
    
    datafile1 =u'Spectrumdata_mixture_air.npy'
    Xtest = np.load(datafile1) 
    datafile2 =u'ALL_label_mixture.npy'
    label = np.load(datafile2) 
    csv_reader = csv.reader(open('namedata.csv', encoding='utf-8'))
    names = [row for row in csv_reader]
    starttime = datetime.datetime.now()  
    ypred = np.zeros((label.shape[0]*label.shape[1],2))
    root = "C:/Users/admin/Desktop/DeepMA/model"
    list_dirs = os.walk(root) 
    i=0

    for root, dirs, files in list_dirs: 
        for d in dirs: 
            tf.reset_default_graph()
            Y1 = label[i,:].reshape([Xtest.shape[0],1])
            Y2 = np.ones((Y1.shape)) - Y1
            Ytest = np.concatenate((Y1,Y2),axis=1)
           
            os.chdir(os.path.join(root, d))
            datafile =u'./X_scale.npy'
            X_scale = np.load(datafile)
            Xtest_scale = (Xtest - X_scale[0])/X_scale[1]
            
            with tf.Session() as sess:

                new_saver=tf.train.import_meta_graph('./compoent.ckpt.meta')
                new_saver.restore(sess,"./compoent.ckpt")
                graph = tf.get_default_graph()

                xs=graph.get_operation_by_name('xs').outputs[0]
                ys=graph.get_operation_by_name('ys').outputs[0]
                keep_prob=graph.get_operation_by_name('keep_prob').outputs[0]
                prediction = graph.get_tensor_by_name('prediction:0')
                test_ypred = sess.run(prediction,feed_dict={xs: Xtest_scale, ys: Ytest, keep_prob : 1.0})  
            ypred[i*label.shape[1]:(i+1)*label.shape[1],:] = test_ypred
            print('compoent', i, 'finished.','The accuracy %.1f%%' % 
                  accuracy(ypred[i*label.shape[1]:(i+1)*label.shape[1],:],Ytest))           
            i+=1
    
    for j in range(Xtest.shape[0]):
        print('The', j ,'th sample contains: ')
        y_real1 = label[:,j].reshape([label.shape[0],1])
        
        y_real2 = np.ones((y_real1.shape)) - y_real1
        y_real = np.concatenate((y_real1,y_real2),axis=1)
        ypre = np.zeros((label.shape[0],2))
        for k in range(label.shape[0]):            
            ypre[k,:] = ypred[j,:]
            j = j+Xtest.shape[0]
        
        for h in range(label.shape[0]):
            if (ypre[h,0]>=0.5):
                print(names[h])                
        
    endtime = datetime.datetime.now()  
    print ('The time :',(endtime - starttime),".seconds")         
    
    
    
    
    
    
    
    
    
    
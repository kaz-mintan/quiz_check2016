import numpy as np
from conv_num import *

INPUT_DIM = 11
MID_UNIT = 15
OUTPUT_DIM = 4
EPOCH = 50000

NUM_MAX = 30
TEST_NUM = 25 #the number of test data is 10
SEQ_NUM = 5

username = ['inusan', 'kumasan', 'nekosan', 'test119', 'test120', 'test121', 'tomato', 'torisan', 'usagisan']

for i_name in username:
  print(i_name)
  tag_number = conv_num(i_name)

  #set input, output data to train

  xdata_b = "./jiken/" + i_name + "/factor_before.csv"
  x2data_b = "./jiken/" + i_name + "/kibun_before.csv"
  ydata_b = "./jiken/" + i_name + "/signal_before.csv"

  factor_b= np.loadtxt(xdata_b,delimiter='\t')
  mood_b = np.loadtxt(x2data_b,delimiter='\t')
  face_b= np.loadtxt(ydata_b,delimiter='\t')
  #x_train_b = np.hstack((x1_train_b,x2_train_b.reshape(-1,1)))

  factor = factor_b
  mood = mood_b
  face = face_b

  test_index = np.zeros(SEQ_NUM,dtype='int')

  for set_num in (5,10,15,20,25):
    test_index0 = np.random.choice(range(0, NUM_MAX-5),TEST_NUM,replace=False) #the first index to start 30 test data sequence.

    for i in range(TEST_NUM):
      test_index[0] = test_index0[i]
      for t in range(1,SEQ_NUM):
        test_index[t] = test_index[t-1]+1
      
      numbers = np.linspace(0,NUM_MAX-1,NUM_MAX,dtype='int')
      not_test_index = np.ones(len(numbers),dtype=bool)
      not_test_index[test_index] = False

      last_index = numbers[not_test_index]
      train_index = last_index[np.random.randint(0,NUM_MAX-SEQ_NUM,set_num)]

      print('test',test_index, 'train',train_index)

      ####################
      factor_train= factor[train_index,:]
      mood_train= mood[train_index]
      face_train= face[train_index,:]

      factor_test= factor[test_index,:]
      mood_test= mood[test_index]
      face_test= face[test_index,:]

      save_factor_train = "/home/kazumi/prog/quiz_check2016/jrm_test/"+str(tag_number)+"/factor_train"+str(set_num) + "-" +str(i)+".csv"
      save_mood_train = "/home/kazumi/prog/quiz_check2016/jrm_test/"+str(tag_number)+"/mood_train"+str(set_num) + "-" +str(i)+".csv"
      save_face_train = "/home/kazumi/prog/quiz_check2016/jrm_test/"+str(tag_number)+"/face_train"+str(set_num) + "-" +str(i)+".csv"
      np.savetxt(save_factor_train,factor_train,fmt='%.4f',delimiter=",")
      np.savetxt(save_mood_train,mood_train,fmt='%.4f',delimiter=",")
      np.savetxt(save_face_train,face_train,fmt='%.4f',delimiter=",")

      save_factor_test = "/home/kazumi/prog/quiz_check2016/jrm_test/"+str(tag_number)+"/factor_test"+str(set_num) + "-" +str(i)+".csv"
      save_mood_test = "/home/kazumi/prog/quiz_check2016/jrm_test/"+str(tag_number)+"/mood_test"+str(set_num) + "-" +str(i)+".csv"
      save_face_test = "/home/kazumi/prog/quiz_check2016/jrm_test/"+str(tag_number)+"/face_test"+str(set_num) + "-" +str(i)+".csv"
      np.savetxt(save_factor_test,factor_test,fmt='%.4f',delimiter=",")
      np.savetxt(save_mood_test,mood_test,fmt='%.4f',delimiter=",")
      np.savetxt(save_face_test,face_test,fmt='%.4f',delimiter=",")

      selected_test = "/home/kazumi/prog/quiz_check2016/jrm_test/" +str(tag_number) + "/selected_num_test"+str(set_num) + "-"+ str(i) + ".csv"
      selected_train = "/home/kazumi/prog/quiz_check2016/jrm_test/" +str(tag_number) + "/selected_num_train"+str(set_num) + "-"+ str(i) + ".csv"
      np.savetxt(selected_test,test_index,fmt='%2d',delimiter=",") 
      np.savetxt(selected_train,train_index,fmt='%2d',delimiter=",") 

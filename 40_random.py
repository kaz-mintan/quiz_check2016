import numpy as np
import scipy as sp
from scipy.stats import pearsonr

import matplotlib.pyplot as plt

for name_num in range(9):
  dir_name = "./jrm_test/" + str(name_num+1)
  for set_num in (5,10,15,20,25,30,35,40):
    #set_num = 35
    r = np.zeros(30)
    p = np.zeros(30)
    for i in range(30):#calculate the avelage value of estimated accuracy for datum in this loop
      i_csv = str(set_num) + "-" + str(i) + ".csv"

      mood_test = np.loadtxt(dir_name + "/mood_test" + i_csv ,delimiter=',')
      mood_est = np.random.rand(10)

      #pearson r
      r[i], p[i] = pearsonr(mood_test, mood_est)

      #diff[i] =np.mean(mood_test - mood_est/10.0)

    #test output
    np.savetxt(dir_name+"/rand_corr-"+str(set_num)+".csv",r,fmt='%.5f',delimiter=',')
    np.savetxt(dir_name+"/rand_p-"+str(set_num)+".csv",p,fmt='%.5f',delimiter=',')
    print(r)

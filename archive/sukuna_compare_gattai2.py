import numpy as np
import scipy as sp
from scipy.stats import pearsonr
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import iqr


test_len = 30

hito_num = 9

set_list = (5, 10, 15, 20, 25, 30)

nn_num = np.zeros((len(set_list),hito_num))
phi_num = np.zeros((len(set_list),hito_num))

nn_ave = np.zeros((len(set_list),hito_num))
phi_ave = np.zeros((len(set_list),hito_num))

nn_all = np.zeros((len(set_list),hito_num,test_len*2))
phi_all = np.zeros((len(set_list),hito_num,test_len*2))

phi_minmax = np.zeros((2,len(set_list),hito_num))

sum_ave = 0
sum_ave2 = 0
sum_ave3 = 0

for name_num in range(hito_num):
  dir_name = "./jrm_test/" + str(name_num+1)
  dir_name2 = "./jrm_test/third_test/" + str(name_num+1)

  for set_num in set_list:

    nn_corr1 = np.loadtxt(dir_name + "/nn_corr-" + str(set_num) + ".csv", delimiter=",")
    nn_corr2 = np.loadtxt(dir_name2 + "/nn_corr-" + str(set_num) + ".csv", delimiter=",")
    nn_p1 = np.loadtxt(dir_name + "/nn_p-" + str(set_num) + ".csv")
    nn_p2 = np.loadtxt(dir_name2 + "/nn_p-" + str(set_num) + ".csv")

    phi_corr1 = np.loadtxt(dir_name + "/phi_corr-" + str(set_num) + ".csv", delimiter=",")
    phi_corr2 = np.loadtxt(dir_name2 + "/phi_corr-" + str(set_num) + ".csv", delimiter=",")
    phi_p1 = np.loadtxt(dir_name + "/phi_p-" + str(set_num) + ".csv")
    phi_p2 = np.loadtxt(dir_name2 + "/phi_p-" + str(set_num) + ".csv")

    nn_corr = np.hstack((nn_corr1,nn_corr2))
    nn_p = np.hstack((nn_p1,nn_p2))
    #nn_corr = nn_corr/nn_p

    phi_corr = np.hstack((phi_corr1,phi_corr2))
    phi_p= np.hstack((phi_p1,phi_p2))
    #phi_corr = phi_corr/phi_p

    phi_corr[np.isnan(phi_corr)] = 0 
    nn_corr[np.isinf(phi_corr)] = 0 

    nn_all[set_num/5-1,name_num,:]= nn_corr
    phi_all[set_num/5-1,name_num,:]= phi_corr

    #nn_ave[set_num/5-1,name_num]= np.average(abs(nn_corr[~np.isnan(nn_corr)]))
    #phi_ave[set_num/5-1,name_num]= np.average(abs(phi_corr[~np.isnan(phi_corr)]))
    arr = phi_corr[~np.isnan(phi_corr)]

    #nn_ave[set_num/5-1,name_num]= np.average(abs(nn_corr[~np.isnan(nn_corr)]))
    #phi_ave[set_num/5-1,name_num]= np.average(abs(phi_corr[~np.isnan(phi_corr)]))
    #arr = phi_corr[~np.isnan(phi_corr)]

    nn_ave[set_num/5-1,name_num]= np.average((nn_corr[nn_corr>0]))
    phi_ave[set_num/5-1,name_num]= np.average((phi_corr[phi_corr>0]))
    #arr = phi_corr[~np.isnan(phi_corr)]

    #nn_ave[set_num/5-1,name_num]= iqr(abs(nn_corr[~np.isnan(nn_corr)]),axis=0)
    #phi_ave[set_num/5-1,name_num]= iqr(abs(phi_corr[~np.isnan(phi_corr)]),axis=0)
    #arr = phi_corr[~np.isnan(phi_corr)]


    #nn_ave[set_num/5-1,name_num]= np.var(abs(nn_corr[~np.isnan(nn_corr)]))
    #phi_ave[set_num/5-1,name_num]= np.var(abs(phi_corr[~np.isnan(phi_corr)]))
    #arr = phi_corr[~np.isnan(phi_corr)]

    #nn_ave[set_num/5-1,name_num]= np.var((nn_corr[nn_corr>0]))
    #phi_ave[set_num/5-1,name_num]= np.var((phi_corr[phi_corr>0]))
    #arr = phi_corr[~np.isnan(phi_corr)]

    nn_num[set_num/5-1,name_num] = np.count_nonzero(abs(nn_corr)>0.4)
    phi_num[set_num/5-1,name_num] = np.count_nonzero(abs(phi_corr)>0.4)

    vsjudge = 'count' + str(np.count_nonzero(abs(nn_corr)>0.2)) + "vs" + str(np.count_nonzero(abs(phi_corr)>0.2))
    vsave = 'ave'+str((nn_ave[set_num/5-2,name_num])) + "vs" + str((phi_ave[set_num/5-2,name_num]))

    left = np.arange(30)
    width = 0.3

    #g1=plt.bar(left,(nn_corr),color='b',label='nn_corr',width=width,align='center')
    #g2=plt.bar(left+width, (phi_corr), color='r',label='phi_corr', width=width, align='center')
    #plt.legend(handles=[g1,g2],loc='best',shadow=True)
    #plt.xlabel('set num')
    #plt.ylabel('correlation')
    #plt.ylim(0.2,1)
    #plt.title("no."+str(name_num) +"-"+ str(set_num)+"\n" + vsjudge+"\n" +vsave)
    #plt.show()

pave = np.zeros(len(set_list))
perr = np.zeros((2,len(set_list)))
nave = np.zeros(len(set_list))
nerr = np.zeros((2,len(set_list)))

plt.figure(figsize=(4,8))

print "datamake"

data_all=0

for i in range(len(set_list)):
  val = phi_all[i,:,:]
  pave[i] = iqr(val[~np.isnan(val)])
  perr[1,i] = abs(np.max(val[~np.isnan(val)])-pave[i])
  perr[0,i] = abs(pave[i]-np.min(val[~np.isnan(val)]))

  val = nn_all[i,:,:]
  nave[i] = iqr(val[~np.isnan(val)])
  nerr[1,i] = abs(np.max(nn_ave[i,:])-nave[i])
  nerr[0,i] = abs(nave[i]-np.min(nn_ave[i,:]))
  #print "val",val
  #print "ave",nave[i]


  for t in range(hito_num):
    data = np.zeros((test_len*2,1))
    index = np.ones((test_len*2,1))*(i+1)

    #index[:,0] = np.linspace(0,5,6)
    phi_ways = np.ones((test_len*2,1))*99
    data[:,0] = phi_all[i,t,:]
    ##print ('index',index)
    #print ('phi_ways',phi_ways)
    #print ('phi_all',data)
    data_phi = np.hstack((index,phi_ways,data))

    data[:,0] = nn_all[i,t,:]
    nn_ways = np.ones((test_len*2,1))*88
    data_nn = np.hstack((index,nn_ways,data))


    df_phi = pd.DataFrame(data=data_phi,columns=["number","way","data"],dtype='float')
    df_nn = pd.DataFrame(data=data_nn,columns=["number","way","data"],dtype='float')
    #df_nn = pd.DataFrame(data=data_nn,columns=["number","way","0","1","2","3","4","5","6","7","8"],dtype='float')

    phi_melt = pd.melt(df_phi, id_vars=['number','way'],var_name='hito')
    nn_melt = pd.melt(df_nn, id_vars=['number','way'],var_name='hito')

    #print 'melt',phi_melt,nn_melt

    if i+t == 0:
      data_all = pd.concat([phi_melt,nn_melt])
    else:
      data_all = data_all.append(pd.concat([phi_melt,nn_melt]))


#data_phi = np.hstack((index,phi_ways,phi_ave))

data_all['way']=data_all['way'].astype(str)

data_all['way'].str.replace('99.0','phi')
data_all['way'].str.replace('88.0','nn')

sns.violinplot(x='number',y='value',hue='way',data=data_all,split=True,inner="stick",scale_hue=False,bw=.5)
#sns.swarmplot(x='number',y='value',hue='way',data=data,split=True)
#sns.despine(offset=10,trim=True)
#sns.boxplot(x='number',y='value',hue='way',data=data_all)

posi = np.linspace(0,6,6)
posi2 = np.linspace(0,6,6) + np.ones(6)*0.5

#g1 = plt.violinplot(phi_arr,posi,showmeans=True)
#g2 = plt.violinplot(nn_arr,posi2,showmeans=True)
#g1 = plt.boxplot(arr1)
#g2 = plt.boxplot(arr2)

#box
#g1=plt.errorbar(set_list,pave,yerr = 0.1)
plt.figure(figsize=(4,8))
g1=plt.plot(set_list,pave,color='r',label='phi',marker='o',linestyle='dashed')
g2=plt.plot(set_list,nave,color='b',label='nn',marker='o',linestyle='dashed')

print('pave',pave)
print('nave',nave)

#error bar
#g1=plt.errorbar(set_list,pave,yerr = perr, color='r',label='proposed method',marker='o',elinewidth=1,linestyle='dashdot',capsize=4)
#g2=plt.errorbar(set_list,nave,yerr=nerr,color='b',label='nn',marker='o',elinewidth=1,linestyle='dashed',capsize=4)
plt.xlabel('number of training data',fontsize=15)
plt.ylabel('var',fontsize=15)
plt.legend()
plt.show()
#plt.savefig('ave_matome.eps')

pcorr = np.zeros(len(set_list))
ncorr = np.zeros(len(set_list))

plt.figure(figsize=(4,8))

for i in range(len(set_list)):

  phi_num[set_num/5-1,name_num] = np.count_nonzero((phi_corr)>0.2)
  val2 = phi_num[i,:]
  print "npcount",np.count_nonzero(val2[~np.isnan(val2)])
  pcorr[i] = np.sum(val2)

  val2 = nn_num[i,:]
  ncorr[i] = np.sum(val2)

g1=plt.plot(set_list,pcorr,color='r',marker='o',label='proposed method',linestyle='dashdot')
g2=plt.plot(set_list,ncorr,color='b',marker='o',label='nn',linestyle='dashed')
plt.xlabel('number of training data',fontsize=15)
plt.ylabel('number of correlation larger than 0.4(abs)',fontsize=15)

plt.legend()
#plt.savefig('corr_matome.eps')
plt.show()

'''
for i in range(6):
  #print('nn_num',nn_num[i,:])
  print('phi_num',phi_ave[i])

  plt.figure(figsize=(8,4))

  left = np.arange(9)
  width = 0.3

  g1=plt.bar(left,phi_ave[i,:],color='pink',label='proposed method',width=width,align='center',tick_label=range(1,10))
  #g2=plt.bar(left+width, nn_ave[i,:], color='none',edgecolor='skyblue',hatch='//////////',label='neural network', width=width, align='center',tick_label=range(1,10))
  #plt.legend(handles=[g1,g2],loc='best',shadow=True,fontsize=10)
  plt.xlabel('user id',fontsize=12)
  plt.ylabel('the average of correlation',fontsize=12)
  #plt.ylabel('the number of correlation\n larger than 0.2',fontsize=12)
  #plt.ylim(0,7.3)
  #plt.title(str((i+1)*10))

  #plt.ylabel('count of up/keep')

  #plt.savefig(str(i)+'times_compare.eps')
  plt.show()
'''

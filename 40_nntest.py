import optuna

import keras.backend as K
from keras.models import Sequential, Model
from keras.layers import Input, Dense, Activation
from keras.layers.advanced_activations import LeakyReLU
import numpy as np
import scipy as sp
from scipy.stats import pearsonr

INPUT_DIM = 11
MID_UNIT = 15
OUTPUT_DIM = 4
EPOCH = 50000

for name_num in (0,1,2,3,4,5,6,7,8):
  dir_name = "./jrm_test/" + str(name_num+1)
  #for set_num in (5,10,15,20,25,30,35,40):
  for set_num in (25,26,27,28,29):

    r = np.zeros(29)
    p = np.zeros(29)
    for i in range(29):#calculate the avelage value of estimated accuracy for datum in this loop
      i_csv = str(set_num) + "-" + str(i) + ".csv"

      #set input, output data to train
      factor_train = dir_name + "/factor_train" + i_csv
      mood_train = dir_name + "/mood_train" + i_csv
      face_train = dir_name + "/face_train" + i_csv

      x1_train = np.loadtxt(factor_train,delimiter=',')
      x2_train = np.loadtxt(mood_train,delimiter=',')
      x_train = np.hstack((x1_train,x2_train.reshape(-1,1)))

      y_train = np.loadtxt(face_train,delimiter=',')

      def objective(trial):
        #セッションのクリア
        K.clear_session()

        #最適化するパラメータの設定
        #中間層のユニット数
        mid_units = trial.suggest_int("mid_units", 5, 100)

        #活性化関数
        activation = trial.suggest_categorical("activation", ["relu", "sigmoid", "tanh"])

        #optimizer
        optimizer = trial.suggest_categorical("optimizer", ["sgd", "adam", "rmsprop"])

        #define NN framework
        model = Sequential()
        model.add(Dense(mid_units, input_dim = INPUT_DIM, activation=activation))
        model.add(Dense(OUTPUT_DIM, activation=activation))

        model.compile(optimizer=optimizer,
              loss="mean_squared_error",
              metrics=["accuracy"])

        history = model.fit(x_train, y_train, verbose=0, epochs=200, batch_size=128, validation_split=0.1)
        return 1 - history.history["val_acc"][-1]

      study = optuna.create_study()
      study.optimize(objective, n_trials=100)

      mid_units=study.best_params["mid_units"]
      activation=study.best_params["activation"]
      optimizer=study.best_params["optimizer"]

      best_params = ["mid_units:",str(mid_units),",activation:" ,activation,",optimizer:",optimizer]
      path_w  = dir_name+"/nn_best_params"+str(set_num)+"-"+str(i)+".txt"
      with open(path_w, mode='w') as f:
          f.writelines(best_params)

      #define NN framework
      model = Sequential()
      model.add(Dense(mid_units, input_dim = INPUT_DIM, activation=activation))
      model.add(Dense(OUTPUT_DIM, activation=activation))

      model.compile(optimizer=optimizer,
            loss="mean_squared_error",
            metrics=["accuracy"])

      train=model.fit(x=x_train, y=y_train, nb_epoch=EPOCH)
      model.save(dir_name+"/nn_model"+str(set_num)+"-"+str(i)+".h5")

      lossname = dir_name + "/nn_loss" + i_csv
      np.savetxt(lossname,train.history['loss'])


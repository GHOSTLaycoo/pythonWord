import librosa
import librosa.display
import numpy as np
import pandas as pd
import glob
import os, sys
import matplotlib.pyplot as plt
import scipy.io.wavfile
from sklearn.utils import shuffle
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Conv1D, Activation, Dropout, MaxPooling1D, Flatten, Dense
from tensorflow.python.keras.utils.np_utils import to_categorical
from sklearn.preprocessing import LabelEncoder


# python3.9.7不匹配matplotlib3.6.0换成3.4.2

def waveform():
    data, sampling_rate = librosa.load('Data/Actor_01/03-01-01-01-01-01-01.wav')

    plt.figure(figsize=(15, 5))
    librosa.display.waveshow(data, sr=sampling_rate)
    plt.show()

def spectrum():
    sr, x = scipy.io.wavfile.read('Data/Actor_01/03-01-01-01-01-01-01.wav')
    ## 参数: 10ms一步, 30ms窗长
    nstep = int(sr * 0.01)
    nwin = int(sr * 0.03)
    nfft = nwin
    window = np.hamming(nwin)
    nn = range(nwin, len(x), nstep)
    X = np.zeros((len(nn), nfft // 2))
    for i, n in enumerate(nn):
        xseg = x[n - nwin:n]
        z = np.fft.fft(window * xseg, nfft)
        X[i, :] = np.log(np.abs(z[:nfft // 2]))
    plt.imshow(X.T, interpolation='nearest',
               origin='lower',
               aspect='auto')
    plt.show()

def createlabel():
    feeling_list = []
    # 所有数据
    mylist = os.listdir('Data/audio/')

    # 遍历数据
    for item in mylist:
        if item[6:-16] == '02' and int(item[18:-4]) % 2 == 0:
            feeling_list.append('female_calm')  # 女性平静
        elif item[6:-16] == '02' and int(item[18:-4]) % 2 == 1:
            feeling_list.append('male_calm')  # 男性平静
        elif item[6:-16] == '03' and int(item[18:-4]) % 2 == 0:
            feeling_list.append('female_happy')  # 女性开心
        elif item[6:-16] == '03' and int(item[18:-4]) % 2 == 1:
            feeling_list.append('male_happy')  # 男性开心
        elif item[6:-16] == '04' and int(item[18:-4]) % 2 == 0:
            feeling_list.append('female_sad')  # 女性悲伤
        elif item[6:-16] == '04' and int(item[18:-4]) % 2 == 1:
            feeling_list.append('male_sad')  # 男性悲伤
        elif item[6:-16] == '05' and int(item[18:-4]) % 2 == 0:
            feeling_list.append('female_angry')  # 女性愤怒
        elif item[6:-16] == '05' and int(item[18:-4]) % 2 == 1:
            feeling_list.append('male_angry')  # 男性愤怒
        elif item[6:-16] == '06' and int(item[18:-4]) % 2 == 0:
            feeling_list.append('female_fearful')  # 女性恐惧
        elif item[6:-16] == '06' and int(item[18:-4]) % 2 == 1:
            feeling_list.append('male_fearful')  # 男性恐惧
        elif item[:1] == 'a':
            feeling_list.append('male_angry')  # 男性愤怒
        elif item[:1] == 'f':
            feeling_list.append('male_fearful')  # 男性恐惧
        elif item[:1] == 'h':
            feeling_list.append('male_happy')  # 男性开心
        # elif item[:1]=='n':
        # feeling_list.append('neutral')
        elif item[:2] == 'sa':
            feeling_list.append('male_sad')  # 男性悲伤

    labels = pd.DataFrame(feeling_list)
    labels[:920]

    # 构建1个包含feature特征列的Dataframe
    df = pd.DataFrame(columns=['feature'])
    bookmark = 0

    # 遍历数据
    for index, y in enumerate(mylist):
        if mylist[index][6:-16] not in ['01', '07', '08'] and mylist[index][:2] != 'su' and mylist[index][:1] not in [
            'n', 'd']:
            X, sample_rate = librosa.load('Data/audio/' + y, res_type='kaiser_fast', duration=2.5, sr=22050 * 2, offset=0.5)
            mfccs = librosa.feature.mfcc(y=X, sr=np.array(sample_rate), n_mfcc=13)
            feature = np.mean(mfccs, axis=0)
            df.loc[bookmark] = [feature]
            bookmark = bookmark + 1

    # 拼接特征与标签
    df3 = pd.DataFrame(df['feature'].values.tolist())
    newdf = pd.concat([df3, labels], axis=1)
    # 重命名标签字段
    rnewdf = newdf.rename(index=str, columns={"0": "label"})

    # 打乱样本顺序
    rnewdf = shuffle(newdf)

    # 80%的训练集，20%的测试集
    newdf1 = np.random.rand(len(rnewdf)) < 0.8
    train = rnewdf[newdf1]
    test = rnewdf[~newdf1]

    train[250:260]

    # 训练集特征与标签
    trainfeatures = train.iloc[:, :-1]
    trainlabel = train.iloc[:, -1:]
    # 测试集特征与标签
    testfeatures = test.iloc[:, :-1]
    testlabel = test.iloc[:, -1:]

    # 转为numpy array格式
    X_train = np.array(trainfeatures)
    y_train = np.array(trainlabel)
    X_test = np.array(testfeatures)
    y_test = np.array(testlabel)
    # 映射编码
    lb = LabelEncoder()
    y_train = to_categorical(lb.fit_transform(y_train))
    y_test = to_categorical(lb.fit_transform(y_test))

    # 扩充维度
    x_traincnn = np.expand_dims(X_train, axis=2)
    x_testcnn = np.expand_dims(X_test, axis=2)
    #
    # # 模型名称
    # model_name = 'Emotion_Voice_Detection_Model.h5'
    # # 路径名称
    # save_dir = os.path.join(os.getcwd(), 'saved_models')
    # model_path = os.path.join(save_dir, model_name)
    # loaded_model = keras.models.load_model(model_path)
    # # 测试集评估
    # score = loaded_model.evaluate(x_testcnn, y_test, verbose=0)
    # print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1] * 100))
    #
    # # 预估得到概率
    # preds = loaded_model.predict(x_testcnn, batch_size=32, verbose=1)
    # # 取出概率最高的类别
    # pred_labels = preds.argmax(axis=1)
    # # 映射回情绪名称
    # pred_labels = pred_labels.astype(int).flatten()
    # predictedvalues = (lb.inverse_transform((pred_labels)))
    # # 真实测试集标签
    # actual_labels = y_test.argmax(axis=1).astype(int).flatten()
    # actualvalues = (lb.inverse_transform((actual_labels)))
    # # 合并预测标签与真实标签
    # final_df = pd.DataFrame({'actualvalues': actualvalues, 'predictedvalues': predictedvalues})
    # # 输出部分结果
    # final_df[170:176]
    # 构建CNN序贯模型



    model = Sequential()
    # 卷积层+激活层
    model.add(Conv1D(256, 5, padding='same', input_shape=(216, 1)))
    model.add(Activation('relu'))
    model.add(Conv1D(128, 5, padding='same'))
    model.add(Activation('relu'))
    # Dropout防止过拟合
    model.add(Dropout(0.1))
    # 池化层降维
    model.add(MaxPooling1D(pool_size=(8)))
    # 卷积层+激活层
    model.add(Conv1D(128, 5, padding='same', ))
    model.add(Activation('relu'))
    model.add(Conv1D(128, 5, padding='same', ))
    model.add(Activation('relu'))
    # 展平+全连接层
    model.add(Flatten())
    model.add(Dense(10))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # 训练
    cnnhistory = model.fit(x_traincnn, y_train, batch_size=16, epochs=700, validation_data=(x_testcnn, y_test))

    model_name = 'Emotion_Voice_Detection_Model.h5'
    # 路径名称
    save_dir = os.path.join(os.getcwd(), 'saved_models')
    model_path = os.path.join(save_dir, model_name)
    # 模型存储
    model.save(model_path)
    print('模型存储在 %s ' % model_path)






if __name__ == "__main__":
    createlabel()
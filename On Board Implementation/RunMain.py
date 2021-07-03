'''
- Aracın otonom olarak ilerleyeceği script bu koddur.
- Kullanılan alt modüller ile;
    + Kameradan alınan veriler ön işlemlere sokulur.
    + Ön işlemlere sokulan veriler modelin input'una verilir.
    + Model görüntülere göre joystick komutu tahmin eder.
    + Tahmin edilen komutlar motor modülündeki move metoduna aktarılır
    ve araç hareket eder.
'''

# Gerekli modüllerin ve kütüphanelerin çağrılması
import cv2
import numpy as np
from tensorflow.keras.models import load_model

import WebcamModule as wM
import MotorModule as mM

# Başlangıç değişken atamaları
#######################################
steeringSen = 0.70  # Steering Sensitivity
maxThrottle = 0.22  # Forward Speed %
motor = mM.Motor(2, 3, 4, 17, 22, 27)  # Pin Numbers
model = load_model('/home/Desktop/Self_Driving_Car_CNN/On Board Implementation/model_colab.h5')
#######################################

# Kamera görüntülerinin ön işleme sokulması için metot
def preProcess(img):
    img = img[54:120, :, :]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img / 255
    return img

# Ana döngü
while True:
    # Kameradan veri alınması
    img = wM.getImg(True, size=[240, 120])
    img = np.asarray(img)
    img = preProcess(img)
    img = np.array([img])
    # Alınan verinin modele gönderilmesi ve modelden tahmin alınması
    steering = float(model.predict(img))
    print(steering * steeringSen)
    # Tahmin edilen komutun motorlara iletilmesi
    motor.move(maxThrottle, -steering * steeringSen)
    cv2.waitKey(1)

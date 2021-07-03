"""
- Bu modül elde edilen görüntü dizinlerini ve joystick verileri
bir csv dosyasına kaydeder.
- Görüntülerin kendilerini "DataCollected" adlı klasöre kaydeder.
- Veri toplamaya başlamak için ana döngüde saveData metodu çağtılır.
- Veri toplamayı bitirmek için saveLog motodu çağrılmalıdır.
- Modül ana script'ten bağımsız olarak çalıştırılırsa 10 adet
görüntü ve joystick verisi toplayaıp, birleştirecektir.
"""

# Gerekli kütüphanelerin eklenmesi
import pandas as pd
import os
import cv2
from datetime import datetime

# Değişken tanımlamaları
global imgList, steeringList
countFolder = 0
count = 0
imgList = []
steeringList = []


# Bulunulan dizinin elde edilmesi
myDirectory = os.path.join(os.getcwd(), 'DataCollected')
# print(myDirectory)

# Kod her çalıştırılıp durdurulduğunda yeni bir IMG klasörü aç
while os.path.exists(os.path.join(myDirectory,f'IMG{str(countFolder)}')):
        countFolder += 1
newPath = myDirectory +"/IMG"+str(countFolder)
os.makedirs(newPath)

# Görüntüleri ve joystick verilerini kaydet
def saveData(img,steering):
    global imgList, steeringList
    # Verilerini karışmaması sonlarına tarih, gün, saat ekle
    now = datetime.now()
    timestamp = str(datetime.timestamp(now)).replace('.', '')
    #print("timestamp =", timestamp)
    # Verileri kaydet
    fileName = os.path.join(newPath,f'Image_{timestamp}.jpg')
    cv2.imwrite(fileName, img)
    # Verileri listelere kaydet
    imgList.append(fileName)
    steeringList.append(steering)

# Veri csv dosyasını oluştur ve görüntü ve joystick değerlerini yaz
def saveLog():
    global imgList, steeringList
    rawData = {'Image': imgList,
                'Steering': steeringList}
    df = pd.DataFrame(rawData)
    df.to_csv(os.path.join(myDirectory,f'log_{str(countFolder)}.csv'), index=False, header=False)
    print('Log Saved')
    print('Total Images: ',len(imgList))

# Script tek başına çalıştırılırsa 10 adet veri kaydet
if __name__ == '__main__':
    cap = cv2.VideoCapture(1)
    for x in range(10):
        _, img = cap.read()
        saveData(img, 0.5)
        cv2.waitKey(1)
        cv2.imshow("Image", img)
    saveLog()


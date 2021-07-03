"""
- Bu Python scripti veri toplamada kullanılacak ana kod bloğudur.
- İlgili modülleri çağırır. Bu modülleri kullanarak;
    + Motorlara Gamepad üzerinden komutları gönderir.
    + Görüntü ve joystick verilerini kaydeder.
    + Bu verileri bir csv dosyasında birleşitirir.
"""

# Gerekli modüllerin koda eklenmesi
import WebcamModule as wM
import DataCollectionModule as dcM
import JoyStickModule as jsM
import MotorModule as mM
import cv2
from time import sleep

# Aracın hızının limitlenmesi
maxThrottle = 0.25

# L298N Modülünün pinlerinin tanımlanması
motor = mM.Motor(2, 3, 4, 17, 22, 27)

# Ana Döngü
record = 0
while True:
    # Gamepad'den buton ve joystick verilerinin okunması
    joyVal = jsM.getJS()
    # print(joyVal)

    # İlgili buton ve joystick verilerinin kullanılmak üzere verilere atanması
    steering = joyVal['axis1']
    throttle = joyVal['o'] * maxThrottle

    # Eğer Joystick'te "Play" butanona basılır ise;
    if joyVal['share'] == 1:
        # Kayıtı başlatmada kullanılacak olan "record" değişkenini "1" yap
        if record == 0: print('Recording Started ...')
        record += 1
        sleep(0.300)
    # Veri toplamaya başla
    if record == 1:
        # getImg metotdu ile görüntüleri kaydet
        img = wM.getImg(True, size=[240, 120])
        # saveData metotu ile görüntü ve joystick verilerini eşleştir ve kaydet
        dcM.saveData(img, steering)
    # "Play" tuşuna bir kez daha basılırsa kayıtı durdur
    elif record == 2:
        # Verileri bir csv dosyasına aktar
        dcM.saveLog()
        record = 0

    # Motora Gamepad komutlarını gönder
    motor.move(throttle, -steering)
    cv2.waitKey(1)

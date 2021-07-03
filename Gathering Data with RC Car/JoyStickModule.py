"""
- Bu modülün görevi Gamepad'den buton ve joytick değerlerinin okumaktır.
- Butonlar ve joystick verileri pygame kütüphanesindeki event'ler yolu ile okunmaktadır.
- Script tek başına çalıştırılırsa tüm buton ve joystick değerlerini okur ve yazdırır.
"""

# Gerekli kütüphanelerin çağrılması
import pygame
from time import sleep

# Pygame'i hazırla
pygame.init()
# Gamepad'i tanımla ve hazırla
controller = pygame.joystick.Joystick(0)
controller.init()
# Buton ve joystick tanımlamaları
buttons = {'x': 0, 'o': 0, 't': 0, 's': 0,
           'L1': 0, 'R1': 0, 'L2': 0, 'R2': 0,
           'share': 0, 'options': 0,
           'axis1': 0., 'axis2': 0., 'axis3': 0., 'axis4': 0.}
axiss = [0., 0., 0., 0., 0., 0.]


# Buton ve joystick  değerlerini oku
def getJS(name=''):
    global buttons
    # Herhangi bir buton veya jostick verisi gelir ise kaydet
    for event in pygame.event.get():  # Joystick değerleri
        if event.type == pygame.JOYAXISMOTION:
            axiss[event.axis] = round(event.value, 2)
        elif event.type == pygame.JOYBUTTONDOWN:  # Buton basıldığında
            # print(event.dict, event.joy, event.button, 'PRESSED')
            for x, (key, val) in enumerate(buttons.items()):
                if x < 10:
                    if controller.get_button(x): buttons[key] = 1
        elif event.type == pygame.JOYBUTTONUP:  # Butondan el çekilince
            # print(event.dict, event.joy, event.button, 'released')
            for x, (key, val) in enumerate(buttons.items()):
                if x < 10:
                    if event.button == x: buttons[key] = 0

    # Kullanımayacak olan ['axis2'] verisini çıkar
    buttons['axis1'], buttons['axis2'], buttons['axis3'], buttons['axis4'] = [axiss[0], axiss[1], axiss[3], axiss[4]]
    if name == '':
        return buttons
    else:
        return buttons[name]


def main():
    print(getJS())  # Tüm komutları almak için
    # sleep(0.05)
    # print(getJS('share'))  # Tekli buton değerleri için
    sleep(0.05)


# Kod tek başına çalıştırılırsa main kodunu çağır ve gamepad komutlarını yazdır
if __name__ == '__main__':
    while True:
        main()

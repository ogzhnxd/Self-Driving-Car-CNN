"""
- Bu modül kameradan görüntü almak için kullanılır.
- Alınan görüntüyü gösterebilir veya göstermeyebilir.
- Görüntüler tekrar boyutlandırılabilir.
"""

import cv2

# Jetson Nano için gstreamer pipeline'ının oluşturulması
def gstreamer_pipeline(
        capture_width=1280,
        capture_height=720,
        display_width=1280,
        display_height=720,
        framerate=60,
        flip_method=0,
):
    return (
            "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                capture_width,
                capture_height,
                framerate,
                flip_method,
                display_width,
                display_height,
            )
    )

# Kameranın tanımlanması
cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0))

# Görüntü almak için metot
def getImg(display=False, size=[480, 240]):
    _, img = cap.read()
    img = cv2.resize(img, (size[0], size[1]))
    # display değişkeni 1 ise görüntüleri göster
    if display:
        cv2.imshow('IMG', img)
    return img

# Kod yalnız çalıştırılırsa görüntü al
if __name__ == '__main__':
    while True:
        img = getImg(True)

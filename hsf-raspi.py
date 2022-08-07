# -*- coding: utf-8 -*-
import picamera #カメラモジュール用
import serial
import time

QR_num = 3
vision_num = QR_num

cap = picamera.PiCamera() #インスタンス生成
cap.resolution = (600, 600) #画像サイズの指定

while True:

    #写真撮影
    ser = serial.Serial('/dev/ttyUSB0', 115200)
    schoomy_data = 0

    
    #schoomyのpress sensor ループ
    for i in range(QR_num):
        #schoomyのLEDを点灯させる信号
        ser.write(b'1')
        print("撮影待機")
        while True:
            schoomy_data = ser.readline()
            print("圧力感知しました。撮影します。")
            time.sleep(4)
            path_jpg = '/home/pi/ai101/vision/'+ str(i+1) +'.jpg'
            cap.capture(path_jpg) #撮影
            if schoomy_data != 0:
                break

    print("すべて撮影完了しました。")
    break

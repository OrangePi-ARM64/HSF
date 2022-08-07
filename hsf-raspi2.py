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
            cap.start_preview()
            time.sleep(4)
            path_jpg = '/home/pi/ai101/vision/'+ str(i+1) +'.jpg'
            cam = cap.capture(path_jpg) #撮影
            attached_image = cam
            attached_image
            cap.stop_preview()
            if schoomy_data != 0:
                break

    print("すべて撮影完了しました。")
    cap.close()
    break

    # 検出数が1以上のときLINE通知
    if target_object_count >= 1:

        # 最小通知間隔を超えていた時だけ通知
        if time.time() - last_send_time > MINIMUM_LINE_INTERVAL:

            # 今の時刻をLINE通知時刻として保存
            last_send_time = time.time()

            # SchooMyから取得したシリアルデータをメッセージとする
            line_message = str(schoomy_data)

            # 検出物体の種別をメッセージに追加
            line_message += ' ' + CLASS_LABELS[target_class_id]

            # 検出物体の数をメッセージに追加
            # subjectは「通知テスト person:1」のようになる
            line_message += ':' + str(target_object_count)

            # HTTPのヘッダ部分にLINE APIトークンをセット
            headers = {"Authorization": "Bearer " + line_notify_token}

            # HTTPボディに通知メッセージをセット
            body = {"message": line_message}

            binary = frame

            # カメラから取り込んだフレームをJPEG形式に変換し attached_image へセット
            # attached_imageにJPEG形式の画像データが入る

            # POSTリクエストに使う, 画像のファイル名を日時から生成し file_name へセット
            # file_nameは「person20200110-111213.jpg」のようになる
            file_name = CLASS_LABELS[target_class_id]
            file_name += time.strftime("%Y%m%d-%H%M%S")
            file_name += '.jpg'

            image_file = file_name

            # imageFileパラメタに, 画像をファイル名や種別情報とともにセット
            files = {"imageFile": (file_name, attached_image, 'image/jpeg')}

            # ヘッダとデータ（ボディ）を指定してLINE通知APIサーバにPOSTリクエストを送信
            res = requests.post(LINE_NOTIFY_API, headers=headers, data=body, files=files)

            # サーバからの応答をターミナル画面に表示させる
            print('通知:{}'.format(line_message))
            print(res.text)
            # ソケットクライアント作成
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                # 送信先サーバーに接続
                s.connect((host, port))

                # サーバーにattached_imageデータを送る
                print(image_file + 'をサーバーに送信')
                s.sendall(attached_image)
                # データ送信完了後、送信路を閉じる
                s.shutdown(1)

                # サーバーからの応答を取得。バッファサイズ1024バイト
                #resp = s.recv(1024)
                # サーバー応答を表示
                #print('認識結果： ' + resp)

            except Exception as e:
                # 例外が発生した場合、内容を表示
                print(e)

    time.sleep(args['interval'])

# 終了処理
# ソケットを閉じて終了
s.close()
print('終了処理...')
time.sleep(3)

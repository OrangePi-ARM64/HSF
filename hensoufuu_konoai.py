#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential, Model,load_model
from PIL import Image
import numpy as np
import socket
import os, sys
import psycopg2
import webbrowser

constr = "host='localhost' port=5432 dbname=shop user=postgres password='a'"

# パラメーターの初期化
classes = [
"caesar_salad",
"cheesecake",
"chicken_wings",
"donuts",
"edamame",
"french_fries",
"fried_rice",
"grilled_salmon",
"gyoza",
"hamburger",
"miso_soup",
"omelette",
"pizza",
"ramen",
"sashimi",
"sushi",
"takoyaki"
]

shoku_id = ["0001","0002","0003","0004","0005","0006","0007","0008","0009","0010","0011","0012","0013","0014","0015","0016","0017"]

num_classes = len(classes)
image_size = 224

# サーバーIPアドレス定義
host = "192.168.100.27"
# サーバーの待ち受けポート番号定義
port = 50001

# 受信画像保存ディレクトリ
sc_dir = 'dataset\sc'
# 受信画像ファイル名
sc_file = 'sc_file.jpg'

def main():

    # 環境設定(ディスプレイの出力先をlocalhostにする)
    os.environ['DISPLAY'] = ':0'

    # モデルのロード
    model = load_model('./vgg16_transfer.h5')


    # ソケット定義(IPv4,TCPによるソケット)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 次の実行に備え、ソケットをTIME-WAIT切れを待つことなく、再利用できるようにしておく
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # IPとPORTを指定してバインド（ソケットに紐づけ）
        s.bind((host,port))
        # ソケット接続待受（キューの最大数を指定）
        s.listen(10)

        while True:
            # ソケット接続受信待ち
            try:
                print('クライアントからの接続待ち...')
                # 接続が来たら対応する新しいソケットオブジェクト作成、接続先アドレスを格納
                clientsock, client_address = s.accept()

            # 接続待ちの間に強制終了が入った時の例外処理
            except KeyboardInterrupt:
                print(' Ctrl + C により強制終了')
                break

            # 接続待ちの間に強制終了なく、クライアントからの接続が来た場合
            else:
                # 受信処理を行い、画像認識結果を返す
                recv_client_data(clientsock, model, classes)

    except Exception as e:
        print(e)

    finally:
        # ソケットを閉じる
        s.close()


def recv_client_data(clientsock, model, classes):
    # 受信データ保存用変数の初期化
    all_data = b''

    try:
        # ソケット接続開始後の処理
        while True:
            # データ受信。受信バッファサイズ1024バイト
            data = clientsock.recv(1024)
            # 全データ受信完了（受信路切断）時に、ループ離脱
            if not data:
                break
            # 受信データを追加し繋げていく
            all_data += data

        # 受信画像ファイル保存
        with open(sc_dir + '/' + sc_file, 'wb') as f:
            # ファイルにデータ書込
            f.write(all_data)

        # 受信画像ファイルに対しAIで画像認識を実行
        res = vgg_recognition(model, classes)
        # 認識結果をクライアントに送信
        #clientsock.sendall('Result: Inference completed.')

    except Exception as e:
        print('受信処理エラー発生')
        print(e)

    finally:
        # コネクション切断
        clientsock.close()


def vgg_recognition(model, classes):
    # 画像ファイル取得
    filename = os.path.join(sc_dir, sc_file)
    image = Image.open(filename)
    image = image.convert("RGB")
    image = image.resize((image_size,image_size))
    data = np.asarray(image) / 255.0
    X = []
    X.append(data)
    X = np.array(X)

    result = model.predict([X])[0]
    predicted = result.argmax()
    percentage = int(result[predicted] * 100)

    print('受信ファイル認識結果：')
    print(classes[predicted], percentage)
    print('=======================================')
    shoku_num = shoku_id[predicted]
    shoku_sql = 'SELECT shoku_id, hin_mei, syoku_zai, syu3_hin, sei_url FROM shokuhin WHERE shoku_id = ' + "'" + shoku_num + "'"
    #print(shoku_sql)
    conn = psycopg2.connect(constr)
    cur = conn.cursor()
    cur.execute(shoku_sql)
    #res = cur.fetchall()
    res = cur.fetchone()
    print(res)
    res1 = res[4]
    cur.close()
    conn.close()
    webbrowser.open(res1)

if __name__ == '__main__':
    main()


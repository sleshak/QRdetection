import cv2 
from qreader import QReader
import numpy as np 
 
def process_video(video_path): 
    cap = cv2.VideoCapture(video_path) 
    if not cap.isOpened(): 
        print(f"Не удалось открыть видео: {video_path}") 
        return 
 
    qreader = QReader()
    #qr_reader = qreader.QR()  # Инициализируем qreader 
    last_positions = {} # Словарь для хранения последних позиций 
 
    while True: 
        ret, frame = cap.read() 
        if not ret: 
            break 
         
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        decoded_data = qreader.detect_and_decode(gray_frame, return_detections = True) # Декодируем кадр 
 
        for qr_code in decoded_data: 
          data = qr_code.data 
          if data is not None: 
             x, y, w, h = qr_code.rect # Получаем координаты и размеры прямоугольника 
             # Отрисовываем прямоугольник вокруг QR-кода 
             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  
             print(f"QR code data: {data}") 
              
             # Запоминаем последнюю позицию 
             last_positions[data] = (x, y, w, h) 
 
        for data, (x, y, w, h) in last_positions.items(): 
           cv2.putText(frame, f"Last seen: {x}, {y}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2) 
 
        cv2.imshow('QR Detection', frame) 
 
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break 
 
    # Выводим последнее местоположение для каждого QR кода 
    print("\nПоследние местоположения:") 
    for data, (x, y, w, h) in last_positions.items(): 
        print(f"QR code: {data}, Pos: {x}, {y}") 
 
    cap.release() 
    cv2.destroyAllWindows() 
 
if __name__ == "__main__": 
    video_path = "assets\образец №1.mp4"  # Замените на путь к вашему видеофайлу 
    process_video(video_path)
import cv2
from qreader import QReader

qreader = QReader()
cap = cv2.VideoCapture('assets/образец №2.mp4')

# Получаем параметры видео
fps = cap.get(cv2.CAP_PROP_FPS)  # Частота кадров
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # Ширина
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Высота

# Задаем новый размер (например, 640x480)
new_width = 640
new_height = 480



while cap.isOpened():
    ret, frame = cap.read()

    resized_frame = cv2.resize(frame, (new_width, new_height))
    
    if not ret:
        break

    qr_code_data = qreader.detect_and_decode(resized_frame, return_detections = True)
    

    if qr_code_data:
        print(qr_code_data)
        #x, y, w, h = qr_code_data.rect
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #cv2.putText(frame, qr_code_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow('QR Detection', resized_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

import cv2
import os
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture('assets\образец №2.mp4')
output_video_path = 'output_video.mp4'
#====================обработка

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 


fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height), isColor=False)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred_frame = cv2.GaussianBlur(gray_frame, (7, 7), 0)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_frame = clahe.apply(gray_frame)
    thresholded_frame = cv2.adaptiveThreshold(enhanced_frame, 255, 
                                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                               cv2.THRESH_BINARY, 11, 2)
    
    resized_frame = cv2.resize(thresholded_frame, (width, height))

    out.write(resized_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

#========================================вывод

video_cap = cv2.VideoCapture('output_video.mp4')

while video_cap.isOpened():
    ret, frame = video_cap.read()
    
    if not ret:
        break
    
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    barcodes = decode(gray_frame)
    
    for barcode in barcodes:
        qr_code_data = barcode.data.decode('utf-8')
        
        x, y, w, h = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        cv2.putText(frame, qr_code_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    cv2.imshow('QR Detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_cap.release()
cv2.destroyAllWindows()

if os.path.exists(output_video_path):
    os.remove(output_video_path)
    print(f"Файл {output_video_path} был удален.")
else:
    print(f"Файл {output_video_path} не найден.")

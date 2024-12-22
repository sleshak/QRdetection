from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QLabel, 
                             QSizePolicy, QSpacerItem) 
from PyQt6.QtGui import QPixmap, QColor, QPalette, QBrush 
from PyQt6.QtCore import Qt, QRect 
import sys 
import tkinter as tk
from tkinter import filedialog
import os 
import cv2
from pyzbar.pyzbar import decode
 
class MainWindow(QWidget): 
    def __init__(self): 
        super().__init__() 
 
        self.setWindowTitle("АйтиКошечки") 

        screen_geometry = QApplication.screens()[0].availableGeometry() 
        x = (screen_geometry.width() - 800) // 2 
        y = (screen_geometry.height() - 500) // 2 
        self.setGeometry(x, y, 800, 500) 
 
        self.background_label = QLabel(self) 
        self.background_label.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        self.background_label.setSizePolicy( 
           QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding 
        ) 
        self.background_label.setScaledContents(True) 
  
        self.background_label.setGeometry(0, 0, 800, 500) 
 
        self.button1 = QPushButton("Добавить QR", self) 
        self.button2 = QPushButton("Загрузить видеофайл", self) 
        self.button3 = QPushButton("Подтвердить", self) 

        self.button1.clicked.connect(self.on_button1_clicked)
        self.button2.clicked.connect(self.on_button2_clicked)
        self.button3.clicked.connect(self.on_button3_clicked)
 
        self.button1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed) 
        self.button2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed) 
        self.button3.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed) 
        self.button1.setFixedHeight(50) 
        self.button2.setFixedHeight(50)
        self.button3.setFixedHeight(50) 
        self.button1.setMinimumWidth(200) 
        self.button2.setMinimumWidth(200) 
        self.button3.setMinimumWidth(200) 
 
        self.file_label = QLabel(self)
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.additional_label = QLabel(self)
        self.additional_label.setAlignment(Qt.AlignmentFlag.AlignCenter)


        button_layout = QHBoxLayout() 
        button_layout.addWidget(self.button1) 
        button_layout.addWidget(self.button2) 


        spacer = QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed) 

        all_buttons_layout = QVBoxLayout() 
        all_buttons_layout.addItem(spacer) 
        all_buttons_layout.addLayout(button_layout) 
        all_buttons_layout.addWidget(self.additional_label)
        all_buttons_layout.addWidget(self.button3) 
        all_buttons_layout.addWidget(self.file_label)
        all_buttons_layout.setContentsMargins(0, 20, 0, 0)
  
        main_layout = QVBoxLayout(self) 
        main_layout.addStretch() 
        main_layout.addLayout(all_buttons_layout)
        main_layout.addWidget(self.file_label) 
 
        self.setLayout(main_layout) 
        self.load_background() 
        self.setup_buttons()

    def on_button2_clicked(self):
        input_video_path = self.select_video_file()
        if input_video_path:
            self.file_label.setText(f"Выбрано видео: {input_video_path}")
            self.input_video_path = input_video_path
    
    def on_button1_clicked(self):
        qr_path = self.select_qr()
        if qr_path:
            self.file_label.setText(f"Выбран файл: {qr_path}")
            self.qr_path = qr_path 

    def on_button3_clicked(self):
        if hasattr(self, 'qr_path') and hasattr(self, 'input_video_path'):
            self.file_label.setText(f"QR и видео выбраны. Ожидайте...")
            self.process_video_and_detect_qr()
        else:
            self.file_label.setText("Пожалуйста, выберите файлы с кнопок 1 и 2.")

    def process_video_and_detect_qr(self):
        comp_code_data = decode(cv2.imread(self.qr_path))

        output_video_path = 'output_video.mp4'

        cap = cv2.VideoCapture(self.input_video_path)

        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height), isColor=False)

        last_qr_position = None

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (width, height))

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

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

        video_cap = cv2.VideoCapture(output_video_path)

        while video_cap.isOpened():
            ret, frame = video_cap.read()
            
            if not ret:
                break
            
            frame = cv2.resize(frame, (width, height))

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            barcodes = decode(gray_frame)
            
            found_correct_qr = False

            for barcode in barcodes:
                qr_code_data = barcode.data.decode('utf-8')
                if qr_code_data == comp_code_data[0].data.decode('utf-8'):
                    found_correct_qr = True
                    last_qr_position = barcode.rect
                    print(f"Координаты правильного QR: {last_qr_position}")
                    x, y, w, h = last_qr_position
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, 'CORRECT QR', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                else:
                    x, y, w, h = barcode.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(frame, qr_code_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            if not found_correct_qr and last_qr_position:
                x, y, w, h = last_qr_position
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, 'LAST CORRECT QR', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            cv2.imshow('QR Detection', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_cap.release()
        cv2.destroyAllWindows()

        if os.path.exists(output_video_path):
            os.remove(output_video_path)
        
        self.file_label.setText("Выберите QR и видео")


    def select_qr(self):
        root = tk.Tk()
        root.withdraw()
        qr_path = filedialog.askopenfilename(title="Выберите файл", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        return qr_path 

    def select_video_file(self):
        root = tk.Tk()
        root.withdraw() 
        video_path = filedialog.askopenfilename(title="Выберите видеофайл", filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv")])
        return video_path
    
    def load_background(self): 
        image_path = 'kotiks.jpg' 
        if os.path.exists(image_path): 
            pixmap = QPixmap(image_path) 
            self.background_label.setPixmap(pixmap) 
            self.background_label.setStyleSheet("background-color: rgba(255, 255, 255, 0.6); border: none;")  # 0.6 для полупрозрачности 
        else: 
            self.background_label.clear() 
            self.setAutoFillBackground(True) 
            palette = self.palette() 
            palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240)) # Светло-серый цвет 
            self.setPalette(palette) 
            self.background_label.setStyleSheet("background-color: rgba(240, 240, 240, 0.6); border: 1px solid #ddd;") # 0.6 для полупрозрачности 
    def setup_buttons(self): 
        button_style = """ 
            QPushButton { 
                background-color: rgba(200, 200, 200, 0.7); 
                border: 2px solid
                #8f8f91; 
                border-radius: 15px; 
                padding: 10px; 
            } 
            QPushButton:hover { 
              background-color: rgba(180, 180, 180, 0.8); 
            } 
            QPushButton:pressed { 
              background-color: rgba(160, 160, 160, 0.9); 
            } 
        """ 
 
        self.button1.setStyleSheet(button_style) 
        self.button2.setStyleSheet(button_style) 
        self.button3.setStyleSheet(button_style) 
 
 
    def resizeEvent(self, event): 
         self.background_label.setGeometry(self.rect()) 
         super().resizeEvent(event) 
 
 
if __name__ == '__main__': 
    app = QApplication(sys.argv) 
    window = MainWindow() 
    window.show() 
    app.exec()
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QLabel, 
                             QSizePolicy, QSpacerItem) 
from PyQt6.QtGui import QPixmap, QColor, QPalette, QBrush 
from PyQt6.QtCore import Qt, QRect 
import sys 
import tkinter as tk
from tkinter import filedialog
import os 
 
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
    
    def on_button1_clicked(self):
        qr_path = self.select_qr()
        if qr_path:
            self.file_label.setText(f"Выбран файл: {qr_path}")

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
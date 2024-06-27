import sys
import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QMessageBox, QVBoxLayout, QWidget, QPushButton, QFrame, QListWidget, QListView, QListWidgetItem, QSlider, QScrollArea
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random
import imports

class Page3(QWidget):
    def __init__(self):
        super().__init__()

        self.scrollArea = QScrollArea(self)  # Tworzymy obszar przewijania
        self.scrollWidget = QWidget()  # Widget, który będzie przewijany
        self.scrollLayout = QVBoxLayout(self.scrollWidget)  # Układ dla przewijanego widgetu

        self.frame = QFrame(self.scrollWidget)
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setLineWidth(2)

        self.scrollLayout.addWidget(self.frame)
        self.scrollWidget.setLayout(self.scrollLayout)

        self.scrollArea.setWidgetResizable(True)  # Umożliwia zmianę rozmiaru widgetu wewnątrz obszaru przewijania
        self.scrollArea.setWidget(self.scrollWidget)  # Ustawia widget do przewijania

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.scrollArea)
        self.setLayout(self.main_layout)

        self.statistics_loaded = False  # Flaga informująca, czy statystyki zostały już załadowane

    def load_statistics(self):
        if self.statistics_loaded:
            return  # Jeśli statystyki zostały już załadowane, nie rób nic

        self.user_id = self.get_user_id()
        statistics = imports.get_statistics(self.user_id)

        labels = list(statistics.keys())
        sizes = list(statistics.values())

        # Generowanie losowych kolorów dla wykresu kołowego
        def random_color():
            return "#{:06x}".format(random.randint(0, 0xFFFFFF))

        pie_colors = [random_color() for _ in range(len(statistics))]

        # Wykres słupkowy
        fig_bar = Figure(figsize=(5, 4), dpi=100)
        plot_bar = fig_bar.add_subplot(111)
        plot_bar.bar(labels, sizes, color='blue')  # Ustawienie stałego koloru dla wykresu słupkowego
        self.add_figure(fig_bar)

        # Wykres kołowy
        fig_pie = Figure(figsize=(7, 6), dpi=100)  # Zwiększono rozmiar wykresu kołowego
        plot_pie = fig_pie.add_subplot(111)
        wedges, texts, autotexts = plot_pie.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=pie_colors)
        
        for autotext in autotexts:
            autotext.set_color('white')  # Ustawienie koloru tekstu na biały
            autotext.set_fontsize(10)  # Ustawienie rozmiaru czcionki

        plot_pie.axis('equal')  # Równy aspekt ratio zapewnia, że wykres kołowy będzie kołem.
        self.add_figure(fig_pie)

        self.statistics_loaded = True  # Ustawienie flagi na True po załadowaniu statystyk

    def add_figure(self, fig):
        canvas = FigureCanvas(fig)
        self.scrollLayout.addWidget(canvas)  # Dodajemy canvas do scrollLayout zamiast do frame

    def get_user_id(self):
        isUserLogged = imports.authService.isUserLogged()
        if isUserLogged:
            logged_user_info = imports.authService.getLoggedUserInfo()
            return logged_user_info['id']
        else:
            return None

    def showEvent(self, event):
        if not self.statistics_loaded:  # Ładuj statystyki tylko raz
            self.load_statistics()
        super().showEvent(event)
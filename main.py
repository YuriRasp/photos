from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel,
    QHBoxLayout, QVBoxLayout, QListWidget,QPushButton,
    QFileDialog,QFileDialog,
                            )
import os
from PIL import (Image, ImageFilter)
from PyQt5.QtGui import QPixmap



app = QApplication([])
win = QWidget()

workdir=QFileDialog.getExistingDirectory

lw_files = QListWidget()
lb_image = QLabel("Картинка")

btn_dir=QPushButton('Папка')
btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_mirr = QPushButton('Зеркало')
btn_shrp = QPushButton('Резкоть')
btn_BW = QPushButton('Ч/Б')
btn_save = QPushButton('Сохранить')
btn_reset = QPushButton('Сбросить')

row = QHBoxLayout()

col1 = QVBoxLayout()
col2 = QVBoxLayout()

row_tools = QHBoxLayout()

col1.addWidget(btn_dir)
col1.addWidget(lw_files)

col2.addWidget(lb_image)

row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_mirr)
row_tools.addWidget(btn_shrp)
row_tools.addWidget(btn_BW)
row_tools.addWidget(btn_reset)
col2.addLayout(row_tools)

row.addLayout(col1, 20)
row.addLayout(col2, 80)

def filter(files,extensions):
    result=[]
    for file in files:
        for extension in extensions:
            if file.endswith(extension):
                result.append(file)
    return result

def chooseWorkdir():
    global workdir
    workdir=QFileDialog.getExistingDirectory()

def showFilenameList():
    extensions=['.png','.jpg','jpeg','.bmp','.gif']
    chooseWorkdir()
    filenames=filter(os.listdir(workdir),extensions)

    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)

class imageProcessor():
    def __init__(self):
        self.image=None
        self.dir=None
        self.filename=None
        self.saveDir='Modified/'
        self.original_image=None
    def loadImage(self,filename):
        self.filename=filename
        image_path=os.path.join(workdir,filename)
        self.image=Image.open(image_path)
        self.original_image=self.image.copy()
    def showImage(self,path):
        pixmapimage=QPixmap(path)
        label_width, label_height = lb_image.width(),lb_image.height()
        scaled_pixmap=pixmapimage.scaled(label_width,label_height,Qt.KeepAspectRatio)
        lb_image.setPixmap(scaled_pixmap)
        lb_image.setVisible(True)
    def do_bw(self):
        self.image=self.image.convert('L')
        self.saveImage()
        image_path=os.path.join(workdir,self.saveDir,self.filename)
        self.showImage(image_path)
    def saveImage(self):
        path=os.path.join(workdir,self.saveDir)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path=os.path.join(path,self.filename)
        self.image.save(image_path)
    def do_flip(self):
        self.image=self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path=os.path.join(workdir,self.saveDir,self.filename)
        self.showImage(image_path)
    def do_sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path=os.path.join(workdir,self.saveDir,self.filename)
        self.showImage(image_path)
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path=os.path.join(workdir,self.saveDir,self.filename)
        self.showImage(image_path)
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path=os.path.join(workdir,self.saveDir,self.filename)
        self.showImage(image_path)
    def do_reset(self):
        self.image=self.original_image.copy()
        self.showImage(os.path.join(workdir,self.filename))


def showChoosenImage():
    if lw_files.currentRow()>=0:
        filename=lw_files.currentItem().text()
        workimage.loadImage(filename)
        image_path=os.path.join(workdir,workimage.filename)
        workimage.showImage(image_path)


lw_files.currentRowChanged.connect(showChoosenImage)

workimage = imageProcessor()
'''Привязка кнопок'''
btn_dir.clicked.connect(showFilenameList)
btn_BW.clicked.connect(workimage.do_bw)
btn_mirr.clicked.connect(workimage.do_flip)
btn_shrp.clicked.connect(workimage.do_sharpen)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_reset.clicked.connect(workimage.do_reset)


win.resize(800,400)
win.setLayout(row)
win.show()

app.exec_()


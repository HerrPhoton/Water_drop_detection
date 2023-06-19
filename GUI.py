import os
import cv2
import sys
import TestNetwork_
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap, QPixmapCache, QImage
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow, QFileDialog, QAction

def detect_image(filepath, output):
    TestNetwork_.work(filepath, output,".jpg", mode = "picture")

def detect_folder(filepath, output):
    TestNetwork_.work(filepath, output,".jpg")

class WelcomeScreen(QMainWindow):
    def __init__(self, widget):
        super(WelcomeScreen,self).__init__()
        loadUi("ui/page1.ui",self)
        self.widget = widget
        pixmap = QPixmap('logo/logobig.png')
        self.label.setPixmap(pixmap)
        self.label_2.setPixmap(QPixmap('logo/wallpaper1.jpg'))
        self.start_btn.clicked.connect(lambda: self.start_click())
           
    def start_click(self):
        select_file = SelectScreen(self.widget) 
        self.widget.addWidget(select_file)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)

class SelectScreen(QMainWindow):
    def __init__(self, widget):
        super(SelectScreen,self).__init__()
        loadUi("ui/page2.ui",self)
        self.widget = widget
        self.setAcceptDrops(True)
        self.label_2.setPixmap(QPixmap('logo/wallpaper1.jpg'))
        self.pushFolderButton.clicked.connect(lambda: self.open_folder())
        self.pushImageButton.clicked.connect(lambda: self.open_image())
    
    def open_folder(self):
        file = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        if os.path.exists(file):
            select_file = FolderPretrainScreen(file, self.widget) 
            self.widget.addWidget(select_file)
            self.widget.setCurrentIndex(self.widget.currentIndex()+1)
        
    def open_image(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Select Image", None, "Image (*.png *.jpg)")[0]
        if "jpg" in file or "png" in file:
            select_file = ImagePretrainScreen(file, self.widget) 
            self.widget.addWidget(select_file)
            self.widget.setCurrentIndex(self.widget.currentIndex()+1)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            self.file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image(self.file_path)
            event.accept()
        else:
            event.ignore()

    def set_image(self, file):
        if "jpg" in file or "png" in file:
            select_file = ImagePretrainScreen(file, self.widget) 
            self.widget.addWidget(select_file)
            self.widget.setCurrentIndex(self.widget.currentIndex()+1)
        else:
            select_file = FolderPretrainScreen(file, self.widget) 
            self.widget.addWidget(select_file)
            self.widget.setCurrentIndex(self.widget.currentIndex()+1)

class ImagePretrainScreen(QMainWindow):
    def __init__(self, file, widget):
        super(ImagePretrainScreen,self).__init__()
        loadUi("ui/page3_image.ui",self)
        self.pixmap = QPixmap(file)
        self.widget = widget
        self.file = file
        self.label_2.setPixmap(QPixmap('logo/wallpaper1.jpg'))
        super().layout().activate()
        self.label.setPixmap(self.pixmap.scaled(1700,717, QtCore.Qt.KeepAspectRatio))
        self.toNeuralButton.clicked.connect(lambda: self.findDrops(file))
        self.ImageProcessingButton.clicked.connect(lambda: self.ImageProcessing(file))
        self.BackButton.clicked.connect(lambda: self.Back())

    def findDrops(self, file):
        select_file = FolderResultScreen(file,0,self.widget) 
        self.widget.addWidget(select_file)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)
        
    def ImageProcessing(self, file):
        select_file = EditScreen(file, self.widget)
        self.widget.addWidget(select_file)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)
        
    def Back(self):
        select_file = SelectScreen(self.widget)
        self.widget.addWidget(select_file)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)

class FolderPretrainScreen(QMainWindow):
    def __init__(self, file, widget):
        super(FolderPretrainScreen,self).__init__()
        loadUi("ui/page3_folder.ui",self)
        self.widget = widget
        self.label.setText("Your choice: \n" + file)
        self.label_3.setPixmap(QPixmap('logo/wallpaper1.jpg'))
        print(file)
        
        self.toNeuralButton.clicked.connect(lambda: self.findDrops(file))
        self.BackButton.clicked.connect(lambda: self.Back())
    
    def findDrops(self, file):
        select_file = FolderResultScreen(file, self.widget) 
        self.widget.addWidget(select_file)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)
        
    def Back(self):
        select_file = SelectScreen(self.widget) 
        self.widget.addWidget(select_file)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)

class EditScreen(QMainWindow):
    def __init__(self, file, widget):
        super(EditScreen,self).__init__()
        loadUi("ui/page4_image.ui",self)
        self.widget = widget
        self.photos = [QPixmap(file)]
        self.rotation = 0
        self.pixmap = QPixmap(file)
        self.edit_pixmap = QPixmap(file)
        self.label_2.setPixmap(QPixmap('logo/wallpaper1.jpg'))
        self.label.setPixmap(QPixmap(file).scaled(1700,717, QtCore.Qt.KeepAspectRatio))
        
        self.okButton.clicked.connect(lambda: self.ok(file))
        self.backButton.clicked.connect(lambda: self.Back())
        self.rotateButton.clicked.connect(lambda: self.rotate())
 
    def ok(self, file):
        self.photos[-1].save('pixmap.png')
        select_file = FolderResultScreen(file, 0, self.widget) 
        self.widget.addWidget(select_file)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)
        
    def Back(self):
        if(len(self.photos)>1):
            self.photos.pop()
            self.label.setPixmap(self.photos[-1].scaled(1700,717, QtCore.Qt.KeepAspectRatio))
    
    def rotate(self):
        pixmap = self.edit_pixmap.copy()
        self.rotation += 90
        transform = QtGui.QTransform().rotate(90)
        pixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)
        self.label.setPixmap(pixmap.scaled(1700,717, QtCore.Qt.KeepAspectRatio))
        self.edit_pixmap = pixmap
        self.photos.append(pixmap)
        pixmap.save('pixmap.png')
        
    def mousePressEvent (self, eventQMouseEvent):
        offset = self.label.pos()
        self.label.originQPoint = eventQMouseEvent.pos()-offset
        self.label.currentQRubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self.label)
        self.label.currentQRubberBand.setGeometry(QtCore.QRect(self.label.originQPoint, QtCore.QSize()))
        self.label.currentQRubberBand.show()

    def mouseMoveEvent (self, eventQMouseEvent):
        offset = self.label.pos()
        self.label.currentQRubberBand.setGeometry(QtCore.QRect(self.label.originQPoint, eventQMouseEvent.pos()-offset).normalized())

    def mouseReleaseEvent (self, eventQMouseEvent):
        self.label.currentQRubberBand.hide()
        currentQRect = self.label.currentQRubberBand.geometry()
        self.label.currentQRubberBand.deleteLater()
        self.edit_pixmap = self.label.grab(currentQRect)
        self.photos.append(self.edit_pixmap)
        self.label.setPixmap(self.edit_pixmap.scaled(self.label.size(), QtCore.Qt.KeepAspectRatio))
        self.edit_pixmap.save('pixmap.png')


class FolderResultScreen(QMainWindow):
    def __init__(self, input_folder, flag, widget):
        super(FolderResultScreen,self).__init__()
        loadUi("ui/page5_folder.ui",self)
        self.widget = widget
        self.label_4.setPixmap(QPixmap('logo/wallpaper1.jpg'))
        if not flag:
            self.output_folder = input_folder[:len(input_folder) - 1 - input_folder[::-1].index('/')+1]+"detected_"+input_folder[len(input_folder) - 1 - input_folder[::-1].index('/')+1:input_folder.find(".")]
            if os.path.exists("pixmap.png"):
                detect_image("pixmap.png", self.output_folder)
                os.remove("pixmap.png")
            else:
                detect_image(input_folder, self.output_folder)
        else:
            self.output_folder = input_folder+'/detected'
            detect_folder(input_folder, self.output_folder)
        self.img_with_frame = []
        self.index = 0
        self.mode = 0

        self.img_no_frame = []
        dirr = sorted(os.listdir(self.output_folder))
        for filename in dirr:
            img = cv2.imread(os.path.join(self.output_folder,filename))
            if img is not None and "frame" not in filename:
                self.img_no_frame.append(img)
                self.img_with_frame.append(cv2.imread(os.path.join(self.output_folder,filename[:filename.find(".")]+"_frame"+filename[filename.find("."):])))

        if len(self.img_no_frame[self.index].shape)<3:
            frame = cv2.cvtColor(self.img_no_frame[self.index], cv2.COLOR_GRAY2RGB)
        else:
            frame = cv2.cvtColor(self.img_no_frame[self.index], cv2.COLOR_BGR2RGB)
            
        h, w = self.img_no_frame[self.index].shape[:2]
        bytesPerLine = 3 * w
        qimage = QImage(frame.data, w, h, bytesPerLine, QImage.Format.Format_RGB888) 
        pix = QPixmap(qimage)
        self.label.setPixmap(pix.scaled(1700,650, QtCore.Qt.KeepAspectRatio))
        
        self.label_3.setText("Result saved in " + self.output_folder)
            
        self.nextButton.clicked.connect(lambda: self.nextPhoto(self.img_no_frame) if self.mode == 0 else self.nextPhoto(self.img_with_frame))
        self.quitButton.clicked.connect(lambda: QApplication.closeAllWindows())
        self.withoutFrame.clicked.connect(lambda: self.changeMode(0))
        self.withFrame.clicked.connect(lambda: self.changeMode(1))

    def changeMode(self, flag):
        if(self.mode != flag):
            self.mode = not(self.mode)

        if (self.mode):
            self.nextPhoto(self.img_with_frame, mode=True)
        else:
            self.nextPhoto(self.img_no_frame, mode=True)

    def nextPhoto(self, images, mode=False):
        if not mode:
            self.index += 1
        if(self.index >= len(images)):
            self.index = 0

        if len(images[self.index].shape)<3:
            frame = cv2.cvtColor(images[self.index], cv2.COLOR_GRAY2RGB)
        else:
            frame = cv2.cvtColor(images[self.index], cv2.COLOR_BGR2RGB)

        h, w = images[self.index].shape[:2]
        bytesPerLine = 3 * w
        qimage = QImage(frame.data, w, h, bytesPerLine, QImage.Format.Format_RGB888) 
        pix = QPixmap(qimage)
        self.label.setPixmap(pix.scaled(1700,650, QtCore.Qt.KeepAspectRatio))
                
def main():
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
        widget = QtWidgets.QStackedWidget()
        welcome = WelcomeScreen(widget)
        widget.addWidget(welcome)
        widget.showMaximized()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")

if __name__ == "__main__":
    main()        
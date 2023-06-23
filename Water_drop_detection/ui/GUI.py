import cv2
import sys
import os

from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

from NN.TestNetwork import work

def detect_image(filepath, output):
    """Takes the path to the image and the name of the folder to save the result and sends it to the function for detecting drops."""

    work(filepath, output, ".jpg", mode = "picture")

def detect_folder(filepath, output):
    """Takes the path to the folder and the name of the folder to save the result and sends it to the function for detecting drops."""

    work(filepath, output, ".jpg")

class WelcomeScreen(QMainWindow):
    """The class of the original UI screen."""

    def __init__(self, widget):
        super(WelcomeScreen,self).__init__()

        loadUi("water_drop_detection/ui/ui/page1.ui", self)
        self.widget = widget
        pixmap = QPixmap('water_drop_detection/ui/logo/logobig.png')
        self.label.setPixmap(pixmap)
        self.label_2.setPixmap(QPixmap('water_drop_detection/ui/logo/wallpaper1.jpg'))
        self.start_btn.clicked.connect(lambda: self.start_click())
           
    def start_click(self):
        """Function to go to the next page."""

        select_file = SelectScreen(self.widget) 
        self.widget.addWidget(select_file)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

class SelectScreen(QMainWindow):
    """Class for the detection object selection screen."""

    def __init__(self, widget):
        super(SelectScreen,self).__init__()

        loadUi("water_drop_detection/ui/ui/page2.ui", self)
        self.widget = widget
        self.setAcceptDrops(True)
        self.label_2.setPixmap(QPixmap('water_drop_detection/ui/logo/wallpaper1.jpg'))
        self.pushFolderButton.clicked.connect(lambda: self.open_folder())
        self.pushImageButton.clicked.connect(lambda: self.open_image())
    
    def open_folder(self):
        """A function for selecting a folder and going to the next page."""

        file = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')

        if os.path.exists(file):
            select_file = FolderPretrainScreen(file, self.widget) 
            self.widget.addWidget(select_file)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        
    def open_image(self):
        """A function for selecting an image and going to the next page."""

        file = QtWidgets.QFileDialog.getOpenFileName(self, "Select Image", None, "Image (*.png *.jpg *.jpeg)")[0]

        if "jpeg" in file or "jpg" in file or "png" in file:
            select_file = ImagePretrainScreen(file, self.widget) 
            self.widget.addWidget(select_file)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        
    def dragEnterEvent(self, event):
        """A function that tracks the transfer of an image/folder to a widget."""

        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        """A function that tracks the transfer of an image/folder to a widget."""

        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """A function that captures the path of the image/folder on which drops want to be detected."""

        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            self.file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image(self.file_path)
            event.accept()
        else:
            event.ignore()

    def set_image(self, file):
        """Function to move to the next slide if the image/folder has been moved to the widget."""

        if "jpeg" in file or "jpg" in file or "png" in file:
            select_file = ImagePretrainScreen(file, self.widget) 
            self.widget.addWidget(select_file)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        else:
            select_file = FolderPretrainScreen(file, self.widget) 
            self.widget.addWidget(select_file)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

class ImagePretrainScreen(QMainWindow):
    """A class for the image display screen before detection."""

    def __init__(self, file, widget):
        super(ImagePretrainScreen,self).__init__()

        loadUi("water_drop_detection/ui/ui/page3_image.ui", self)
        self.file = file
        self.widget = widget
        self.pixmap = QPixmap(file)
        self.label_2.setPixmap(QPixmap('water_drop_detection/ui/logo/wallpaper1.jpg'))

        super().layout().activate()
        self.label.setPixmap(self.pixmap.scaled(1700, 717, QtCore.Qt.KeepAspectRatio))
        self.toNeuralButton.clicked.connect(lambda: self.findDrops(file))
        self.ImageProcessingButton.clicked.connect(lambda: self.ImageProcessing(file))
        self.BackButton.clicked.connect(lambda: self.Back())

    def findDrops(self, file):
        """Function for switching to the detection slide."""

        select_file = FolderResultScreen(file, 0, self.widget) 
        self.widget.addWidget(select_file)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        
    def ImageProcessing(self, file):
        """Function for switching to the image processing slide."""

        select_file = EditScreen(file, self.widget)
        self.widget.addWidget(select_file)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        
    def Back(self):
        """Function to return to the previous slide."""

        select_file = SelectScreen(self.widget)
        self.widget.addWidget(select_file)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

class FolderPretrainScreen(QMainWindow):
    """A class for displaying the folder name before detecting it."""
    
    def __init__(self, file, widget):
        super(FolderPretrainScreen,self).__init__()

        loadUi("water_drop_detection/ui/ui/page3_folder.ui", self)
        self.widget = widget
        self.label.setText("Your choice: \n" + file)
        self.label_3.setPixmap(QPixmap('water_drop_detection/ui/logo/wallpaper1.jpg'))
        print(file)
        
        self.toNeuralButton.clicked.connect(lambda: self.findDrops(file))
        self.BackButton.clicked.connect(lambda: self.Back())
    
    def findDrops(self, file):
        """Function for switching to the detection slide."""

        select_file = FolderResultScreen(file, 1, self.widget) 
        self.widget.addWidget(select_file)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        
    def Back(self):
        """Function to return to the previous slide."""

        select_file = SelectScreen(self.widget) 
        self.widget.addWidget(select_file)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

class EditScreen(QMainWindow):
    """A class for the input image processing screen."""

    def __init__(self, file, widget):
        super(EditScreen,self).__init__()

        loadUi("water_drop_detection/ui/ui/page4_image.ui", self)
        self.rotation = 0
        self.widget = widget
        self.pixmap = QPixmap(file)
        self.photos = [QPixmap(file)]
        self.edit_pixmap = QPixmap(file)
        self.label_2.setPixmap(QPixmap('water_drop_detection/ui/logo/wallpaper1.jpg'))
        self.label.setPixmap(QPixmap(file).scaled(1700, 717, QtCore.Qt.KeepAspectRatio))
        
        self.okButton.clicked.connect(lambda: self.OK_button(file))
        self.backButton.clicked.connect(lambda: self.Back_button())
        self.rotateButton.clicked.connect(lambda: self.Rotate_button())
 
    def OK_button(self, file):
        """Function to switch to the detection slide."""

        self.photos[-1].save('pixmap.png')
        select_file = FolderResultScreen(file, 0, self.widget) 
        self.widget.addWidget(select_file)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        
    def Back_button(self):
        """A function to cancel the last processing action."""

        if len(self.photos) > 1:
            self.photos.pop()
            self.label.setPixmap(self.photos[-1].scaled(1700, 717, QtCore.Qt.KeepAspectRatio))
    
    def Rotate_button(self):
        """Function for rotating the image by 90 degrees."""

        pixmap = self.edit_pixmap.copy()
        self.rotation += 90
        transform = QtGui.QTransform().rotate(90)
        pixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)
        self.label.setPixmap(pixmap.scaled(1700, 717, QtCore.Qt.KeepAspectRatio))
        self.edit_pixmap = pixmap
        self.photos.append(pixmap)
        pixmap.save('pixmap.png')
        
    def mousePressEvent(self, eventQMouseEvent):
        """A function for tracking mouse clicks on a widget with an image."""

        offset = self.label.pos()
        self.label.originQPoint = eventQMouseEvent.pos() - offset
        self.label.currentQRubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self.label)
        self.label.currentQRubberBand.setGeometry(QtCore.QRect(self.label.originQPoint, QtCore.QSize()))
        self.label.currentQRubberBand.show()

    def mouseMoveEvent(self, eventQMouseEvent):
        """A function for tracking the movement of the previously pressed mouse button 
        on the widget with the image and building a rectangle for cropping."""

        offset = self.label.pos()
        self.label.currentQRubberBand.setGeometry(QtCore.QRect(self.label.originQPoint, eventQMouseEvent.pos() - offset).normalized())

    def mouseReleaseEvent(self, eventQMouseEvent):
        """A function for cropping the image along the resulting rectangle after pressing the mouse button."""

        self.label.currentQRubberBand.hide()
        currentQRect = self.label.currentQRubberBand.geometry()
        self.label.currentQRubberBand.deleteLater()
        self.edit_pixmap = self.label.grab(currentQRect)
        self.photos.append(self.edit_pixmap)
        self.label.setPixmap(self.edit_pixmap.scaled(self.label.size(), QtCore.Qt.KeepAspectRatio))
        self.edit_pixmap.save('pixmap.png')

class FolderResultScreen(QMainWindow):
    """A class for the detection result display screen."""

    def __init__(self, input_folder, flag, widget):
        super(FolderResultScreen,self).__init__()

        loadUi("water_drop_detection/ui/ui/page5_folder.ui", self)
        self.widget = widget
        self.label_4.setPixmap(QPixmap('water_drop_detection/ui/logo/wallpaper1.jpg'))

        if not flag:

            self.output_folder = input_folder[:len(input_folder) - 1 - input_folder[::-1].index('/') + 1] \
                + "detected_"+ input_folder[len(input_folder) - 1 - input_folder[::-1].index('/') + 1:input_folder.find(".")]
            
            if os.path.exists("pixmap.png"):
                detect_image("pixmap.png", self.output_folder)
                os.remove("pixmap.png")
            else:
                detect_image(input_folder, self.output_folder)

        else:
            self.output_folder = input_folder + '/detected'
            detect_folder(input_folder, self.output_folder)

        self.mode = 0
        self.index = 0
        self.img_no_frame = []
        self.img_with_frame = []

        dirr = sorted(os.listdir(self.output_folder))

        for filename in dirr:
            img = cv2.imread(os.path.join(self.output_folder,filename))
            
            if img is not None and "frame" not in filename:
                self.img_no_frame.append(img)
                self.img_with_frame.append(cv2.imread(os.path.join(self.output_folder, filename[:filename.find(".")] \
                                                                   + "_frame" + filename[filename.find("."):])))

        if len(self.img_no_frame[self.index].shape) < 3:
            frame = cv2.cvtColor(self.img_no_frame[self.index], cv2.COLOR_GRAY2RGB)
        else:
            frame = cv2.cvtColor(self.img_no_frame[self.index], cv2.COLOR_BGR2RGB)
            
        h, w = self.img_no_frame[self.index].shape[:2]
        bytesPerLine = 3 * w
        qimage = QImage(frame.data, w, h, bytesPerLine, QImage.Format.Format_RGB888) 
        pix = QPixmap(qimage)
        self.label.setPixmap(pix.scaled(1700, 650, QtCore.Qt.KeepAspectRatio))
        
        self.label_3.setText("Result saved in " + self.output_folder)
            
        self.nextButton.clicked.connect(lambda: self.nextPhoto(self.img_no_frame) \
                                        if self.mode == 0 else self.nextPhoto(self.img_with_frame))
        
        self.quitButton.clicked.connect(lambda: QApplication.closeAllWindows())
        self.withoutFrame.clicked.connect(lambda: self.changeMode(0))
        self.withFrame.clicked.connect(lambda: self.changeMode(1))

    def changeMode(self, flag):
        """Function for changing the result viewing mode."""

        if(self.mode != flag):
            self.mode = not(self.mode)

        if (self.mode):
            self.nextPhoto(self.img_with_frame, mode = True)
        else:
            self.nextPhoto(self.img_no_frame, mode = True)

    def nextPhoto(self, images, mode = False):
        """Function to view the next image, if available."""

        if not mode:
            self.index += 1

        if self.index >= len(images):
            self.index = 0

        if len(images[self.index].shape) < 3:
            frame = cv2.cvtColor(images[self.index], cv2.COLOR_GRAY2RGB)
        else:
            frame = cv2.cvtColor(images[self.index], cv2.COLOR_BGR2RGB)

        h, w = images[self.index].shape[:2]
        bytesPerLine = 3 * w
        qimage = QImage(frame.data, w, h, bytesPerLine, QImage.Format.Format_RGB888) 
        pix = QPixmap(qimage)
        self.label.setPixmap(pix.scaled(1700, 650, QtCore.Qt.KeepAspectRatio))
                
def main():
    """A function to launch the start screen."""

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

    

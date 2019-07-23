#TODO: change camera photo capture method - opencv
#from datetime import datetime
import logging
logger = logging.getLogger(__name__)

from PIL import Image
import os


CW = 0
CCW = 1

class OCR:
    """
    Takes photo and converts to text

    """
    def capture_photo(self, image_filename):
        """
        Use picamera to capture a photo

        Args: int side
        Returns: None
        """
        self.image_filename = image_filename
        os.system('fswebcam -d /dev/video0 -r 320x240 -S 3 --jpeg 50 --no-banner --save '+ self.image_filename)

    def capture_usb_photo(self, image_filename):
        """
        Use USB_cam to capture a photo.
        """
        self.image_filename = image_filename
        os.system('fswebcam -d /dev/video2 -r 320x240 -S 3 --jpeg 50 --no-banner --save '+ self.image_filename)


    def image_to_text(self):
        """
        ##########Unimplemented##########
        Function to read text from images.
        """

        # im = Image.open("IDCARD1.PNG")
        #text = pytesseract.image_to_string(im , lang = 'eng')
        self.text = "<OCR PLACEHOLDER TEXT>"
        #self.text = pytesseract.image_to_string(im, lang='eng+mal', config='--psm 6')
        return self.text


    def detect_language(self):
        """
        Unimplemented
        """
        pass

    def correct_orientation(self):
        """
        Unimplemented
        """
        pass

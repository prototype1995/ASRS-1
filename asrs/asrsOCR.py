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

    def crop_image(self, image, cam_num):
        """
        Method to crop image according to camera number.
        """
        if cam_num == 1:
            coords = (20, 25, 310, 210)
            image_obj = Image.open(image)
            cropped_image = image_obj.crop(coords)
            return cropped_image.save('cropped_usb1_img.jpg')
        else:
            coords = (30, 20, 295, 180) #1 -- (20, 18, 295, 180)
            image_obj = Image.open(image)
            cropped_image = image_obj.crop(coords)
            return cropped_image.save('cropped_usb2_img.jpg')


    def capture_photo(self, image_filename):
        """
        Use USB-Camera-1 to capture a photo

        Args: int side
        Returns: None
        """
        self.image_filename = image_filename
        try:
            try:
                os.system('fswebcam -d /dev/video0 -r 320x240 -S 3 --jpeg 50 --no-banner --save '+ self.image_filename)
                self.crop_image(image_filename, 1)
                logger.info("Capturing image with /dev/video0.")
            except:
                os.system('fswebcam -d /dev/video1 -r 320x240 -S 3 --jpeg 50 --no-banner --save '+ self.image_filename)
                self.crop_image(image_filename, 1)
                logger.info("Skipped /dev/video0...trying to capture image with /dev/video1.")
        except:
            print("Camera not detected... Check camera connection")
            logger.warning("Camera not detected")


    def capture_usb_photo(self, image_filename):
        """
        Use USB_Camera-2 to capture a photo.
        """
        self.image_filename = image_filename
        try:
            try:
                os.system('fswebcam -d /dev/video2 -r 320x240 -S 3 --jpeg 50 --no-banner --save '+ self.image_filename)
                self.crop_image(image_filename, 2)
                logger.info("Capturing image with /dev/video2.")
            except:
                os.system('fswebcam -d /dev/video3 -r 320x240 -S 3 --jpeg 50 --no-banner --save '+ self.image_filename)
                self.crop_image(image_filename, 2)
                logger.info("Skipped /dev/video2...trying to capture image with /dev/video3.")
        except:
            print("Camera not detected...Check camera connection")
            logger.warning("Camera not detected")


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

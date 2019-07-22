
import logging
logger = logging.getLogger(__name__)

from datetime import datetime

class Slot:
    """
    slot_id   : Integer, stores the unique id of a slot
    status    : Boolean, stores the storage status of a slot: 0 = empty; 1 = used.
    datetime_in : String, Time at which the card was stored
    datetime_out : String, Time at which the card was retrieved
    ocr_info : String, Extracted string info from the images.
    """
    def __init__(self, t):
        """
        Args: all slot parameters in a tuple (slot_id, uid, status, datetime_in,
                                              ocr_info)
        Returns: None
        """
        self.slot_id = t[0]
        self.uid = t[1]
        self.status = t[2]
        self.datetime_in = t[3]
        self.ocr_info = t[4]

    def copy(self, s):
        """
        Method to update current slot object with another
        Args: Slot object s
        Returns: None
        """
        self.slot_id = s.slot_id
        self.status = s.status
        self.uid = s.uid
        self.datetime_in = s.datetime_in
        self.ocr_info = s.ocr_info



    def gen_uid(self):
        """
        Method to generate a UID
        Args: None
        Returns: None
        """
        self.uid = "ASRS" + str(hash(self.datetime_in))

    def get_tuple(self, to_records = False):
        """
        Args: boolean to_records - whether it is being called by records or current table
        Returns: Tuple of members
        """
        if to_records:
            return (self.uid, self.datetime_in, self.datetime_out, self.ocr_info)
        else:
            return (self.slot_id, self.uid, self.status, self.datetime_in, self.ocr_info)


    def get_datetime(self):
        """
        Method to get current datetime
        Args: None
        Returns: Str datetime
        """
        dt = datetime.now()
        return dt.strftime("%Y%m%d%H%M%S")

    def get_image_filename(self, side=1):
        """
        Method to set image file name
        Args: int side = 1
        Returns: str image_filename
        """
        logger.debug("Image filename {}_{}.jpg".format(self.datetime_in, side))
        return "{}_{}.jpg".format(self.datetime_in, side) #CAMERA NOT WORKING

    def set_datetime_in(self):
        """
        SEts the datetime_in varialble

        Args: None
        Returns: None
        """
        self.datetime_in = self.get_datetime()

    def set_datetime_out(self):
        """
        Sets the datetime_out variable on retrieval

        Args: None
        Returns: None
        """
        self.datetime_out = self.get_datetime()


    def get_photo(self, side=1, dirpath="asrsphotos"):
        """
        Returns path where the photo is saved

        Args: integer - side 1 or 2
              string - path to directory
        Returns: string - image full path
        """
        return "{}/{}_{}.jpg".format(dirpath, self.datetime_in, side)

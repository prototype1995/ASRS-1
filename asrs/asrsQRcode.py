#Generate QR qr_code
#print QR code with the thermal printer

import logging
logger = logging.getLogger(__name__)

from escpos.printer import Dummy
import pyqrcode
import pyudev
from datetime import datetime


def detect_printer():
    """
    Function to detect if the printer is present in /dev/usb/lp*
    Returns Boolean
    """
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='usb')

    for device in iter(monitor.poll, None):
        if device.action == 'add':
            logger.info('{} Connected'.format(device))
        else:
            logger.warning("Printer not Connected.")

def printer_check_routine():
    """
    Do a demo print
    """
    d = Dummy()
    d.text("-"*30)
    d.text("\n"*3)
    d.text("Test Print")
    d.text("\n"*3)
    d.text("-"*30)
    d.text("\n"*3)
    #TODO: add exception when lp not found
    with open("/dev/usb/lp0", "wb") as f:
        data = b"".join(d._output_list)
        f.write(data)
        f.close()

def generate_qrcode(text):
    """
        Function to create qr code for the given text.
        Args : Text to be stored in QR code.
        Returns : QRcode image.
    """
    qrcode = pyqrcode.create(text)
    image = qrcode.png("QRCODE.PNG", scale=6)



def print_qr_code(text):
    """
        Function to write to /dev/usb/lp*
        Arguments: Text to be stored in QR qr_code
        Return: None

        QR code data bytes are creted using escpos library's Dummy class
    """
    d = Dummy()
    d.text("Company Name Place Holder\n\n\n")
    d.text("{}\n\n\n".format(datetime.strftime(datetime.now(), "%D - %H:%M:%S")))
    d.qr(text, ec=3, size=8, model=2, native=False)
    d.text("\n"*6)
    d.text("-"*30)
    d.text("\n"*3)
    #TODO: add exception when lp not found
    with open("/dev/usb/lp0", "wb") as f:
        data = b"".join(d._output_list)
        f.write(data)
        f.close()

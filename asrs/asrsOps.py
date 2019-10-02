#Module containing higher level operations of the ASRS

import logging
logger = logging.getLogger(__name__)

import RPi.GPIO as GPIO
import configparser
import os
import psutil
import platform
import datetime
import time
import json

from asrs import asrsMotor
from asrs import asrsDB
from asrs import asrsSlots
from asrs import asrsOCR
from asrs import asrsQRcode as qr

from shutil import copyfile



config_file = "/home/pi/Project/ASRS3/server/asrsConfig.conf"
config = configparser.ConfigParser()
config.read(config_file)

#card detection pin declarations
card_limit_pin = 36
GPIO.setmode(GPIO.BOARD)
GPIO.setup(card_limit_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

db = asrsDB.ASRSDataBase()
logger.info("db created...")

#Create actuator objects
m1 = asrsMotor.StepperMotor(step_pin=config.getint('STEPPERMOTOR', 'M1_STEP_PIN'),
                            dir_pin=config.getint('STEPPERMOTOR', 'M1_DIR_PIN'),
                            limit_pin=config.getint('STEPPERMOTOR', 'M1_LIM_PIN'),
                            step_angle=config.getfloat('STEPPERMOTOR', 'M1_STEP_ANGLE'),
                            stepping = 16,
                            delay=0.00001, res=0.01)

logger.info("m1 created...")
m2 = asrsMotor.StepperMotor(step_pin=config.getint('STEPPERMOTOR', 'M2_STEP_PIN'),
                            dir_pin=config.getint('STEPPERMOTOR', 'M2_DIR_PIN'),
                            limit_pin=config.getint('STEPPERMOTOR', 'M2_LIM_PIN'),
                            step_angle=config.getfloat('STEPPERMOTOR', 'M2_STEP_ANGLE'),
                            stepping = 16,
                            delay=0.00001, res=1)
logger.info("m2 created...")

s1 = asrsMotor.Solenoid(in1_pin=config.getint('SOLENOID', 'S1_PIN'))
logger.info("s1 created...")

l1 = asrsMotor.LED(in1_pin=config.getint('LED', 'L1_PIN'))
logger.info("l1 created...")

logger.debug("Reading Offsets from config file")

offset_storage = config.getfloat('SLOTS', 'offset_storage')
offset_retrieval = config.getfloat('SLOTS', 'offset_retrieval')
cardTray_pitch = config.getfloat('SLOTS', 'cardTray_pitch')

logger.info("Intial Homing axes...")

#m2.go_home(delay=0.0001)
#m1.go_home(delay=0.0001)

logger.info("Initial Homing axes complete.")

ocr = asrsOCR.OCR()
slot = asrsSlots.Slot((0, '', 0, '', ''))


#### Storage && Retrieval position list
storage_list = [2.1, 2.7, 3.3, 3.9, 4.6, 5.2, 5.8, 6.6, 7.0, 7.6, 8.3, 8.9, 9.5, 10.1, 10.7, 11.5, 12, 12.6, 13.2, 13.8, 14.5, 15.1, 15.7, 16.35, 16.95, 17.75, 18.2, 18.85, 19.45, 20.05, 20.65, 21.3, 22.05]
retrieval_list = [8.5, 9.2, 9.9, 10.5, 11.1, 11.7, 12.3, 13, 13.6, 14.2, 14.8, 15.4, 16.1, 16.7, 17.3, 17.9, 18.6, 19.2, 19.8, 20.4, 21, 21.7, 22.3, 23, 23.6, 24.2, 24.8, 25.4, 26, 26.6, 27.25, 27.9, 28.5] 

def move_to_slot(pos=0, storage=True):
    """Move the storage rack to the specified position

    Args: int pos - default 0
          boolean storage - defualt True - determines weather storing or retrieving
                                    False - retrieval
    Returns: None
    """
    logger.debug("offsets & pitch ({}, {}, {}) ".format(offset_storage, offset_retrieval, cardTray_pitch))
    global storage_list
    global retrieval_list

    if storage:
        # move slot no. given by pos to storage operation
        rev = storage_list[pos]
        logger.info("Moving to slot {} for storage: abs_pos = {}deg".format(pos, rev))
    else:
        # move slot no. given by pos to retrieval operation
        rev = retrieval_list[pos]
        logger.info("Moving to slot {} for retrieval: abs_pos = {}deg".format(pos, rev))

    m1.drive_motor(revolutions = rev, direction = 1, delay = 0.00001)
    return rev


def init_storage_seq():
    """
    Method to intialize storage sequence
    """
    logger.debug("init_storage_seq() called...")
    slot.slot_id = db.get_empty_slot()
    rev = move_to_slot(slot.slot_id, storage=True)
    content = '''{{ "cmd": "{}",
                    "revolutions": "{}",
                    "pos": "{}"}}'''.format("init_storage_seq()", rev, slot.slot_id)
    logger.debug(content)
    return(True, bytes(content, "UTF-8"))


def init_image_proc():
    """
    Method to initialize image processing sequence
    """
    logger.debug("init_image_proc() method called.")
    slot.set_datetime_in()

    l1.fire_led(state=True) # Turned ON LED.

    logger.info("Capturing image of side 1...")
    ocr.capture_photo(slot.get_image_filename(side=1))
    copyfile(slot.get_image_filename(side=1), "IDCARD1.JPG")

    logger.info("Capturing image of side 2...")
    ocr.capture_usb_photo(slot.get_image_filename(side=2))
    copyfile(slot.get_image_filename(side=2), "IDCARD2.JPG")

    l1.fire_led(state=False) # Turned OFF LED

    logger.info("Generating QRcode.")
    slot.gen_uid()
    qr.generate_qrcode(slot.uid)

    content = '''{{ "cmd": "{}",
                    "slot": "{}"}}'''.format("init_image_proc()", slot.get_tuple())
    logger.debug(content)
    return(True, bytes(content, "UTF-8"))


def confirm_storage(data = " ", prints="False"):
    logger.debug("confirm_storage() called...")
    s1.fire_solenoid(3)
    logger.info("Updating slot object.")
    slot.status = 1
    logger.info("Adding OCR data to slot object...")
    slot.ocr_info = data
    db.update_current(slot)
    db.insert_to_records(slot)
    if prints=="True":
        qr.print_qr_code(slot.uid)
        cmd = "confirm_storage_print_with_data()"
    else:
        cmd = "confirm_storage_noPrint_with_data()"
    m1.go_home(delay=0.00001) # moving back to home position.
    logger.info("Returning to home position... [OBSOLETE]")
    logger.info("Homing complete.")
    content = '''{{ "cmd": "{}",
                    "slot": "{}"}}'''.format(cmd, slot.get_tuple())
    logger.debug(content)
    return content


def confirm_retrieval():
    logger.debug("confirm_retrieval() called...")
    logger.info("Updating Date-time out in Records")
    db.update_rec_datetimeout(slot.get_datetime(), slot.uid)
    move_to_slot(pos=slot.slot_id, storage=False)
    db.delete_from_current(slot)
    reset_slot = asrsSlots.Slot((slot.slot_id, '', 0, '', ''))
    db.insert_to_current(reset_slot)
    logger.debug("Retireval...")
    m2.drive_motor(revolutions=98, direction=1)
    m2.go_home()
    #db.update_slot_status(slot.slot_id, 1)
    content = '''{{ "cmd": "{}",
                    "slot": "{}"}}'''.format("confirm_retrieval()", slot.get_tuple())
    logger.debug(content)
    return(True, bytes(content, "UTF-8"))

def purge_all_cards():
    logger.info("Homing...")
    auto_home()
    logger.info("Purging all cards...")
    for i in range(33):
        move_to_slot(pos=i, storage=False)
        push_card()
        auto_home()

    logger.info("Deleting database and all images...")
    os.system("rm ASRS_records.db *.jpg user_files/*")
    os.system("sudo reboot -h now")

    content = '''{{"cmd":"{}"
                    "slot": "{}"}}'''.format("purge_all_cards()", slot.get_tuple())
    return(True, bytes(content, "UTF-8"))


def detect_card(card_limit_pin=36):
    """
    Method for card detection.
    """
    logger.debug("detect_card() called...")
    while not GPIO.input(card_limit_pin):
        return(False,bytes("False","UTF-8"))
    while GPIO.input(card_limit_pin):
        return(True,bytes("True","UTF-8"))

def push_card():
    logger.info("Push Card...")
    m2.drive_motor(revolutions=98,direction=1)
    m2.go_home()
    content = '''{{"cmd":"{}"
                   "slot":"{}"}}'''.format("push_card()",slot.get_tuple())
    return(True, bytes(content, "UTF-8"))

def print_test():
    logger.info("Printer testing...")
    qr.printer_check_routine()
    content = '''{{"cmd":"{}"
                   "slot":"{}"'''.format("print_test()",slot.get_tuple())
    return(True, bytes(content, "UTF-8"))

def solenoid_test():
    logger.info("Testing Solenoid...")
    s1.fire_solenoid(2)
    content = '''{{ "cmd": "{}",
                    "slot": "{}"}}'''.format("solenoid_test()", slot.get_tuple())
    return(True, bytes(content, "UTF-8"))

def stepperMotor_test():
    logger.info("Testing carousel motor...")
    m1.drive_motor(revolutions = 1, direction= 1)
    m1.go_home()
    content = '''{{ "cmd": "{}",
                    "slot": "{}"}}'''.format("stepperMotor_test()", slot.get_tuple())
    return(True, bytes(content, "UTF-8"))

def piCamera_test():
    logger.info("Testing PiCam...[file-name : piCam_test_image.jpg]")
    l1.fire_led(state=True)
    ocr.capture_photo("piCam_test_image.jpg")
    l1.fire_led(state=False)
    try:
        with open("piCam_test_image.jpg", 'rb') as file:
            return(True, file.read())
    except:
        return(False, "")

def usbCamera_test():
    logger.info("Testing USB Cam...[file-name : usbCam_test_image.jpg]")
    l1.fire_led(state=True)
    ocr.capture_usb_photo("usbCam_test_image.jpg")
    l1.fire_led(state=False)
    try:
        with open("usbCam_test_image.jpg", 'rb') as file:
            return(True, file.read())
    except:
        return(False, "")


def led_test():
    """
    Method to test LED.
    """
    l1.fire_led(state=True)
    time.sleep(2)
    l1.fire_led(state=False)
    content = '''{{ "cmd": "{}",
                    "slot": "{}"}}'''.format("led_test()", slot.get_tuple())
    return(True, bytes(content, "UTF-8"))


def go_home():
    logger.info("Homing... [OBSOLETE]")
    m1.go_home()
    m2.go_home()

    content = '''{{ "cmd": "{}",
                    "slot": "{}"}}'''.format("go_home()", slot.get_tuple())
    return(True, bytes(content, "UTF-8"))

def auto_home():
    logger.info("Auto Homing...")
    m2.go_home()
    m1.go_home()
    content = '''{{ "cmd": "{}",
                    "slot": "{}"}}'''.format("auto_home()", slot.get_tuple())
    return(True, bytes(content, "UTF-8"))

def pusher_go_home():
    m2.go_home()
    content = ""
    return(True, bytes(content,"UTF-8"))

def stepper_go_home():
    m1.go_home()
    content = ""
    return(True, bytes(content, "UTF-8"))

### Written for admin dashboard.

def cpu_usage():
    logger.debug("cpu_usage() called...")
    cpu_usage = psutil.cpu_percent()
    content = '''{{ "cmd": "{}",
                    "cpu": "{}"}}'''.format("cpuUsage()", cpu_usage)
    return(True, bytes(content,"UTF-8"))

def mem_usage():
    logger.debug("mem_usage() called...")
    mem_info = "Total memory : " + str(psutil.virtual_memory()[0]) + " >> Used Memory : " + str(psutil.virtual_memory()[3])
    content = '''{{ "cmd": "{}",
                    "mem": "{}"}}'''.format("memoryUsage()", mem_info)
    return(True, bytes(content, "UTF-8"))

def system_status():
    """
    Method to display the Disk usage, CPU usage and Memory usage.
    """
    logger.debug("system_status() called...")
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory()[2]
    disk_percent = psutil.disk_usage('/')[3]
    content = '''{{ "cmd": "{}",
                    "mem": "{}",
                    "cpu": "{}",
                    "disk":"{}"}}'''.format("system_status()", memory_percent, cpu_percent, disk_percent)
    return(True, bytes(content, "UTF-8"))

def list_all_curr_users():
    """
    Method to list all current users
    Args: None
    Returns: json
    """
    d = db.get_all_curr_users()
    content = json.dumps(d)
    return(True, bytes(content, "UTF-8"))


def list_all_users_by_date(date):
    """
    Method to list users by date.
    Args : Date
    Returns : {name : {uid : date_out}}
    """
    user_data = db.list_all_users_by_date(date)
    content = json.dumps(user_data)
    return content


def list_all_users_by_name(name):
    """
    Method to list users by name.
    Args : Name
    Returns : {uid : {date_in : date_out}}
    """
    user_list = db.list_slot_from_name(name)
    content = json.dumps(user_list)
    return content


def list_all_users_by_mobile(mob):
    """
    Method to list users by mobile number.
    Args : Name
    Returns : {uid : {date_in : date_out}}
    """
    user_list = db.list_slot_from_mobile(mob)
    content = json.dumps(user_list)
    return content


def list_curr_users_by_text(text):
    """
    Method to list users by name.
    Args : Text
    Returns : {uid : {name : date_in}}
    """
    user_list = db.check_ocr_substring(text)
    content = json.dumps(user_list)
    return content


def list_all_users_between_dates(date1, date2):
    """
    Method to list users b/w dates.
    Args : Date1, Date2
    Returns : {uid : name;dob;id;company;validity;date_in;date_out}
    """
    user_data = db.list_all_users_between_dates(date1, date2)
    content = json.dumps(user_data)
    return content


def short_list_users_between_dates(date1, date2):
    """
    Method to list users b/w dates.
    Args : Date1, Date2
    Returns : {uid : name;date_in;date_out}
    """
    user_data = db.short_list__users_between_dates(date1, date2)
    content = json.dumps(user_data)
    return content


def send_firstLast_dates():
    """
    Method to send first and last dates.
    Args : None.
    Returns : {first_date : last_date}
    """
    user_data = db.send_first_last_date()
    content = json.dumps(user_data)
    return(True, bytes(content, "UTF-8"))



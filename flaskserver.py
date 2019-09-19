#!/usr/bin/env python3

#TODO:
# Multi threading
# Update for Rpi as AP

###########Initialize logger##########
import logging
LOGFILE = 'testing/log.log'
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

import base64

#Set the logging format
formatter = logging.Formatter('%(asctime)s :: [%(levelname)s] - %(name)s - %(message)s')

#To output log to file
fh = logging.FileHandler(LOGFILE)
fh.setLevel(logging.DEBUG) #set the minimum logging level
fh.setFormatter(formatter)
logger.addHandler(fh)

#To output log to std stream
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)




from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import time
import os
from asrs import asrsOps as asrs
from shutil import copyfile
from datetime import datetime
import pyudev
import psutil


UPLOAD_FOLDER = 'user_files'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#####################HTTP Server####################

responses = { 'INIT_STORE'   : {
                         'cmd' : 'asrs.init_storage_seq()',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'application/json'
                        },
         'INIT_IMG_PROC': {
                         'cmd': 'asrs.init_image_proc()',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'application/json'
                        },
         'CONFIRM_STORE_NOPRINT': {
                         'cmd': 'asrs.confirm_storage(print=False)',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'application/json'
                       },
         'CONFIRM_STORE_PRINT':{
                        'cmd':'asrs.confirm_storage(print=True)',
                        'response-good': 200,
                        'response-bad': 406,
                        'content-type': 'text/plain'
                       },
         'CONFIRM_RETRIEVAL':{
                         'cmd': 'asrs.confirm_retrieval()',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'application/json'
                       },
         'GOHOME':  {
                         'cmd': 'asrs.go_home()',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'application/json'
                       },
         'AUTOHOME':  {
                         'cmd': 'asrs.auto_home()',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'application/json'
                       },
         'PUSHERGOHOME':  {
                         'cmd': 'asrs.pusher_go_home()',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'application/json'
                       },
         'STEPPERGOHOME':  {
                         'cmd': 'asrs.stepper_go_home()',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'application/json'
                        },
         'FETCHQRCODE':{ #todo : serve correct image "datetime_1.jpg"
                         #todo : rename PNG to JPG
                         'cmd': 'serve_image("QRCODE.PNG")',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'image/png'
                       },
         'FETCHIDCARD1':{
                         'cmd': 'serve_image("IDCARD1.JPG")',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'image/jpg'
                       },
         'FETCHIDCARD2':{
                         'cmd': 'serve_image("IDCARD2.JPG")',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'image/jpg'
                       },
         'GETUID'     :{
                         'cmd': 'serve_text(asrs.slot.uid)',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'text/plain'
                       },
         'DETECTCARD'     :{
                         'cmd': 'asrs.detect_card()',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'text/plain'
                        },
         'GETOCRINFO' :{
                         'cmd': 'serve_text(asrs.slot.ocr_info)',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'text/plain'
                       },
         'GETCOUNT' : {
                         'cmd': 'get_count()',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'application/json'
                      },
         'VALIDATEUID':{
                         'cmd': 'validate_uid()',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'text/plain'
                       },
         'PUSHCARD':{
                        'cmd':'asrs.push_card()',
                        'response-good': 200,
                        'response-bad': 406,
                        'content-type': 'text/plain'
                       },
         'PRINTTEST':{
                        'cmd': 'asrs.print_test()',
                        'response-good': 200,
                        'response-bad': 406,
                        'content-type': 'text/plain'
                       },
         'SOLENOIDTEST':{
                         'cmd': 'asrs.solenoid_test()',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'text/plain'
                       },
        'STEPPERMOTORTEST':{
                         'cmd': 'asrs.stepperMotor_test()',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'text/plain'
                       },
         'PUSHERMOTORTEST':{
                         'cmd': 'asrs.pusherMotor_test()',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'text/plain'
                       },
         'PICAMTEST':{
                         'cmd': 'asrs.piCamera_test()',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'image/jpg'
                       },
         'USBCAMTEST':{
                         'cmd': 'asrs.usbCamera_test()',
                        'response-good': 200,
                         'response-bad': 406,
                       'content-type': 'image/jpg'
                       },
         'LEDTEST':{
                         'cmd': 'asrs.led_test()',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'text/plain'
                       },
         'CPUUSAGE':{
                         'cmd': 'asrs.cpuUsage()',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'text/plain'
                       },
         'MEMINFO':{
                         'cmd': 'asrs.memoryUsage()',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'text/plain'
                       },
         'SYSTEMSTATUS':{
                         'cmd': 'asrs.system_status()',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'text/plain'
                       },
         'PURGEALL':{
                      'cmd': 'asrs.purge_all_cards()',
                      'response-good': 200,
                      'response-bad': 406,
                      'content-type': 'text/plain'
                      },
         'GETDB':{
                   'cmd': 'serve_db()',
                   'response-good': 200,
                   'response-bad': 406,
                   'content-type': 'application/x-sqlite3'
                      },
         'SENDDATE':{
                   'cmd': 'sent_ret_date()',
                   'response-good': 200,
                   'response-bad': 406,
                   'content-type': 'text/plain'
                     },
         'SENTIMAGE':{
                   'cmd': 'sent_user_photo()',
                   'response-good': 200,
                   'response-bad': 406,
                   'content-type': 'image/jpg'
                     },
         'GETOCR':{
                   'cmd': 'get_ocr_info()',
                   'response-good': 200,
                   'response-bad': 406,
                   'content-type': 'text/plain'
                    },
         'LSNAME':{
                   'cmd': 'list_slot_from_name()',
                   'response-good': 200,
                   'response-bad': 406,
                   'content-type': 'application/json'
                  },
         'LSBYDATES':{
                    'cmd': 'get_users_between_dates()',
                    'response-good': 200,
                    'response-bad': 406,
                    'content-type': 'application/json'
                    },
         'SHORTLSBYDATES':{
                    'cmd': 'get_short_list_between_dates()',
                    'response-good': 200,
                    'response-bad': 406,
                    'content-type': 'application/json'
                    },
         'DAILYACTS':{
                    'cmd': 'get_user_list_by_date()',
                    'response-good': 200,
                    'response-bad': 406,
                    'content-type': 'application/json'
                      },
         'VALIDATESLOT':{
                    'cmd': 'validate_slot()',
                    'response-good': 200,
                    'response-bad': 406,
                    'content-type': 'application/json'
                      },
         'LSALL':{
                    'cmd': 'asrs.list_all_curr_users()',
                    'response-good': 200,
                    'response-bad': 406,
                    'content-type': 'application/json'
                    },
         'CROP_COORDS':{
                     'cmd': 'crop_image_coords()',
                     'response-good': 200,
                     'response-bad': 406,
                     'content-type': 'application/json'
                       },
         'SHUTDOWN':{
                   'cmd': 'pi_shutdown()',
                   'response-good': 200,
                   'response-bad': 406,
                   'content-type': 'text/plain'
                  },
         'REBOOT':{
                   'cmd': 'pi_reboot()',
                   'response-good': 200,
                   'response-bad': 406,
                   'content-type': 'text/plain'
                  },
         'SETTIME':{
                   'cmd': 'set_time()',
                   'response-good': 200,
                   'response-bad': 406,
                   'content-type': 'text/plain'
                   },
         'REPORT':{
                   'cmd': 'copy_server_folder()',
                   'response-good': 200,
                   'response-bad': 406,
                   'content-type': 'text/plain'
                   },
         'UPDATESERVER':{
                   'cmd': 'update_server()',
                   'response-good': 200,
                   'response-bad': 406,
                   'content-type': 'text/plain'
                   }
      }



######################routes##################

response = ""

@app.route('/', methods=['GET', 'POST'])
def cmd_handler():
    global response
#    if request.method == 'POST':
#        file = request.files['file']
#        data = json.load(file)
#        print("POST : {}".format(request.form.to_dict()))
#        print("data : {}".format(data))
#        response = Response(response=data, status=200, content_type='application/json')
    if request.method == 'GET' or request.method == 'POST':
        cmd = request.args.get('cmd')
        print(request.args.to_dict())
        if cmd in responses:
            cmd_dict = responses[cmd]
            ret, content = eval(cmd_dict['cmd'])
            if ret:
                response = Response(response=content, status=cmd_dict['response-good'], content_type=cmd_dict['content-type'])
            else:
                response = Response(response=content, status=cmd_dict['response-bad'], content_type=None)
        else:
            response = Response(response="False", status=406, content_type=None)
    return response


####### IMG HANDLER ######
@app.route('/upload_file', methods=['GET', 'POST'])
def img_handler():
    if request.method == 'POST':
        filename = request.form.get('uid') + '.jpeg'
        file_b64 = bytes(request.form.get('file'), 'utf-8')
        with open("user_files/"+filename, 'wb') as fp:
            fp.write(base64.decodebytes(file_b64))
            #os.rename("user_files/"+filename,uid)
        #file = request.files['file']
        #print("POST : {}".format(request.files.to_dict()))
        #filename = secure_filename(file.filename)
        #print("filename : {}".format(filename))
        #file.save("user_files/"+filename)
        response = Response(response=filename, status=200)
    return response


def update_server():
    """
    Method to update server code.
    """
    try:
        os.system('git config user.email "bas3dp@gmail.com"')
        os.system('git config user.name "BAS3DP"')
        os.system('git pull https://BAS3DP:{}{}{}plaabs3dp@github.com/prototype1995/ASRS-1.git master')
        logger.info("Server updated successfully.")
        return(True, bytes("OK","UTF-8"))
    except:
        logger.info("Check internet connection.")
        return(False, bytes("-1","UTF-8"))


def copy_server_folder():
    """
    Method to copy the asrs folder to the external device.
    """
    try:
        context= pyudev.Context()
        removable = [device for device in context.list_devices(subsystem='block', DEVTYPE='disk') if device.attributes.asstring('removable') == "1"]
        for device in removable:
            partitions = [device.device_node for device in context.list_devices(subsystem='block', DEVTYPE='partition', parent=device)]
            for p in psutil.disk_partitions():
                if p.device in partitions:
                    removable_device = p.mountpoint
        os.system('cp -r /home/pi/Project/ASRS3/server {}'.format(removable_device))
        logger.info("Files copied to {}".removable_device)
        return(True, bytes("OK","UTF-8"))
    except:
        logger.info("Device not detected...Copying files failed.")
        return(False, bytes("-1","UTF-8"))


def set_time():
    """
    Method to set time in RPi.
    """
    datetime_str = request.args.get('value')
    #format_str = "%Y-%m-%d-%H:%M:%S"
    #date_str = datetime_str[:9]
    date_str = datetime_str.split(";")
    #time_str = datetime_str[9:]
    #datetime_val = datetime.strptime(datetime_str, format_str)
    #os.system("sudo date +%Y%m%d -s {}".format(date_str))
    #print("datetime {}".format(date_str))
    os.system('sudo date "+%F" -s "{}"'.format(date_str[0]))
    os.system('sudo date "+%T" -s "{}"'.format(date_str[1]))
    return(True, bytes("True", "UTF-8"))


def get_ocr_info():
    """
    Method to insert ocr info into ocr_table.
    """
    try:
        uid = request.args.get('uid')
        name = request.args.get('name')
        dob = request.args.get('dob')
        id = request.args.get('id')
        company = request.args.get('company')
        validity = request.args.get('validity')
        o = (uid, name, dob, id, company, validity)
        asrs.db.insert_to_ocr_table(o)
        logger.info("OCR values inserted...")
        return(True, bytes("True", "UTF-8"))
    except:
        logger.info("OCR value insertion failed...")
        return(False, bytes("-1", "UTF-8"))


def list_slot_from_name():
    """
    Method to list users by name.
    """
    name = request.args.get('name')
    try:
        content = asrs.list_all_users_by_name(name)
        return(True, bytes(content, "UTF-8"))
    except:
        logger.error("Invalid Name provided - {}".format(name))
        return(False, bytes("-1", "UTF-8"))


def sent_ret_date():
    """
    Method to return retrieval date from uid.
    """
    try:
        uid = request.args.get('uid')
        retrieval_date = asrs.db.return_date_out(uid)
        logger.info("Sending retrieval date-time of {}".format(uid))
        formatted_date = retrieval_date[0:4]+"-"+retrieval_date[4:6]+"-"+retrieval_date[6:8]+"---"+retrieval_date[8:10]+":"+retrieval_date[10:12]
        return(True, bytes(formatted_date, "UTF-8"))
    except:
        logger.warning("INVALID UID provided")
        return(False, bytes(" ", "UTF-8"))


def sent_user_photo():
    """
    Method to sent user photo.
    """
    uid = request.args.get('uid')
    ret, content = serve_image("user_files/"+uid+".jpeg")
    if ret:
        logger.info("User Photo sent.")
        return (True, content)
    else:
        logger.warning("Failed to fetch User Photo")
        return (False, bytes("-1", "UTF-8"))


def get_user_list_by_date():
    """
    Method to list users by date.
    """
    date = request.args.get('date')
#    try:
    content = asrs.list_all_users_by_date(date)
    return(True, bytes(content, "UTF-8"))
#    except:
#        logger.error("Invalid Date provided - {}".format(date))
#        return(False, bytes("-1", "UTF-8"))


def get_users_between_dates():
    """
    Method to list users b/w given dates.
    """
    date1 = request.args.get('date1')
    date2 = request.args.get('date2')
    try:
        content = asrs.list_all_users_between_dates(date1, date2)
        return(True, bytes(content, "UTF-8"))
    except:
        logger.error("Invalid Dates provided - {} & {}".format(date1, date2))
        return(False, bytes("-1", "UTF-8"))


def get_short_list_between_dates():
    """
    Method to show a short list of users n/w given dates.
    """
    date1 = request.args.get('date1')
    date2 = request.args.get('date2')
    try:
        content = asrs.short_list_users_between_dates(date1, date2)
        return(True, bytes(content, "UTF-8"))
    except:
        logger.error("Invalid Dates provided - {} & {}".format(date1, date2))
        return(False, bytes("-1", "UTF-8"))


def get_count():
    try:
        empty_slot = asrs.db.get_empty_slot()
        content = '''{{ "cmd": "{}", "empty_slot": "{}"}}'''.format("get_count()", empty_slot)
        return (True, bytes(content, "UTF-8"))
    except IndexError:
        return (False, bytes("-1", "UTF-8"))


def serve_text(content):
    if not content:
        content = "PlaceHolder Text"
        return (False, bytes(content, "UTF-8"))
    else:
        return (True, bytes(content, "UTF-8"))


def serve_image(filename):
    """
    Method to serve images
    Args: str filename
    Returns: Image file
    """
    try:
        with open(filename, 'rb') as file:
            return(True, file.read())
    except:
        return(False, "")


def serve_db():
    """
    Method to serve database.
    Args: None.
    Returns: DB
    """
    try:
        with open("ASRS_records.db",'rb') as file:
            return(True, file.read())
    except:
        return(False,"")


def validate_uid():
    """
    Method to validate uid
    """
    try:
        uid = request.args.get('uid')
        logger.info("Validating UID {}".format(uid))
        t = asrs.db.get_by_uid_from_current(uid) #sends a 200 response if successful
        logger.info("Validating UID {}".format(uid))
        print("new slot: {}".format(t))
        asrs.slot.copy(asrs.asrsSlots.Slot(t))
        copyfile(asrs.db.get_by_uid_image_filename(uid, side=1), "IDCARD1.JPG")
        copyfile(asrs.db.get_by_uid_image_filename(uid, side=2), "IDCARD2.JPG")
        content = '''{{ "cmd": "validate_uid()",
                        "slot": "{}"}}'''.format("init_storage_seq()", t)
        return(True, bytes(content, "UTF-8"))
    except ValueError:
            logger.warning("Invalid UID")
            content = '''{{ "cmd": "validate_uid()",
                            "slot": "{}"}}'''.format("init_storage_seq()", "-1")
            return(False, bytes(content, "UTF-8"))
    except KeyError:
        logger.warning("KeyError - No valid key named 'uid' in GET parameters")
        return (False, bytes("No key named uid", "UTF-8"))


def validate_slot():
    """
    Method to validate slot.
    """
    try:
        slot = request.args.get('slot')
        logger.info("Validating slot {}".format(slot))
        t = asrs.db.get_by_slot_id_from_current(slot) #sends a 200 response if successful
        logger.info("Validating slot {}".format(slot))
        print("new slot: {}".format(t))
        asrs.slot.copy(asrs.asrsSlots.Slot(t))
        copyfile(asrs.db.get_by_slot_id_image_filename(slot, side=1), "IDACRD1.JPG") #IDCARD1.JPG
        copyfile(asrs.db.get_by_slot_id_image_filename(slot, side=2), "IDCARD2.JPG") #IDCARD2.JPG
        content = '''{{ "cmd": "validate_slot()",
                        "slot": "{}"}}'''.format("init_storage_seq()", t)
        return(True, bytes(content, "UTF-8"))
    except ValueError:
            logger.warning("Invalid slot")
            content = '''{{ "cmd": "validate_slot()",
                            "slot": "{}"}}'''.format("init_storage_seq()", "-1")
            return(False, bytes(content, "UTF-8"))
    except KeyError:
        logger.warning("KeyError - No valid key named 'slot' in GET parameters")
        return (False, bytes("No key named slot", "UTF-8"))


def crop_image_coords():
    """
    Method to iset crop coordinates
    """
    try:
        coords = self.GET_args['coords'][0]
        side = int(self.GET_args['side'][0])-1
        t = tuple([int(float(i)) for i in coords.split(',')])
        logger.info("Converting coords to tuple ".format(t))
        asrs.crop_coordinates[side] = t
        logger.info("asrs.crop_coordinates = {}".format(asrs.crop_coordinates))
        content = '''{{ "cmd": "crop_image_coods()"
                        }}'''
        return(True, bytes(content, "UTF-8"))
    except KeyError:
        logger.warning("KeyError - No valid key named 'coords' or 'side' in GET parameters")
        return (False, bytes("No key named coords or side", "UTF-8"))


def pi_shutdown():
    """
    Method to shutdown pi.
    """
    os.system("sudo shutdown -h now")
#    return(True, bytes("OK", "UTF-8"))


def pi_reboot():
    """
    Method to reboot pi.
    """
    os.system("sudo reboot -h now")
#    return(True, bytes("OK", "UTF-8"))


if __name__ == "__main__":
    try:
        #auto detect ip
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        logger.info("Server started - %s:%s"%(ip, 9000))
        app.run(host=ip, port=9000, debug=True)

    except OSError as err:
        logger.error(err)

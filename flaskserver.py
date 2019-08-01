#!/usr/bin/env python3

#TODO:
# Multi threading
# Update for Rpi as AP

###########Initialize logger##########
import logging
LOGFILE = 'testing/log.log'
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

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


UPLOAD_FOLDER = 'user_photos'
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
         'DETECTCARD' :{
                          'cmd': 'asrs.detect_card()',
                          'response-good': 200,
                          'response-bad': 406,
                          'content-type': 'application/json'
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
          'SENDDATE':{
                   'cmd':'send_ret_date()',
                   'response-good': 200,
                   'response-bad': 406,
                   'content-type': 'text/plain'
                         },
#         'UPLOADIMAGE':{
#                   'cmd': 'upload_file()',
#                   'response-good' : 200,
#                   'response-bad' : 406,
#                   'content-type' : 'multipart/form-data'
#                      },
         'SENTIMAGE':{
                   'cmd': 'sent_user_photo()',
                   'response-good': 200,
                   'response-bad': 406,
                   'content-type': 'image/jpg'
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
    if request.method == 'GET':
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



####### IMG Handler #######
@app.route('/upload_file', methods=['GET', 'POST'])
def img_handler():
    if request.method == 'POST':
        file = request.files['file']
        print("POST : {}".format(request.form.to_dict()))
        filename = secure_filename(file.filename)
        print("filename : {}".format(filename))
        file.save("user_files/"+filename) #change acc
        response = Response(response=filename, status=200, content_type='application/json')
    return response



#def allowed_file(filename):
#    return '.' in filename and \
#        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#def upload_file():
#    if 'file' not in request.files:
#        print('No file part')
#        return redirect(request.url)
#    if request.method == 'POST':
#        file = request.files['file']
#        if file.filename == '':
#            print('No selected file')
#            return (False, bytes("-1", "UTF-8"))
#        if file and allowed_file(file.filename):
#            print("got file")
#            filename = secure_filename(file.filename)
#            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#            logger.info("File -'{}'- uploaded to user photos".format(filename))
#            return (True, bytes("file got", "UTF-8"))


def sent_user_photo():
    """
    Method to sent user photo.
    """
    uid = request.args.get('uid')
    ret, content = serve_image("user_files/"+uid)
    if ret:
        logger.info("User Photo sent.")
        return (True, content)
    else:
        logger.warning("Failed to fetch User Photo")
        return (False, bytes("-1", "UTF-8"))


def get_count():
    try:
        empty_slot = asrs.db.get_empty_slot()
        content = '''{{ "cmd": "{}", "empty_slot": "{}"}}'''.format("get_count()", empty_slot)
        return (True, bytes(content, "UTF-8"))
    except IndexError:
        return (False, bytes("-1", "UTF-8"))


def send_ret_date():
    """
    Method to send the retrieval date of given UID
    """
    try:
        uid = self.GET_args['uid'][0]
        retrieval_date = asrs.db.return_date_out(uid)
        logger.info("Sending retrieval date-time of {}".format(uid))
        formated_date = retrieval_date[0:4]+"-"+retrieval_date[4:6]+"-"+retrieval_date[6:8]+" at "+retrieval_date[8:10]+":"+retrieval_date[10:12]
        return(True, bytes(formated_date, "UTF-8"))
    except:
        logger.warning("INVALID UID provided.")
        return(False, bytes(" ", "UTF-8"))


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

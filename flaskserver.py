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




from flask import Flask, render_template, request, Response, jsonify
import time
from asrs import asrsOps as asrs
from shutil import copyfile


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
                         'cmd': 'self.serve_image("QRCODE.PNG")',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'image/png'
                       },
         'FETCHIDCARD1':{
                         'cmd': 'self.serve_image("IDCARD1.JPG")',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'image/jpg'
                       },
         'FETCHIDCARD2':{
                         'cmd': 'self.serve_image("IDCARD2.JPG")',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'image/jpg'
                       },
         'GETUID'     :{
                         'cmd': 'self.serve_text(asrs.slot.uid)',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'text/plain'
                       },
         'GETOCRINFO' :{
                         'cmd': 'self.serve_text(asrs.slot.ocr_info)',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'text/plain'
                       },
         'GETCOUNT' : {
                         'cmd': 'self.get_count()',
                         'response-good': 200,
                         'response-bad': 406,
                         'content-type': 'application/json'
                      },
         'VALIDATEUID':{
                         'cmd': 'self.validate_uid()',
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
                   'cmd': 'self.serve_db()',
                   'response-good': 200,
                   'response-bad': 406,
                   'content-type': 'application/x-sqlite3'
                  }
      }



######################routes##################

@app.route('/', methods=['GET', 'POST'])
def cmd_handler():
    logger.info(request.args.to_dict())








class ASRSHandler(BaseHTTPRequestHandler):

    status = 1

    def respond(self, cmd_response):
        """
        Select appropriate responses based on GET_args
        Args: dict opts eg: {'foo': ['bar'], 'one': ['1']}
        Returns: None
        """
        ret, content = eval(cmd_response['cmd'])
        if ret:
            self.send_response(cmd_response['response-good'])
            self.send_header('Content-type', cmd_response['content-type'])
        else:
            self.send_response(cmd_response['response-bad'])
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        """
        This method serves the 'GET' request, parses the arguments and
        send them to respond()
        """
        self.GET_args = parse_qs(urlparse(self.path).query)
        try:
            cmd = self.GET_args['cmd'][0]
            cmd_response = self.responses[cmd]
            self.respond(cmd_response)
        except KeyError as err:
            logger.warning("err - Invalid GET parameters.")


    def get_count(self):

        try:
            empty_slot = asrs.db.get_empty_slot()
            content = '''{{ "cmd": "{}", "empty_slot": "{}"}}'''.format("get_count()", empty_slot)
            return (True, bytes(content, "UTF-8"))
        except IndexError:
            return (False, bytes("-1", "UTF-8"))


    def serve_text(self, content):
        if not content:
            content = "PlaceHolder Text"
            return (False, bytes(content, "UTF-8"))
        else:
            return (True, bytes(content, "UTF-8"))


    def serve_image(self, filename):
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


    def serve_db(self):
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


    def validate_uid(self):
        """
        Method to validate uid
        """
        try:
            uid = self.GET_args['uid'][0]
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
        logger.info("Server started - %s:%s"%(HOST_NAME, PORT_NUMBER))
        app.run(host=ip, port=9000 debug=True)

    except OSError as err:
        logger.error(err)

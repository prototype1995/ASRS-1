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




import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from asrs import asrsOps as asrs

from shutil import copyfile
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-ip=", "--ip", required=True , help="ip address")
ap.add_argument("-port=", "--port", required=True , help="port number")
args = vars(ap.parse_args())

HOST_NAME = args['ip']
PORT_NUMBER = int(args['port'])





#####################HTTP Server####################

class ASRSHandler(BaseHTTPRequestHandler):

    status = 1
    responses = { 'SC2STORE'   : {
                                 'cmd' : 'asrs.init_storage_seq()',
                                 'response-good': 200,
                                 'response-bad': 406,
                                 'content-type': 'application/json'
                                },
                 'SC3CONTINUE': {
                                 'cmd': 'asrs.init_image_proc()',
                                 'response-good': 200,
                                 'response-bad': 406,
                                 'content-type': 'application/json'
                                },
                 'SC7CONFIRM': {
                                 'cmd': 'asrs.confirm_storage(print=False)',
                                 'response-good': 200,
                                 'response-bad': 406,
                                 'content-type': 'application/json'
                               },
                 'PRINT':{
                                'cmd':'asrs.confirm_storage(print=True)',
                                'response-good': 200,
                                'response-bad': 406,
                                'content-type': 'text/plain'
                               },
                 'SC14CONFIRM':{
                                 'cmd': 'asrs.confirm_retrieval()',
                                 'response-good': 200,
                                 'response-bad': 406,
                                 'content-type': 'application/json'
                               },
                 'SC9GOHOME':  {
                                 'cmd': 'asrs.stepper_go_home()',
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
                 'DETECTCARD' :{
                                 'cmd': 'asrs.detect_card()',
                                 'response-good': 200,
                                 'response-bad': 406,
                                 'content-type': 'application/json'
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
                          },
                 'DAILYACTS':{
                           'cmd': 'self.get_user_list_by_date()',
                           'response-good': 200,
                           'response-bad': 406,
                           'content-type': 'application/json'
                         },
                 'VALIDATESLOT':{
                           'cmd': 'self.validate_slot()',
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
                           'cmd':'self.send_ret_date()',
                           'response-good': 200,
                           'response-bad': 406,
                           'content-type': 'text/plain'
                         }

              }

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
            if cmd_response['content-type'] == 'application/x-sqlite3' :
                self.send_header('Content-Disposition', 'attachment ; filename = "ASRS_database.db"')
            
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
            logger.warning("err - Invalid GET parameters")


    def get_count(self):

        try:
            empty_slot = asrs.db.get_empty_slot()
            content = '''{{ "cmd": "{}", "empty_slot": "{}"}}'''.format("get_count()", empty_slot)
            return (True, bytes(content, "UTF-8"))
        except IndexError:
            return (False, bytes("-1", "UTF-8"))


    def send_ret_date(self):
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
            print(asrs.db.return_date_out(uid))
            logger.info("Validating UID {}".format(uid))
            t = asrs.db.get_by_uid_from_current(uid) #sends a 200 response if successfull
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
            print(asrs.db.return_date_out(uid))
            content = '''{{ "cmd": "validate_uid()",
                            "slot": "{}"}}'''.format("init_storage_seq()", "-1")
            return(False, bytes(content, "UTF-8"))

        except KeyError:
            logger.warning("KeyError - No valid key named 'uid' in GET parameters")
            print(asrs.db.return_date_out(uid))
            return (False, bytes("No key named uid", "UTF-8"))




if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), ASRSHandler)
    logger.info("Server started - %s:%s"%(HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logger.info("Server stopped - %s:%s"%(HOST_NAME, PORT_NUMBER))

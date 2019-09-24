
import logging
logger = logging.getLogger(__name__)


import sqlite3
import os

class ASRSDataBase:
    """
    The ASRS_records.db will have two TABLES - current & records

    CREATE TABLE current
                 (slot_id int, uid int, status int, datetime_in text, ocr_info text)
    pictures will be saved with datetime_in prefix

    CREATE TABLE records
                 (uid int, datetime_in text, datetime_out text, ocr_info text, mobile_num text)

    CREATE TABLE ocr_table
                 (uid int, name text, dob text, id text, company text, validity text)
    """

    __db_filename = "ASRS_records.db"
    def __init__(self, slot_count=None, inaccessible_slots=None):
        """
        Connect to the sqllite

        Args: None
        Returns: None
        """

        self.__conn = sqlite3.connect(self.__db_filename, check_same_thread=False)
        self.__c = self.__conn.cursor()
        if slot_count is None:
            self.slot_count = 33
        else:
            self.slot_count = slot_count

        if inaccessible_slots is None:
            self.inaccessible_slots = []
        else:
            self.inaccessible_slots = inaccessible_slots

        try:
            self.__c.execute('''CREATE TABLE current
                         (slot_id int, uid text, status int,
                         datetime_in text, ocr_info text)''')

            self.__c.execute('''CREATE TABLE records
                         (uid int, datetime_in text, datetime_out text,
                         ocr_info text, mobile_num text)''')

            self.__c.execute('''CREATE TABLE ocr_table
                         (uid int, name text, dob text, id text, company text,
                          validity text)''')

            #intialize dummy values for table current if the file is newly created
            for i in range(self.slot_count):
                if i not in self.inaccessible_slots:
                    status = 0
                else:
                    status = 1
                t  = (i, "", status, "", "")
                self.__c.execute('''INSERT into current(slot_id, uid,
                                    status, datetime_in, ocr_info)
                                    VALUES (?, ?, ?, ?, ?)''', t)
                self.__conn.commit()

        except:
            pass


    def get_current_slots(self):
        """
        Returns storage info from current

        Args: None
        Returns: list of Slot objects
        """
        current_slots = self.__c.execute('SELECT * FROM current ORDER BY slot_id')
        return current_slots.fetchall()

    def get_by_uid_from_current(self, uid):
        """
        Method to retrieve a slot by its uid
        Args: str uid
        Returns: tuple
        Exception: throws an exception if uid not found
        """
        logger.info("called get_by_uid_from_current()")
        t = (uid, )
        logger.info("t: {}".format(t))
        curr_slot = self.__c.execute('SELECT * FROM current WHERE uid = ?', t).fetchone()
        logger.info("current slot: {}".format(curr_slot))
        if not curr_slot:
            logger.error("Value error raised")
            raise ValueError("UID {} not found in database".format(uid))
        return curr_slot

    def get_by_uid_image_filename(self, uid, side=1):
        """
        Method to get filename string of the spcified uid
        Args: str uid, int side
        Returns: string
        """
        logger.info("Called get_by_uid)_image_filename()")
        t = (uid, )
        datetime_in = self.__c.execute('SELECT datetime_in FROM current WHERE uid = ?',t).fetchone()
        logger.info("Fetched datetime_in: {}".format(datetime_in))
        if not datetime_in:
            logger.error("Value error raised")
            raise ValueError("UID {} not found in database".format(uid))
        return "{}_{}.jpg".format(datetime_in[0], side)

    def get_by_slot_id_from_current(self, slot_id):
        """
        Method to retrieve a slot by its slot_id
        Args: str slot_id
        Returns: tuple
        Exception: throws an exception if uid not found
        """
        logger.info("called get_by_slot_id_from_current()")
        t = (slot_id, )
        logger.info("t: {}".format(t))
        curr_slot = self.__c.execute('SELECT * FROM current WHERE slot_id = ?', t).fetchone()
        logger.info("current slot: {}".format(curr_slot))
        if not curr_slot[2]: #if status is zero
            logger.error("Value error raised")
            raise ValueError("slot {} is empty".format(slot_id))
        return curr_slot

    def get_by_slot_id_image_filename(self, slot_id, side=1):
        """
        Method to get filename string of the spcified uid
        Args: str slot_id, int side
        Returns: string
        """
        logger.info("Called get_by_slot_id_image_filename()")
        t = (slot_id )
        datetime_in = self.__c.execute('SELECT datetime_in FROM current WHERE slot_id= ?',t).fetchone()
        logger.info("Fetched datetime_in: {}".format(datetime_in))
        if not datetime_in:
            logger.error("Value error raised")
            raise ValueError("slot {} is empty".format(uid))
        return "{}_{}.jpg".format(datetime_in[0], side)


    def insert_to_current(self, s):
        """
        Inserts a slot class object into the table 'current'

        Args: s object of class Slot
        Returns: None
        """
        t = s.get_tuple(False) #returns a tuple of member variables
        self.__c.execute('INSERT INTO current(slot_id, uid, status, datetime_in, ocr_info) VALUES (?, ?, ?, ?, ?)', t)
        self.__conn.commit()


    def delete_from_current(self, s):
        """
        Removes a slot class object from the table 'current'

        Args: s obj of class Slot
        Returns None
        """
        t = (s.slot_id, )
        self.__c.execute('DELETE FROM current WHERE slot_id = ? ', t)
        self.__conn.commit()


    def get_empty_slot(self):
        """
        Returns the first free slot availble

        Args: None
        Returns: int
        """
        empty_slot = self.__c.execute('SELECT slot_id FROM current WHERE status = 0 ORDER BY slot_id LIMIT 1')
        return empty_slot.fetchall()[0][0]

    def insert_to_records(self, s):
        """
        Inserts a slot class object into the table 'records'

        Args: s object of class Slot
        Returns: None
        """
        s.set_datetime_out()
        t = s.get_tuple(to_records=True)
        self.__c.execute('INSERT INTO records(uid, datetime_in, datetime_out, ocr_info) VALUES (?, ?, ?, ?)', t)
        self.__conn.commit()

    def insert_mobile_to_records(self, uid, mob):
        """
        Inserts mobile number to records table.
        """
        logger.info("Called insert_mobile_to_records()...")
        self.__c.execute('''UPDATE records
                            SET mobile_num = ?
                            WHERE uid = ?''',(mob,uid,))
        logger.info("Mobile number added to records.")
        self.__conn.commit()


    def insert_to_ocr_table(self, o):
        """
        """
        self.uid = o[0]
        self.name = o[1]
        #self.dob = o[2]

        # converting DOB in the form -- 01-Jan-2000
        try:
            DOB = o[2]
            month_dict = {'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May', '06':'Jun', '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}
            month = month_dict[DOB[3:5]]
            self.dob = DOB[0:2] + "-" + month + "-" + DOB[6:]
        except:
            self.dob = o[2]

        self.id = o[3]
        self.company = o[4]
        self.validity = o[5]

        self.__c.execute('INSERT INTO ocr_table(uid, name, dob, id, company, validity) VALUES (?, ?, ?, ?, ?, ?)', (self.uid, self.name, self.dob, self.id, self.company, self.validity))
        self.__conn.commit()


    def update_rec_datetimeout(self, date_out, UID):
        """
        Updates the date-time out on retrieval
        """
        self.__c.execute('''UPDATE records
                            SET datetime_out = ?
                            WHERE uid = ?''',(date_out,UID,))
        self.__conn.commit()


    def return_date_out(self, UID):
        """
        Returns date-time-out of the given UID.
        """
        date_time_out = self.__c.execute('SELECT datetime_out FROM records WHERE uid = ?', (UID,)).fetchone()
        return date_time_out[0]


    def update_current(self, s):
        """
        Updates current table with new members of slot

        Args: s object of class Slot
        Returns: None
        """
        self.__c.execute('''UPDATE current
                            SET status=?, uid=?, datetime_in=?, ocr_info=?
                            WHERE slot_id = ?''',(s.status, s.uid, s.datetime_in, s.ocr_info, s.slot_id))
        self.__conn.commit()


    def __del__(self):
        """
        """
        self.__conn.close();


    def close(self):
        """
        """
        self.__conn.close();


    def get_all_curr_users(self):
        """
        Returns currently stored slot_id and uid.
        """
        current_users = self.__c.execute('SELECT uid,datetime_in FROM current WHERE uid != "" ORDER BY datetime_in DESC')
        d = {}
        for uid,date_in in current_users.fetchall():
            name = self.__c.execute('SELECT name FROM ocr_table WHERE uid = ?', (uid,)).fetchone()[0]
            formatted_date_in = date_in[0:4]+"/"+date_in[4:6]+"/"+date_in[6:8]+" at "+date_in[8:10]+":"+date_in[10:12]
            d[uid] = name+";"+formatted_date_in
        return d


    def check_date_in_current(self, date):
        """
        """
        current_date_in = self.__c.execute('SELECT datetime_in FROM current')
        for j in current_date_in.fetchall():
            if j[0]==date:
                formatted_date_out = "Still in storage"
                break
            else:
                date_out = self.__c.execute('SELECT datetime_out FROM records WHERE datetime_in = ?', (date,)).fetchone()[0]
                formatted_date_out = date_out[0:4]+"/"+date_out[4:6]+"/"+date_out[6:8]+" at "+date_out[8:10]+":"+date_out[10:12]
        return formatted_date_out


    def list_all_users_by_date(self, date):
        """
        Method to list user data by date.
        Params : date
        Returns : {name : {uid : date_out}}
        """
        user_data = {}
        key_data = {}
        date_in = self.__c.execute('SELECT datetime_in FROM records ORDER BY datetime_in DESC')
        for i in date_in.fetchall():
            formatted_date = (i[0])[0:8]
            if formatted_date==date:
                formatted_date_in = i[0][0:4]+"/"+i[0][4:6]+"/"+i[0][6:8]+" at "+i[0][8:10]+":"+i[0][10:12]
                uid = self.__c.execute('SELECT uid FROM records WHERE datetime_in = ?', (i[0],)).fetchone()[0]
                date_out = self.check_date_in_current(i[0])
                name = self.__c.execute('SELECT name FROM ocr_table WHERE uid = ?', (uid,)).fetchone()[0]
                key_data[uid] = name+";"+formatted_date_in+";"+date_out
        return key_data


    def list_slot_from_name(self, name):
        """
        Lists all UID's with specified name.
        """
        key_list ={}
        uid = self.__c.execute('SELECT uid FROM ocr_table WHERE name = ?', (name,))
        for i in uid.fetchall():
            date_in = self.__c.execute('SELECT datetime_in FROM records WHERE uid = ?', (i[0],)).fetchone()[0]
            formatted_date_in = date_in[0:4]+"/"+date_in[4:6]+"/"+date_in[6:8]+" at "+date_in[8:10]+":"+date_in[10:12]
            date_out = self.check_date_in_current(date_in)
            key_list[i[0]] = formatted_date_in+";"+date_out
        return key_list


    def list_slot_from_mobile(self, mob):
        """
        Lists all transactions with specified mobile number.
        """
        key_list ={}
        uid = self.__c.execute('SELECT uid FROM records WHERE mobile_num = ?', (mob,))
        for i in uid.fetchall():
            date_in = self.__c.execute('SELECT datetime_in FROM records WHERE uid = ?', (i[0],)).fetchone()[0]
            formatted_date_in = date_in[0:4]+"/"+date_in[4:6]+"/"+date_in[6:8]+" at "+date_in[8:10]+":"+date_in[10:12]
            date_out = self.check_date_in_current(date_in)
            key_list[i[0]] = formatted_date_in+";"+date_out
        return key_list


#    def eject_by_mobile_number(self, mob):
#        """
#        Eject card with specified mobile number.
#        """
#        uid = self.__c.execute('SELECT uid FROM records WHERE mobile_num = ?', (mob,)).fetchone()[0]
#        return uid


    def list_all_users_between_dates(self, date1, date2):
        """
        Method to list user datas b/w supplied dates.
        Params : date
        Returns : {uid : name;dob;id;company;validity;date_in;date_out;}
        """
        key_data = {}
        date_in = self.__c.execute('SELECT datetime_in FROM records ORDER BY datetime_in DESC')
        for i in date_in.fetchall():
            formatted_date = (i[0])[0:8]
            if (date1<=formatted_date and date2>=formatted_date):
                uid = self.__c.execute('SELECT uid FROM records WHERE datetime_in = ?', (i[0],)).fetchone()[0]
                name = self.__c.execute('SELECT name FROM ocr_table WHERE uid = ?', (uid,)).fetchone()[0]
                dob = self.__c.execute('SELECT dob FROM ocr_table WHERE uid = ?', (uid,)).fetchone()[0]
                id = self.__c.execute('SELECT id FROM ocr_table WHERE uid = ?', (uid,)).fetchone()[0]
                company = self.__c.execute('SELECT company FROM ocr_table WHERE uid = ?', (uid,)).fetchone()[0]
                validity = self.__c.execute('SELECT validity FROM ocr_table WHERE uid = ?', (uid,)).fetchone()[0]
                date_in = self.__c.execute('SELECT datetime_in FROM records WHERE datetime_in = ?', (i[0],)).fetchone()[0]
                formatted_date_in = date_in[0:4]+"/"+date_in[4:6]+"/"+date_in[6:8]+" at "+date_in[8:10]+":"+date_in[10:12]
                date_out = self.check_date_in_current(i[0])
                key_data[uid] = name+";"+dob+";"+id+";"+company+";"+validity+";"+formatted_date_in+";"+date_out
        return key_data


    def short_list__users_between_dates(self, date1, date2):
        """
        Method to show a short list of user datas b/w supplied dates.
        Params : date
        Returns : {uid : name;date_in;date_out;}
        """
        user_data = {}
        date_in = self.__c.execute('SELECT datetime_in FROM records ORDER BY datetime_in DESC')
        for i in date_in.fetchall():
            formatted_date = (i[0])[0:8]
            if (date1<=formatted_date and date2>=formatted_date):
                uid = self.__c.execute('SELECT uid FROM records WHERE datetime_in = ?', (i[0],)).fetchone()[0]
                name = self.__c.execute('SELECT name FROM ocr_table WHERE uid = ?', (uid,)).fetchone()[0]
                date_in = self.__c.execute('SELECT datetime_in FROM records WHERE datetime_in = ?', (i[0],)).fetchone()[0]
                formatted_date_in = date_in[0:4]+"/"+date_in[4:6]+"/"+date_in[6:8]+" at "+date_in[8:10]+":"+date_in[10:12]
                date_out = self.check_date_in_current(i[0])
                user_data[uid] = name+";"+formatted_date_in+";"+date_out
        return user_data


    def send_first_last_date(self):
        """
        Method to send first and last dates from stored date & time.
        """
        date_val = {}
        first_date = self.__c.execute('SELECT MIN(datetime_in) FROM records').fetchone()[0]
        last_date = self.__c.execute('SELECT MAX(datetime_in) FROM records').fetchone()[0]
        date_val[first_date] = last_date
        return date_val


    def create_report(self, date1, date2):
        """
        Method to create report for given list.
        """
        data = self.list_all_users_between_dates(date1, date2)
        formatted_date1 = date1[0:4]+"/"+date1[4:6]+"/"+date1[6:8]
        formatted_date2 = date2[0:4]+"/"+date2[4:6]+"/"+date2[6:8]
        with open('asrs_report.txt', 'w') as f:
            f.write('\nFrom : {}  To : {}\n'.format(formatted_date1, formatted_date2))
            f.write("-------------------------------------------------------------------------------------------\n")
            f.write("-------------------------------------------------------------------------------------------\n\n")
            for key, value in data.items():
                x = value.split(';')
                f.write('\n\n\n\nTID         : %s\n\nNAME        : %s\nDOB         : %s\nID          : %s\nCOMPANY     : %s\nVALIDITY    : %s\nSTORED DATE : %s  |  RETRIEVED DATE : %s \n\n' % (key, x[0], x[1], x[2], x[3], x[4], x[5], x[6]))
                f.write("-------------------------------------------------------------------------------------------\n\n")

        os.system('enscript -b "ASRS REPORT" -G -p output.ps asrs_report.txt')
        os.system('ps2pdf output.ps asrs_report.pdf')


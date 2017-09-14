import yaml
import json
import sql
import psycopg2
import time
import pprint


# # connect to database makerspace
# conn = psycopg2.connect("host=localhost dbname=makerspace user=postgres")
# # open a cursor to perform database operations
# cur = conn.cursor()

# sdb = StudentDatabase( "host", "db_name", "user", "pass" )
# sdb.add_user( "cardID", "ID", "netID", "Name", "Lastname", "oldid" )


class StudentDatabase:
    def __init__(self, host, db_name, user, password, port):
        # TODO: add password field to connection after successful database connection
        self.host = host
        self.db_name = db_name
        self.user = user
        self.password = password
        self.port = port

        try:
            # connect to database makerspace
            #TODO: add password field
            self.conn = psycopg2.connect("host={} dbname={} user={} port={}".format(self.host, self.db_name, self.user, self.port))
            # open a cursor to perform database operations
        except:
            print("I am unable to connect to the database. \n Please supply parameters in this format: StudentDatabase.StudentDatabase(self, host, db_name, user, password)")

    def __dbReq(self, stringReq):
        """
        Handles creating a cursor, making a request, and closing said cursor.
        """
        # TODO: Add exception handling, do some logging
        try:
            cur = self.conn.cursor()
            print("Request made!")
            result = cur.execute(stringReq)
            self.conn.commit()
            cur.close()
            return result
        except Exception as e:
            print(e)

    def get_init(self):
        return "{} {} {} {}".format(self.host, self.db_name, self.password, self.user)

    def user_exists(self, card_id, uw_id, uw_netid):
        # cur = self.conn.cursor()
        user_exists = self.__dbReq('SELECT * FROM users WHERE card_id=\'{}\' OR uw_id=\'{}\' OR uw_netid=\'{}\''.format(str(card_id), str(uw_id), str(uw_netid)))
        return user_exists is not None # if true then user exists

        #user_exists = cur.description[0][2]

    def add_user(self, card_id, uw_id, uw_netid, first_name, last_name):
        # searches table for existing users with any matching unique inputs, i.e. duplicates
        try:
            if not self.user_exists(card_id, uw_id, uw_netid):  # user does not exist
                print("didn't find user in database! now inserting user into database")
                request = "INSERT INTO users (card_id, uw_id, uw_netid, first_name, last_name) VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\'".format(str(card_id), str(uw_id), str(uw_netid), str(first_name), str(last_name))
                self.__dbReq(request)
        except Exception as e:
            print(e)

    # removing user from form input
    def remove_user(self, card_id, uw_id, uw_netid):
        # searches for user with a matching input
        self.__dbReq("SELECT * FROM users WHERE card_id=%(card_id)s OR uw_id=%(uw_id)s OR uw_netid=%(uw_netid)s") % {'card_id': str(card_id), 'uw_id': str(uw_id), 'uw_netid': str(uw_netid)}
        # if a user is found, remove from table
        if len(cur.fetchall()) == 1:
            self.__dbReq("DELETE FROM users")
            # move deleted user to new table?
        # error, no user found matching inputs
        else:
            pass
    # editing user entry by form input
    def edit_user(self, old_uw_id, card_id, uw_id, uw_netid, first_name, last_name):
        # gets id of user entry matching
        self.__dbReq("SELECT id FROM users WHERE uw_id=%(uw_id)s") % {'uw_id': str(old_uw_id)}
        # if id is found update user entry
        if len(cur.fetchall()) == 1:
            id = cur.fetchall()[0]
            self.__dbReq("UPDATE users SET card_id=%(card_id)s, uw_id=%(uw_id)s, uw_netid=%(uw_netid)s, first_name=%(first_name)s, last_name=%(last_name)s WHERE id=%(id)s") % {'card_id': str(card_id), 'uw_id': str(uw_id), 'uw_netid': str(uw_netid), 'first_name': str(firstname), 'last_name': str(last_name), 'id': str(id)}
        # error, no id found so no update
        else:
            pass

    # display all users
    def display_users():
        table = "<table>"
        self.__dbReq("SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='users'")
        header = cur.fetchall()
        for column in header:
            table += "<th>" + str(column[3]) + "</th>"
        self.__dbReq("SELECT * FROM users")
        data = cur.fetchall()
        for row in data:
            table += "<tr>"
            for column in row:
                table += "<td>" + str(column) + "</td>"
            table += "</tr>"
        return table + "</table>"

    def display_all_users(self):
        self.__dbReq("SELECT * FROM users;")

    # add membership to uw_id given card_id and type of membership
    # expiration_date is only required if it is a main_door membership
    def add_membership(card_id, type, expiration_date):
        pass

    # display all memberships and allow removing one by selecting one
    def remove_membership(card_id, type, expiration_date):
        pass

    # edit details of a membership
    def edit_membership(card_id, type, expiration_date):
        pass

    # ban membership of uw_id given card_id and type of membership
    # start_date is from time of form submission and end_date set by submitter
    def ban_card(card_id, type, start_date, end_date):
        pass

    # display list of all bans and allow unbanning by selecting one
    def unban_card(card_id, type, start_date, end_date):
        pass

    def add_card_reader():
        pass

    def edit_card_reader():
        pass

    def remove_card_reader():
        pass

    def add_equipment_groups():
        pass

    def edit_equipment_groups():
        pass

    def remove_equipment_groups():
        pass

    # writes to table card_activity
    def write_card_activity(self, uw_id, type, date):
    #def write_card_activity(uw_id, type, date, pass='0'): doesn't work for Cody & Chuan
        pass

    # optional: show which equipment types a user is trained on
    def show_trained_equipment(uw_id):
        pass

    # optional: show all users trained on an equipment type
    def show_trained_users(type):
        pass

#
#
# class Members():
#     def __init__ (self, card_id, type, expiration_date, start_date, end_date, date):
#         self.card_id = card_id
#         self.type = type
#         self.expiration_date = expiration_date
#         self.start_date = start_date
#         self.end_date = end_date
#         self.date = date
#
#
#     # checks card number for bans then for membership then if membership is expired
#     def card_swipe(card_id, card_reader):
#         # given card_reader id get equipment type from card_readers table
#         self.__dbReq("SELECT type FROM card_readers WHERE id=%(card_reader)s", {'card_reader': card_reader})
#         if cur.rowcount > 0:
#             type = cur.fetchall()[0][0]
#             # given user's card_id get user's uw_id from users table
#             self.__dbReq("SELECT uw_id FROM users WHERE card_id=%(card_id)s", {'card_id': card_id})
#             if cur.rowcount > 0:
#                 uw_id = cur.fetchall()[0][0]
#                 # search memberships table for uw_id and equipment type and if found return expiration_date
#                 self.__dbReq("SELECT expiration_date FROM memberships WHERE uw_id=%(uw_id)s AND type=%(type)s ORDER BY expiration_date DESC", {'uw_id': uw_id, 'type': type})
#                 if cur.rowcount > 0:
#                     expiration_date = cur.fetchall()[0][0]
#                     if expiration_date > time.time():
#                         return 'GJ YOU IN'
#                         # call write_card_activity()
#         else:
#             return 'U FAILED'


student = StudentDatabase("localhost", "postgres", "postgres", "1234", "2345")
print(student.user_exists("16808028", "16808028", "16808028"))
# student.add_user("1234", "1234", "431")

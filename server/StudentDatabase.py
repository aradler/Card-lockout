import yaml
import json
import sql
import psycopg2
import time
import datetime
import pprint


# # connect to database makerspace
# conn = psycopg2.connect("host=localhost dbname=makerspace user=postgres")
# # open a cursor to perform database operations
# cur = conn.cursor()

# sdb = StudentDatabase( "host", "db_name", "user", "pass" )
# sdb.add_user( "cardID", "ID", "netID", "Name", "Lastname", "oldid" )


class StudentDatabase:
    def __init__(self, host, db_name, user, password, port=5432):
        # TODO: add password field to connection after successful database connection
        self.host = host
        self.db_name = db_name
        self.user = user
        self.password = password
        self.port = port

        try:
            # TODO: add password field
            # connect to database makerspace
            self.conn = psycopg2.connect("host={} dbname={} user={} port={}".format(self.host, self.db_name, self.user, self.port))
            # open a cursor to perform database operations
        except:
            print("ERROR: I am unable to connect to the database. \n Please supply parameters in this format: StudentDatabase.StudentDatabase(self, host, db_name, user, password)")

    def __dbReq(self, stringReq):
        """
        Handles creating a cursor, making a request, and closing said cursor.
        """
        # TODO: Add exception handling, do some logging
        try:
            cur = self.conn.cursor()
            cur.execute(stringReq)
            try:
                result = cur.fetchall()  # if not a fetch operation, this will fail.
                print("results fetched!")
            except:
                result = None
                pass
            self.conn.commit()
            print("Request made!")
            cur.close()
            return result
        except Exception as e:
            print(e)

    def get_init(self):
        return "Parameters for database connection are: host={} db_name={} password={} user={} port={}".format(self.host, self.db_name, self.password, self.user, self.port)

    def user_exists(self, card_id, uw_id, uw_netid):
        user_exists = self.__dbReq('SELECT * FROM users WHERE card_id=\'{}\' OR uw_id=\'{}\' OR uw_netid=\'{}\''.format(str(card_id), str(uw_id), str(uw_netid)))
        print(user_exists)
        return bool(user_exists)  # if true then user exists

    def add_user(self, card_id, uw_id, uw_netid, first_name, last_name):
        # searches table for existing users with any matching unique inputs, i.e. duplicates
        try:
            if not self.user_exists(card_id, uw_id, uw_netid):  # user does not exist
                print("didn't find user in database! now inserting user into database")
                request = "INSERT INTO users (card_id, uw_id, uw_netid, first_name, last_name) VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\')".format(str(card_id), str(uw_id), str(uw_netid), str(first_name), str(last_name))
                self.__dbReq(request)
                return True
            else:
                print("user already exists!")
                return False
        except Exception as e:
            print(e)

    # removing user from form input
    def remove_user(self, card_id, uw_id, uw_netid):
        # if a user is found, remove them from the users table
        if self.user_exists(card_id, uw_id, uw_netid):  # user exists
            # TODO: move deleted user to new table?
            print("found user in database! now deleting user from database...")
            # TODO: decide if we need this to be an OR or an AND
            self.__dbReq("DELETE FROM users WHERE card_id=\'{}\' OR uw_id=\'{}\' OR uw_netid=\'{}\'".format(str(card_id), str(uw_id), str(uw_netid)))
            return True
        # error, no user found matching inputs
        else:
            print("didn\'t find user in database!")
            return False

    # editing user entry by form input
    def edit_user(self, id, card_id, uw_id, uw_netid, first_name, last_name):
        # if id is found update user entry exactly
        if self.user_exists(card_id, uw_id, uw_netid):  # user exists
            self.__dbReq("UPDATE users SET card_id=\'{}\', uw_id=\'{}\', uw_netid=\'{}\', first_name=\'{}\', last_name=\'{}\' WHERE id=\'{}\'".format(str(card_id), str(uw_id), str(uw_netid), str(first_name), str(last_name)))
            return True
        # error, no id found so no update
        else:
            print("error, no id found so no update")
            return False

    def display_all_users(self):
        return self.__dbReq("SELECT * FROM users;")

    def display_user_no_html(self, id=None, card_id=None, uw_id=None, uw_netid=None, first_name=None, last_name=None)

    # display all users
    # TODO: is this currently necessary? What will it provide us?
    def display_users(self):
        table = "<table>"
        self.__dbReq("SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=\'users\'")
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

    def membership_exists(self, card_id):
        membership_exists = self.__dbReq("SELECT * FROM memberships WHERE card_id=\'{}\'".format(str(card_id))
        print(membership_exists)
        return bool(membership_exists)  # if true then membership exists

    # add membership to uw_id given card_id and type of membership
    # expiration_date is only required if it is a main_door membership
    def add_membership(self, card_id, type, expiration_date):
        # searches table for existing memberships with any matching unique inputs, i.e. duplicates
        try:
            if not self.membership_exists(card_id):  # membership does not exist
                print("didn't find membership in database! now inserting membership into database")
                join_date = datetime.date.today()
                print(join_date)
                request = "INSERT INTO memberships (card_id, type, join_date, expiration_date) VALUES(\'{}\', \'{}\', \'{}\', \'{}\')".format(str(card_id), str(type), str(join_date), str(expiration_date))
                self.__dbReq(request)
                return True
            else:
                print("membership already exists!")
                return False
        except Exception as e:
            print(e)

    # display all memberships and allow removing one by selecting one
    def remove_membership(self, card_id, type, expiration_date):
        pass

    # edit details of a membership
    def edit_membership(self, card_id, type, expiration_date):
        pass

    # ban membership of uw_id given card_id and type of membership
    # start_date is from time of form submission and end_date set by submitter
    def ban_card(self, card_id, type, start_date, end_date):
        pass

    # # display list of all bans and allow unbanning by selecting one
    # def unban_card(self, card_id, type, start_date, end_date):
    #     pass
    #
    # def add_card_reader(self):
    #     pass
    #
    # def edit_card_reader(self):
    #     pass
    #
    # def remove_card_reader(self):
    #     pass
    #
    # def add_equipment_groups(self):
    #     pass
    #
    # def edit_equipment_groups(self):
    #     pass
    #
    # def remove_equipment_groups(self):
    #     pass
    #
    # # writes to table card_activity
    # def write_card_activity(self, uw_id, type, date):
    # # def write_card_activity(uw_id, type, date, pass='0'): doesn't work for Cody & Chuan
    #     pass
    #
    # # optional: show which equipment types a user is trained on
    # def show_trained_equipment(uw_id):
    #     pass
    #
    # # optional: show all users trained on an equipment type
    # def show_trained_users(type):
    #     pass

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
    def test_users_table(self, card_id, uw_id, uw_netid, first_name, last_name):
        print("****USER EXISTS?****")
        print(student.user_exists(card_id, uw_id, uw_netid))  # check if student exists
        print("****ADDING USER****")
        student.add_user(card_id, uw_id, uw_netid, first_name, last_name)
        print("****REMOVING USER****")
        student.remove_user("1234512341", "1234512341", "1234512341")

    def test_memberships_table(self, card_id, uw_id, uw_netid, first_name, last_name):
        print("****USER EXISTS?****")
        print(student.user_exists(card_id, uw_id, uw_netid))  # check if student exists
        print("****ADDING USER****")
        student.add_user(card_id, uw_id, uw_netid, first_name, last_name)
        print("****REMOVING USER****")
        student.remove_user("1234512341", "1234512341", "1234512341")

# pprint.pprint(student.display_all_users())


student = StudentDatabase("localhost", "postgres", "postgres", "1234")

# Testing for test_users_table
# print("****INITIALIZATION****")
# print(student.get_init())
# student.test_users_table("1234512341", "1234512341", "1234512341", "aaron test", "aaron test 2")

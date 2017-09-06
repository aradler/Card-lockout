import psycopg2, pprint, random
from itertools import permutations


# Connect to an existing database
try:
    conn = psycopg2.connect("dbname='codes' user='codes' host='localhost' port=2345")
except:
    print "I am unable to connect to the database"


def get_all_info_from_id(id_number):
   """
   Takes an id number as an input, and returns all the information for that id number from the database
   """
   cur = conn.cursor()
   cur.execute("SELECT data -> \'" + str(id_number) + "\' FROM equip_auth")
   rows = cur.fetchall()
   conn.commit()
   i = 0 #use this to increment
   for row in rows:
     if rows[i][0] is not None:
         print(rows[i])
   i = i + 1

def did_receive_orientation(id_number):
    """
    Checks if ID received orientation and returns true/false
    """
    cur = conn.cursor()
    cur.execute("SELECT data -> \'" + str(id_number) + "\' ->> 'is_oriented' as authorized_true_false FROM equip_auth;")
    rows = cur.fetchall()
    i = 0
    for row in rows:
        if rows[i][0] == 'true':
            is_oriented = True
            return is_oriented # if the row we're looking for is true, then the student is oriented
        i = i + 1
    conn.commit()

def get_if_authorized_for_equipment_name(id_number, equip_name):
    """
    Allow you to determine if ID number is authorized by first looking up the ID in the DB. Then we'll check to ensure that the ID has received orientation. If ID has recieved orientation, then we'll check if they're authorized to use said equipment
    """
    ## TODO: remove all whitespaces and replace with underscores (if we really need to)
    if did_receive_orientation(id_number):
       cur = conn.cursor()
       cur.execute("SELECT data -> \'" + str(id_number) + "\'->> \'"+ equip_name +"\' as authorized_true_false FROM equip_auth;")
       rows = cur.fetchall()
       print(rows[-1])
    else:
        print("not oriented")
    conn.commit()

def insert_random_entry(id_number):
    """
    Generates and inserts a random entry using the random function, and ensures that if the is_oriented is false that everything else is also false. Takes an ID number as input
    """
    _is_oriented = bool(random.getrandbits(1)) 
    if _is_oriented:
        _is_oriented = "true"
        _cnc_mill = generate_db_true_false()
        _laser_cutter = generate_db_true_false()
        _3d_printer = generate_db_true_false()
        _drill_press = generate_db_true_false()
    else:
        _is_oriented = "false"
        _cnc_mill = "false"
        _laser_cutter = "false"
        _3d_printer = "false"
        _drill_press = "false"


    cur = conn.cursor()
    cur.execute("""
    INSERT into equip_auth (data) values (
    \'{
    """ + "\"" + str(id_number) + "\"" + """ : {
    \"is_oriented\" : """ + _is_oriented + """,
    \"3d_printer\" : """ + _3d_printer + """,
    \"cnc_mill\" : """ + _cnc_mill + """,
    \"laser_cutter\" : """ + _laser_cutter + """
    }
   }
  \'::jsonb);""")

    #commented out to save resources
    #print("""
    #INSERT into equip_auth (data) values (
    #\'{
    #""" + "\"" + str(id_number) + "\"" + """ : {
    #\"is_oriented\" : """ + _is_oriented + """,
    #\"3d_printer\" : """ + _3d_printer + """,
    #\"cnc_mill\" : """ + _cnc_mill + """,
    #\"laser_cutter\" : """ + _laser_cutter + """
    #}
  # }
 # \'#::jsonb);""")
    conn.commit()

def generate_db_true_false():
    """
    Used to correctly enter booleans into the postgresql database
    """
    boolean = bool(random.getrandbits(1))
    if boolean:
        return "true"
    else:
        return "false"

def insert_data(id_number, equip_name):
    """
    Used to insert data into database
    """
    #TODO: Finish this.
    cur = conn.cursor()
    cur.execute("insert into jsonData (data) values (\'" + id_number + "\')")
    conn.commit()

def insert_test_permutations_data():
    """
    Used to test inserting records into the database
    """
    permutations_list = generate_permutations_list() #generate 8! (40,320) permutations to test with database
    for item in permutations_list:
        insert_random_entry(reduce(lambda rst, d: rst * 10 + d, item)) #puts tuple as concated ints
    conn.commit()

def retrieve_test_permutations_data():
    """
    Uses random library and and list of permutations  to test database entries
    """
    permutations_list = generate_permutations_list()
    id_number = random.choice(permutations_list)
    concat_id_number = reduce(lambda rst, d: rst * 10 + d, id_number)
    get_all_id_info(concat_id_number)
    print(concat_id_number)

def generate_permutations_list():
    """
    Generates a list of permutations based on the range input
    """

    return list(permutations(range(1, 9)))


def main():
    print("""
    Functions that you can use:
    
    Retrieval operations:

    get_all_info_from_id(id_number)
    get_if_authorized_for_equipment_name(id_number, equip_name)
    did_receive_orientation(id_number)

    Insertion operations:

    insert_random_entry(id_number)
    insert_data(id_number, equip_name) ***NEEDS TO BE COMPLETED

    Testing:

    insert_test_permutations_data()
    retrieve_test_permutations_data()
    """)



main()

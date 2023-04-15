"""
    CREATED BY @VIKAS
"""
import sqlite3
import constants

session = {}

def login_validatlilon(eml, pwd):
    email = eml
    password = pwd
    try:
        conn = sqlite3.connect(constants.DB_USER_PATH)
        print("success")
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM user WHERE email = '{}' AND password = '{}'""".format(email, password))
        users = cursor.fetchall()
        print(users)

        conn.commit()
        conn.close()
        session['user_email'] = users[0][1]
        print(session)

        if len(users) == 1:
            print("successfully implemented login_validation function")
            return users
        else:
            print("successfully implemented login_validation function")
            return 0
    except:
        print("error occurred in login_validation function")


def uniq_email(eml):
    email_unq = eml

    try:
        conn = sqlite3.connect(constants.DB_USER_PATH)
        print("succes")
        cursor1 = conn.cursor()
        cursor1.execute("""SELECT * FROM user WHERE email = '{}'""".format(email_unq))
        users = cursor1.fetchall()

        conn.commit()
        conn.close()

        if len(users) == 1:
            print('match found')
            print("successfully implemented uniq_email function")
            return 1
        else:
            print("successfully implemented uniq_email function")
            print('no match found')
            return 0
    except:
        print("error occurred in uniq_email function")


def register_user(users_name, eml, pwd):
    email = eml
    password = pwd
    name = users_name

    try:
        conn = sqlite3.connect(constants.DB_USER_PATH)
        print("success")
        cursor2 = conn.cursor()
        cursor2.execute(
            """INSERT INTO user (name,email,password)VALUES( '{}','{}','{}')""".format(name, email, password))
        print("user added successful")

        conn.commit()
        conn.close()
        print("successfully implemented register_user function")
    except:
        print("error occurred in register_user")


def savei(email, filename, filepath, lat, lon, num_pot):
    my_email = email
    my_filename = filename
    my_filepath = filepath
    my_lat = lat
    my_lon = lon
    num_pothole = num_pot

    try:
        conn4 = sqlite3.connect(constants.DB_USER_PATH)
        cursor4 = conn4.cursor()
        cursor4.execute(
            """INSERT INTO image(email,filename,filepath,lat,lon,count)VALUES('{}','{}','{}',{},{},{})""".format(
                my_email, my_filename, my_filepath, my_lat, my_lon, num_pothole))

        print("pothole data stored successfully")
        conn4.commit()
        conn4.close()
        print("successfully implemented savei function")

    except:
        print("error occurred in savei method")


def admshow():
    try:
        conn5 = sqlite3.connect(constants.DB_USER_PATH)
        cursor5 = conn5.cursor()
        cursor5.execute("""SELECT email,lat,lon,count FROM image""")
        users_image = cursor5.fetchall()
        conn5.commit()
        conn5.close()
        print("successfully implemented admshow function")
        return users_image
    except:
        print("error occurred in admshow function")
        return None

def view_previous(email):
    email_id = email
    try:
        conn6 = sqlite3.connect(constants.DB_USER_PATH)
        print("succes")
        cursor6 = conn6.cursor()
        cursor6.execute("""SELECT email,lat,lon,count FROM image WHERE email='{}'""".format(email_id))
        users_image = cursor6.fetchall()
        conn6.commit()
        conn6.close()
        print("successfully implemented view_previous function")
        return users_image
    except:
        print("error occurred in view_previous function")

def view_recent(email):
    email_id = email

    try:
        conn9 = sqlite3.connect(constants.DB_USER_PATH)
        print("success")
        cursor9 = conn9.cursor()
        cursor9.execute("""SELECT email,lat,lon,count FROM image WHERE email='{}'""".format(email_id))
        users_image = cursor9.fetchall()
        users_recent = users_image[(len(users_image) - 1)]

        conn9.commit()
        conn9.close()
        print("successfully implemented view_recent function")
        return users_recent
    except:
        print("error occurred in view_recent function")

def user_info_basic(u_email):

    try:
        conn7 = sqlite3.connect(constants.DB_USER_PATH)
        print("success")
        cursor7 = conn7.cursor()
        cursor7.execute("""SELECT name FROM user WHERE email='{}'""".format(u_email))
        users_name = cursor7.fetchall()
        conn7.commit()
        conn7.close()
        print("successfully implemented user_info_basic function")
        return users_name[0][0]

    except:
        print("error occurred in user_info_basic function")

def user_complaint_basic(u_email):

    try:
        conn8 = sqlite3.connect(constants.DB_USER_PATH)
        print("success")
        cursor8 = conn8.cursor()
        cursor8.execute("""SELECT filename FROM image WHERE email='{}'""".format(u_email))
        temp_ar = cursor8.fetchall()
        count = len(temp_ar)
        conn8.commit()
        conn8.close()
        print("successfully implemented user_complaint_basic function")
        return count

    except:
        print("error occurred in user_complaint_basic")

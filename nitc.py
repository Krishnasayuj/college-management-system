import mysql.connector as mysql
db = mysql.connect(host="localhost",user="root",password="",database="nitc")
command_handler=db.cursor(buffered=True)


def student_session(username):
    while 1:
        print("")
        print("1. View Register")
        print("2. Download Register")
        print("3. Logout")

        user_option = input(str("Option : "))
        if user_option == "1":
            print("Displaying register")
            username = (str(username),)
            command_handler.execute("SELECT date, username, status FROM attendance WHERE username = %s",username)
            records = command_handler.fetchall()
            for record in records:
                print(record)
        
        elif user_option== "2":
            print("Downloading register.....")
            username = (str(username),)
            command_handler.execute("SELECT date, username, status FROM attendance WHERE username = %s",username)
            records = command_handler.fetchall()
            for record in records:
                with open("C:/Users/ACER/Desktop/COLLEGE MANAGEMENT SYSTEM/register.txt", "w") as f:
                    f.write(str(records)+"\n")
                f.close()
            print("All records saved")
        elif user_option=="3":
            break
        else:
            print("Invalid option")


def admin_session():
    while 1:
        print("")
        print("Admin Menu")
        print("1. Register new Student")
        print("2. Register new Teacher")
        print("3. Delete existing Student")
        print("4. Delete existing Teacher")
        print("5. Logout")

        user_option = input(str("Option : "))
        if user_option == "1":
            print("")
            print("Register new student")
            username = input(str("Student username: "))
            password = input(str("Student passowrd: "))
            query_vals  = (username,password)
            command_handler.execute("INSERT INTO user(username,password,designation) VALUES(%s,%s,'student')",query_vals)
            db.commit()
            print(username + " has been registered as a student")
        elif user_option =="2":
            print("")
            print("Register new teacher")
            username = input(str("Teacher username: "))
            password = input(str("Teacher passowrd: "))
            query_vals  = (username,password)
            command_handler.execute("INSERT INTO user(username,password,designation) VALUES(%s,%s,'Teacher')",query_vals)
            db.commit()
            print(username + " has been registered as a Teacher")
        elif user_option=="3":
            print("")
            print("Delete Existing Student Account")
            username=input(str("Student username : "))
            query_vals=(username,"student")
            command_handler.execute("DELETE FROM user WHERE username = %s AND designation = %s",query_vals)
            db.commit()
            if command_handler.rowcount < 1:
                print("User not found")
            else:
                print(username + " has been deleted")

        elif user_option=="4":
            print("")
            print("Delete Existing Teacher Account")
            username=input(str("Teacher username : "))
            query_vals=(username,"teacher")
            command_handler.execute("DELETE FROM user WHERE username = %s AND designation = %s",query_vals)
            db.commit()
            if command_handler.rowcount < 1:
                print("User not found")
            else:
                print(username + " has been deleted")
        elif user_option=="5":
            break
        else:
            print("No valid options selected")




        #user_option = input(str)
def teacher_session():
    while 1:
        print("")
        print("Teacher's Menu")
        print("1. Mark student register")
        print("2. View register")
        print("3. Logout")
        
        user_option = input(str("Option : "))
        if user_option == "1":
            print("")
            print("Mark student register")
            command_handler.execute("SELECT username FROM user WHERE designation = 'student'")
            records = command_handler.fetchall()
            date = input(str("Date : DD/MM/YYYY "))
            for record in records:
                #record is here returned as a tuple and we are returning only name and no0 other data, hence this is required to strip it down
                record = str(record).replace("'","")
                record = str(record).replace(",","")
                record = str(record).replace("(","")
                record = str(record).replace(")","")
                #PRESENT | ABSENT | LATE
                status = input(str("Status for " + str(record) + "P/A/L : "))
                query_vals = (str(record),date,status)
                command_handler.execute("INSERT INTO attendance (username, date, status) VALUES(%s,%s,%s)",query_vals)
                db.commit()
                print(record + "Marked as " + "" + status)
            
        elif user_option=="2":
            print("")
            print("Viewing all student registers")
            command_handler.execute("SELECT username, date, status FROM attendance")
            records = command_handler.fetchall()
            print("Displaying all registers")
            for record in records:
                print(record)
        elif user_option == "3":
            break
        else:
            print("No valid option was selected")


def auth_student():
    print("")
    print("Student's Login")
    print("")
    username = input(str("Username: "))
    password = input(str("Password: "))
    query_vals = (username, password,"student")
    command_handler.execute("SELECT username FROM user WHERE username = %s AND password = %s AND designation = %s",query_vals)
    if command_handler.rowcount <= 0:
        print("invalid login details")
    else:
        student_session(username)




def auth_teacher():
    print("")
    print("Teacher's Login")
    print("")
    username = input(str("Username : "))
    password = input(str("Password : "))
    query_vals = (username, password)
    command_handler.execute("SELECT * FROM user WHERE username = %s AND password = %s AND designation='teacher'",query_vals)
    if command_handler.rowcount<1:
        print("Login denied")
    else:
        teacher_session()


def auth_admin():
    print("")
    print("Admin login")
    print("")
    username = input(str("Username : "))
    password = input(str("Password : "))
    if username == "admin" and password=="password":
        admin_session()
    else:
        print("Login access denied")


def main():
    while True:
        print("NATIONAL INSTITUITE OF TECHNOLOGY CALICUT")
        print("")
        print("1. Login as student")
        print("2. Login as teacher")
        print("3. Login as admin")

        user_option = input(str("Option : "))
        if user_option == "1":
            auth_student()
        elif user_option=="2":
            auth_teacher()
        elif user_option=="3":
            auth_admin()
        else:
            print("No valid option was selected")

main()
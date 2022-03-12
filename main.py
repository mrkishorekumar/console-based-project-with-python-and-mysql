import mysql.connector as mysql

db = mysql.connect(host="localhost",user="root",passwd="123@mySQL",db="office")

command_handler = db.cursor(buffered=True) #run multiple commands

def student_session(username):
	while 1:
		print()
		print("Login Sucess Welcome Employee")
		print()
		print("1. View Register")
		print("2. Download Register")
		print("3. Logout")

		userchoices = int(input("Option : "))

		if userchoices==1:
			print("Displaying Register")
			username = (str(username),)
			command_handler.execute("SELECT date, username, status FROM attendance WHERE username = %s",username)
			records = command_handler.fetchall()
			for record in records:
				print(record[0],record[1],record[2])

		elif userchoices==2:
			print("Downloadind Register............")
			username = (str(username),)
			command_handler.execute("SELECT date, username, status FROM attendance WHERE username = %s",username)
			records = command_handler.fetchall()
			for record in records:
				with open("Register.txt","w") as f:
					f.write(str(records)+"\n")
				f.close()
			print("All Records are Saved!")

		elif userchoices==3:
			break
		else:
			print("No Valid Option was Selected!")

def auth_employee():
	print()
	print("Login Employee")
	print()

	username = input("Username : ")
	password = input("Password : ")

	query_vals = (username,password,"employee")

	command_handler.execute("SELECT username FROM users WHERE username = %s AND password = %s AND privilege = %s",query_vals)

	if command_handler.rowcount <= 0:
		print("Invaild Login Details")
	else:
		student_session(username)


def hr_manger_session():
	print("Login Sucess Welcome HR Manager")
	
	while 1:
		print()
		print("HR Manager Menu")
		print("1. Mark Employee Register")
		print("2. View Register")
		print("3. Logout")

		userchoices = int(input("Option : "))

		if userchoices==1:
			print()
			print("Mark Employee Register")

			command_handler.execute("SELECT username FROM users WHERE privilege = 'employee'")
			records = command_handler.fetchall()
			date = input("Date : DD/MM/YYYY : ")
			for record in records:
				# return in tuple
				record = str(record).replace("'","")
				record = str(record).replace(",","")
				record = str(record).replace("(","")
				record = str(record).replace(")","")
				# Present | Absent | Late
				status  = input("Status for "+ str(record) + " Present | Absent | Late : ")
				query_vals = (str(record),date,status)

				command_handler.execute("INSERT INTO attendance (username, date, status) VALUES(%s,%s,%s)",query_vals)
				db.commit()
				print(record + " Marked as " + status)

		elif userchoices==2:
			print()
			print("Viewing All Employee Register")
			command_handler.execute("SELECT username, date, status FROM attendance")

			records = command_handler.fetchall()
			print("Displaying all Register")
			for record in records:
				print(record[0],record[1],record[2])

		elif userchoices==3:
			break

		else:
			print("No Valid Option was Selected!")

def admin_session():
	print("Login Sucess Welcome Admin")
	
	while 1:
		print()
		print("Admin Menu")
		print("1. Register New Employee")
		print("2. Register New HR Manager")
		print("3. Delete Existing Employee")
		print("4. Delete Existing HR Manager")
		print("5. Logout")

		userchoices = int(input("Option : "))
		if userchoices==1:
			print()
			print("Register Name Employee")
			username = input("Employee Username : ")
			password = input("Employee Password : ")
			query_vals = (username,password)

			command_handler.execute("INSERT INTO users (username,password,privilege) VALUES (%s,%s,'employee')",query_vals)
			db.commit()
			print(username + " has been Registered as a employee")

		elif userchoices==2:
			print()
			print("Register Name HR Manager")
			username = input("HR Manager Username : ")
			password = input("HR Manager Password : ")
			query_vals = (username,password)

			command_handler.execute("INSERT INTO users (username,password,privilege) VALUES (%s,%s,'hr_manager')",query_vals)
			db.commit()
			print(username + " has been Registered as a HR Manager")

		elif userchoices==3:
			print()
			print("Delete Existing Employee")
			username = input("Employee Username : ")
			query_vals = (username,"employee")

			command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s",query_vals)

			db.commit()
			if command_handler.rowcount < 1:
				print("User Not Found")
				
			else:
				print(username + " has been Deleted")

		elif userchoices==4:
			print()
			print("Delete Existing HR Manager")
			username = input("HR Manager Username : ")
			query_vals = (username,"hr_manager")

			command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s",query_vals)

			db.commit()
			if command_handler.rowcount < 1:
				print("User Not Found")
				
			else:
				print(username + " has been Deleted")

		elif userchoices==5:
			break

		else:
			print("No Valid Option was Selected!")

def auth_admin():
	print()
	print("Admin Login")
	print()
	username = input("Username : ")
	password = input("Password : ")
	if username == "admin":
		if password == "password":
			admin_session()
		else:
			print("Incorrect Password")
	else:
		print("Incorrect Username")

def auth_hr_manger():
	print()
	print("Login Sucess Welcome HR Manager")
	print()

	username = input("Username : ")
	password = input("Password : ")
	query_vals = (username,password)

	command_handler.execute("SELECT * FROM users WHERE username = %s AND password = %s AND privilege = 'hr_manager'",query_vals)
	if command_handler.rowcount <= 0:
		print("Login not Recognized")
		
	else:
		hr_manger_session()


def main():
	while 1: #infite loop
		print()
		print("Welcome to Office Management System")
		print()
		print("1. Login as Employee")
		print("2. Login as HR Manager")
		print("3. Login as Admin")
		print("4. Close Login Port")

		userchoices = int(input("Option : "))
		if userchoices==1:
			auth_employee()
		elif userchoices==2:
			auth_hr_manger()
		elif userchoices==3:
			auth_admin()
		elif userchoices==4:
			break
			db.close()
		else:
			print("No Valid Option was Selected!")

main()

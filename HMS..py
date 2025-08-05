from db import Db
import pandas as pd
import random
import pyttsx3
import time
class HMS:
    def __init__(self, a):
        self.db = a
    def display(self):
        print("..THIS ARE THE ROOMS AVAILABLE IN  THIS HOTEL..")
        time.sleep(2)
        s.say("THIS ARE THE ROOMS AVAILABLE IN  THIS HOTEL")
        s.runAndWait()
        q1 = "SELECT * FROM rooms"
        cursor = self.db.cursor()
        cursor.execute(q1)
        result = cursor.fetchall()
        df = pd.DataFrame({"ROOM_ID":[],"ROOM_TYPE":[],"CHARGE_PER_DAY":[],"TOTAL_ROOMS":[],"AVAILABLE_ROOMS":[]})
        for i in range(len(result)):
            df.loc[i] = result[i]
        print(df)
        
    def Book_room(self, Db):
        print(".. YOU HAVE CHOSEN TO BOOK A ROOM ..")
        s.say("YOU HAVE CHOSEN TO BOOK A ROOM")
        s.runAndWait()
        time.sleep(2)
        print(" PLEASE ENTER YOUR DETAILS SO WE CAN BOOK A ROOM FOR YOU ")
        s.say("PLEASE ENTER YOUR DETAILS SO WE CAN BOOK A ROOM FOR YOU")
        s.runAndWait()
        guest_id = int(input("Enter Guest ID: "))
        name = input("Enter Guest Name: ")
        email = input("Enter Email: ")
        phone = input("Enter Phone Number: ")
        address = input("Enter Address: ")
        id_proof = input("Enter ID Proof (e.g., Aadhar, Passport): ")

        cursor = self.db.cursor()


        # Insert guest into guests table
        q1 = """
            INSERT INTO guests (guest_id, name, email, phone, address, id_proof)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        q2 = (guest_id, name, email, phone, address, id_proof)

        try:
            cursor.execute(q1, q2)
            self.db.commit()
        except Exception as e:
            print("Error inserting guests:", e)
            return
#################
    def Book_Reservation(self, Db):
        print("..YOU HAVE CHOOSEN TO RESERVE A ROOM..")
        s.say("..YOU HAVE CHOOSEN TO RESERVE A ROOM..")
        s.runAndWait()
        guest_id = input("Enter Guest ID: ")
        room_id = input("Enter Room ID: ")
        check_in = input("Enter Check-in Date (YYYY-MM-DD): ")
        check_out = input("Enter Check-out Date (YYYY-MM-DD): ")

        cursor = self.db.cursor()
        q1 = "SELECT TOTAL_ROOMS, AVAILABLE_ROOMS FROM ROOMS WHERE ROOM_ID = %s", (room_id,)
        cursor.execute(q1)
        result = cursor.fetchone()
       ####################

        q2 = """
        INSERT INTO RESERVATIONS (GUEST_ID, ROOM_ID, CHECH_IN, CHECK_OUT)
        VALUES (%s, %s, %s, %s)
      """
        values = (guest_id, room_id, check_in, check_out)

        try:
             cursor.execute(q2, values)
             self.db.commit()

             # After reservation, reduce count_of_rooms by 1 for that room
             q3 = "UPDATE ROOMS SET COUNT_OF_ROOMS = COUNT_OF_ROOMS - 1 WHERE ROOM_ID = %s AND COUNT_OF_ROOMS > 0"
             cursor.execute(q3, (room_id,))
             self.db.commit()

             print(".. YOUR BOOKING IS NOW CONFIRMED ..")
             s.say(".. YOUR BOOKING IS NOW CONFIRMED ..")
             s.runAndWait()
        except Exception as e:
             print("Error booking reservation:", e)
             s.say("Error booking reservation")
             s.runAndWait()
####################
    def view_services(self, a):
        print("..THIS ARE  THE SERVICES WE PROVIDE")
        s.say("..THIS ARE  THE SERVICES WE PROVIDE..")
        s.runAndWait()
        time.sleep(2)
              
        q1 = "SELECT * FROM SERVICES"
        cursor = self.db.cursor()
        cursor.execute(q1)
        result = cursor.fetchall()
        df = pd.DataFrame({"SERVICE_ID":[],"SERVICE_NAME":[],"COST":[]})
        for i in range(len(result)):
            df.loc[i] = result[i]
        print(df)
    def Guests_Service(self, Db):
        s.say("please enter the guest id and service id")
        s.runAndWait()
        guest_id = input("Enter Guest ID: ")
        service_id = input("Enter Service ID: ")

        cursor = self.db.cursor()

        try:
          #  Fetching the service cost from the services table
           cursor.execute("SELECT COST FROM SERVICES WHERE SERVICE_ID = %s", (service_id,))
           service = cursor.fetchone()

           if service is None:
            print("IT SEEMS THAT YOU HAVE CHOOSEN THE WRONG SERVICE ID")
            s.say("IT SEEMS THAT YOU HAVE CHOOSEN THE WRONG SERVICE ID")
            s.runAndWait()
            return

           cost = service[0]

            # Insert this values into GUESTS_SERVICES table
           q1 = "INSERT INTO GUESTS_SERVICES (GUEST_ID, SERVICE_ID, COST) VALUES (%s, %s, %s)"
           values = (guest_id, service_id, cost)
           cursor.execute(q1, values)
           self.db.commit()

           print("SERVICE ADDED SUCCESSFULLY TO YOUR ROOM")
           s.say("SERVICE ADDED SUCCESSFULLY TO YOUR ROOM")
           s.runAndWait()


        except Exception as e:
           print("SORRY WE ARE FACING AN ERROR IN THIS PLEASE CHOOSE AGAIN:", e)
           s.say("SORRY WE ARE FACING AN ERROR IN THIS PLEASE CHOOSE AGAIN")
           s.runAndWait()


   

    def Generate_Bill(self, Db):
        print("..PRINTING THE TOTAL BILL..")
        s.say("..PRINTING THE TOTAL BILL..")
        s.runAndWait()
        guest_id = input("Enter Guest ID: ")
        cursor = self.db.cursor()
        cursor.execute ("SELECT R.ROOM_ID, R.CHARGE_PER_DAY, RES.CHECH_IN, RES.CHECK_OUT FROM RESERVATIONS AS RES JOIN ROOMS AS R ON RES.ROOM_ID = R.ROOM_ID WHERE RES.GUEST_ID = %s", [guest_id])

        room_info = cursor.fetchone()

        if room_info is None:
            print("No reservation found for the given guest ID.")
            s.say("No reservation found for the given guest ID.")
            s.runAndWait()
            return

        room_id, charge_per_day, check_in, check_out = room_info
        days = (check_out - check_in).days
        total_charge = days * charge_per_day

        cursor.execute("SELECT COST FROM GUESTS_SERVICES WHERE GUEST_ID = %s", [guest_id])
        services = cursor.fetchall()
        service_total = sum(s[0] for s in services if s[0] is not None) if services else 0

        total_bill = total_charge + service_total

        print("TOTAL_BILL")
        print(f"Guest_id            : {guest_id}")
        print(f"Room_id             : {room_id}")
        print(f"Charge              : {charge_per_day}")
        print(f"Dayas Stayed        : {days}")
        print(f"Room_Total          : {total_charge}")
        print(f"Service_Total       : {service_total}")
        print(f"Total_Bill          : {total_bill + service_total}")
        
        
        s.say("THIS YOUR TOTAL BILL")
        s.runAndWait()
        cursor.execute("INSERT INTO TOTAL_BILL(GUEST_ID, ROOM_ID, ROOM_TOTAL, SERVICE_TOTAL, TOTAL_BILL) VALUES (%s, %s, %s, %s, %s)", (guest_id, room_id, total_charge, service_total, total_bill))
        self.db.commit()
        
obj = Db()
db_connect = obj.creating_connection()

obj2 = HMS(db_connect)
s = pyttsx3.init()
voices = s.getProperty('voices')
s.setProperty('voice',voices[1].id)

if db_connect is None:
    print("Failed to connect to the database. Please check your credentials or server status.")
    exit()

print("WELCOM TO THE HOTEL SIMBA😊")
s.say("WELCOM TO THE HOTEL SIMBA")
s.runAndWait()
while True:
    print("\n1. View Available Rooms\n2. Book Room\n3. Book_Reservation\n4. View Services \n5. GUESTS SERVICES\n6. Generate Bill\n7. Exit")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        obj2.display()
    

    elif choice == 2:
        obj2.Book_room(Db)

    elif choice == 3:
        obj2.Book_Reservation(Db)

    elif choice == 4:
        obj2.view_services(Db)
   

    elif choice == 5:
        obj2.Guests_Service(Db)

    elif choice == 6:
        obj2.Generate_Bill(Db)
    

    elif choice == 7:
        print("Thank you for using our hotel management system. Have a nice day!😊")
        s.say("Thank you for using our hotel management system. Have a nice day")
        s.runAndWait()
        break
    else:
        print("Invalid choice. Please try again.")
        s.say("Invalid choice. Please try again")
        s.runAndWait()
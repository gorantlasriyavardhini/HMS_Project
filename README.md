# HMS_Project
#  Hospitality Management System (HMS)

The **Hospitality Management System (HMS)** is a command-line-based hotel management project developed using **Python** and **MySQL**. It is designed to automate and manage hotel operations such as room bookings, guest check-ins, assigning services (like meals, laundry, spa), and final bill generation.

This system can help hotel staff reduce manual paperwork and keep track of all operations efficiently using a structured relational database.

## Project Objective

The goal of this project is to simulate the basic operations of a hotel management system. It provides functionalities like:
- Guest registration and room assignment
- Reservation tracking
- Adding and managing services
- Generating bills for each guest
- Maintaining historical records of guests and services used

This CLI-based tool is ideal for small hotels or for students learning about integrating Python with SQL.

## Tech Stack Used

- **Frontend:** Python (Command Line Interface)
- **Backend:** MySQL
- **Library:** `mysql-connector-python`
- **Database Name:** `hotel`
- **Main Tables:**
  - `rooms`
  - `guests`
  - `services`
  - `reservations`
  - `guest_services`
    
## Key Features
### 🛏 Room Management
- Add new rooms with room type and cost
- View available and booked rooms
- Assign rooms to guests upon reservation
###  Guest Management
- Register guests with name, contact info, check-in/check-out dates
- View all registered guests
###  Reservation System
- Book a room for a guest
- Prevent double booking by checking room availability
### Service Management
- Add services like food, spa, laundry, etc.
- Assign services to guests
- Track services used by each guest
### Billing System
- Generate total bill for guests including room charges and services used
- Bill details are calculated based on stay duration and selected services


## 📂 Project Structure


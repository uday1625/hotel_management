-- db_setup.sql
CREATE DATABASE IF NOT EXISTS Hotel;
USE Hotel;

-- Drop existing (safe for dev)
DROP TABLE IF EXISTS Payment;
DROP TABLE IF EXISTS Booking;
DROP TABLE IF EXISTS Room;
DROP TABLE IF EXISTS RoomType;
DROP TABLE IF EXISTS Guest;
DROP TABLE IF EXISTS Admins;

CREATE TABLE Admins (
  Admin_ID INT PRIMARY KEY AUTO_INCREMENT,
  Username VARCHAR(50) UNIQUE NOT NULL,
  Password VARCHAR(255) NOT NULL,
  FullName VARCHAR(100)
);

CREATE TABLE RoomType(
  Type_ID INT PRIMARY KEY,
  Type_Name VARCHAR(50),
  Description VARCHAR(200),
  Price_Per_Night DECIMAL(10,2)
);

CREATE TABLE Room(
  Room_ID INT PRIMARY KEY,
  Room_Number VARCHAR(20),
  Type_ID INT,
  Price DECIMAL(10,2),
  Status VARCHAR(20),
  FOREIGN KEY (Type_ID) REFERENCES RoomType(Type_ID)
);

CREATE TABLE Guest(
  Guest_ID INT PRIMARY KEY,
  Name VARCHAR(100),
  Phone VARCHAR(20),
  Email VARCHAR(100),
  Address VARCHAR(255)
);

CREATE TABLE Booking(
  Booking_ID INT PRIMARY KEY,
  Guest_ID INT,
  Room_ID INT,
  Check_IN_Date DATE,
  Check_Out_Date DATE,
  Status VARCHAR(20),
  FOREIGN KEY (Guest_ID) REFERENCES Guest(Guest_ID),
  FOREIGN KEY (Room_ID) REFERENCES Room(Room_ID)
);

CREATE TABLE Payment(
  Payment_ID INT PRIMARY KEY,
  Booking_ID INT,
  Amount DECIMAL(10,2),
  Payment_date DATE,
  Payment_method VARCHAR(50),
  FOREIGN KEY (Booking_ID) REFERENCES Booking(Booking_ID)
);

-- Seed admin (demo)
INSERT INTO Admins (Admin_ID, Username, Password, FullName) VALUES
(1, 'admin', 'admin123', 'Hotel Administrator');

-- Seed RoomType
INSERT INTO RoomType (Type_ID, Type_Name, Description, Price_Per_Night) VALUES
(1, 'Single', 'Single bed, basic room', 1000.00),
(2, 'Double', 'Double bed, more space', 1800.00),
(3, 'Suite', 'Luxury suite with extras', 3500.00);

-- Seed Rooms (20 rooms example)
INSERT INTO Room (Room_ID, Room_Number, Type_ID, Price, Status) VALUES
(1,'101',1,1000.00,'Available'),
(2,'102',1,1000.00,'Available'),
(3,'103',1,1000.00,'Available'),
(4,'104',1,1000.00,'Available'),
(5,'105',2,1800.00,'Available'),
(6,'106',2,1800.00,'Available'),
(7,'107',2,1800.00,'Available'),
(8,'108',2,1800.00,'Available'),
(9,'109',3,3500.00,'Available'),
(10,'110',3,3500.00,'Available'),
(11,'111',1,1000.00,'Available'),
(12,'112',1,1000.00,'Available'),
(13,'113',2,1800.00,'Available'),
(14,'114',2,1800.00,'Available'),
(15,'115',3,3500.00,'Available'),
(16,'116',1,1000.00,'Available'),
(17,'117',2,1800.00,'Available'),
(18,'118',3,3500.00,'Available'),
(19,'119',1,1000.00,'Available'),
(20,'120',2,1800.00,'Available');

-- Insert 50 Guest records (no password column)
INSERT INTO Guest (Guest_ID, Name, Phone, Email, Address) VALUES
(1,'Aarav Sharma','9000000001','aarav.sharma1@example.com','1 MG Road, City'),
(2,'Vivaan Patel','9000000002','vivaan.patel2@example.com','2 Park Lane, City'),
(3,'Kabir Singh','9000000003','kabir.singh3@example.com','3 Church St, City'),
(4,'Ishaan Verma','9000000004','ishaan.verma4@example.com','4 Hill Rd, City'),
(5,'Reyansh Gupta','9000000005','reyansh.gupta5@example.com','5 Lake View, City'),
(6,'Arjun Reddy','9000000006','arjun.reddy6@example.com','6 North St, City'),
(7,'Aditya Nair','9000000007','aditya.nair7@example.com','7 East End, City'),
(8,'Rohan Mehta','9000000008','rohan.mehta8@example.com','8 South Park, City'),
(9,'Krishna Joshi','9000000009','krishna.joshi9@example.com','9 West Ave, City'),
(10,'Shaurya Rao','9000000010','shaurya.rao10@example.com','10 Main St, City'),
(11,'Sai Kumar','9000000011','sai.kumar11@example.com','11 North Gate, City'),
(12,'Dhruv Malhotra','9000000012','dhruv.malhotra12@example.com','12 Central Ave, City'),
(13,'Ritvik Chopra','9000000013','ritvik.chopra13@example.com','13 Olive Rd, City'),
(14,'Kunal Bose','9000000014','kunal.bose14@example.com','14 Maple St, City'),
(15,'Naveen Kumar','9000000015','naveen.kumar15@example.com','15 Pine St, City'),
(16,'Manav Shah','9000000016','manav.shah16@example.com','16 Cedar Ln, City'),
(17,'Hrithik Sen','9000000017','hrithik.sen17@example.com','17 River Rd, City'),
(18,'Aniket Desai','9000000018','aniket.desai18@example.com','18 Terrace St, City'),
(19,'Tanishq Verma','9000000019','tanishq.verma19@example.com','19 Garden St, City'),
(20,'Varun Yadav','9000000020','varun.yadav20@example.com','20 Station Rd, City'),
(21,'Yash Thakur','9000000021','yash.thakur21@example.com','21 Market St, City'),
(22,'Ayaan Khan','9000000022','ayaan.khan22@example.com','22 High St, City'),
(23,'Samar Nair','9000000023','samar.nair23@example.com','23 Cross Rd, City'),
(24,'Kartik Iyer','9000000024','kartik.iyer24@example.com','24 Old Town, City'),
(25,'Om Prakash','9000000025','om.prakash25@example.com','25 New St, City'),
(26,'Vikram Rawat','9000000026','vikram.rawat26@example.com','26 Green Ln, City'),
(27,'Gaurang Patel','9000000027','gaurang.patel27@example.com','27 Orchard Rd, City'),
(28,'Ritesh Goyal','9000000028','ritesh.goyal28@example.com','28 Lake Rd, City'),
(29,'Deven Mehra','9000000029','deven.mehra29@example.com','29 Hilltop St, City'),
(30,'Siddharth Roy','9000000030','siddharth.roy30@example.com','30 Brook Ln, City'),
(31,'Pranav Singh','9000000031','pranav.singh31@example.com','31 Sunrise Blvd, City'),
(32,'Mihir Joshi','9000000032','mihir.joshi32@example.com','32 Sunset Rd, City'),
(33,'Raghav Kapoor','9000000033','raghav.kapoor33@example.com','33 Hill Crest, City'),
(34,'Neil Dutta','9000000034','neil.dutta34@example.com','34 Riverbank, City'),
(35,'Saket Jain','9000000035','saket.jain35@example.com','35 Valley Rd, City'),
(36,'Amit Bhatia','9000000036','amit.bhatia36@example.com','36 Ridge St, City'),
(37,'Ansh Verma','9000000037','ansh.verma37@example.com','37 Harbor Ave, City'),
(38,'Ravindra Kumar','9000000038','ravindra.kumar38@example.com','38 Wood St, City'),
(39,'Prithvi Shah','9000000039','prithvi.shah39@example.com','39 Bay Road, City'),
(40,'Sarvesh Nanda','9000000040','sarvesh.nanda40@example.com','40 Plaza St, City'),
(41,'Karan Ahuja','9000000041','karan.ahuja41@example.com','41 Beacon Rd, City'),
(42,'Mayank Sood','9000000042','mayank.sood42@example.com','42 Summit St, City'),
(43,'Rishi Bhatt','9000000043','rishi.bhatt43@example.com','43 Terrace Ln, City'),
(44,'Tarun Aggarwal','9000000044','tarun.aggarwal44@example.com','44 Bridge Rd, City'),
(45,'Yuvraj Chawla','9000000045','yuvraj.chawla45@example.com','45 Harbor St, City'),
(46,'Adarsh Pillai','9000000046','adarsh.pillai46@example.com','46 Harbor View, City'),
(47,'Nikhil Tiwari','9000000047','nikhil.tiwari47@example.com','47 Garden Ln, City'),
(48,'Shreyas Khatri','9000000048','shreyas.khatri48@example.com','48 Glen Rd, City'),
(49,'Anuj Bhardwaj','9000000049','anuj.bhardwaj49@example.com','49 Parkview, City'),
(50,'Sahil Mehra','9000000050','sahil.mehra50@example.com','50 Lakeside, City');

CREATE DATABASE IF NOT EXISTS t2;
USE t2;

CREATE TABLE Tourist (
    TouristID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100),
    PhoneNo VARCHAR(15),
    EmailID VARCHAR(100),
    DOB DATE,
    Age INT
);

CREATE TABLE TourPackage (
    PackageID INT PRIMARY KEY AUTO_INCREMENT,
    PackageName VARCHAR(100),
    Description TEXT,
    Duration INT,
    Price DECIMAL(10, 2)
);

CREATE TABLE Reservation (
    BookingID INT PRIMARY KEY AUTO_INCREMENT,
    TouristID INT,
    PackageID INT,
    NoOfPeople INT,
    BookingDate DATE,
    FOREIGN KEY (TouristID) REFERENCES Tourist(TouristID),
    FOREIGN KEY (PackageID) REFERENCES TourPackage(PackageID)
);

CREATE TABLE Transportation (
    TransportID INT PRIMARY KEY AUTO_INCREMENT,
    BookingID INT,
    TransportType VARCHAR(50),
    Departure DATETIME,
    Arrival DATETIME,
    FOREIGN KEY (BookingID) REFERENCES Reservation(BookingID)
);

CREATE TABLE Accommodation (
    HotelID INT PRIMARY KEY AUTO_INCREMENT,
    BookingID INT,
    HotelName VARCHAR(100),
    Location VARCHAR(100),
    Ratings DECIMAL(3, 2),
    FOREIGN KEY (BookingID) REFERENCES Reservation(BookingID)
);

CREATE TABLE Payment (
    PaymentID INT PRIMARY KEY AUTO_INCREMENT,
    BookingID INT,
    Amount DECIMAL(10, 2),
    Method VARCHAR(50),
    PaymentDate DATE,
    Status VARCHAR(50),
    FOREIGN KEY (BookingID) REFERENCES Reservation(BookingID)
);

-- Insert into Tourist
INSERT INTO Tourist (Name, PhoneNo, EmailID, DOB, Age) VALUES
('John Doe', '123-456-7890', 'john@example.com', '1985-06-15', 38),
('Jane Smith', '234-567-8901', 'jane@example.com', '1990-07-20', 34),
('Alice Johnson', '345-678-9012', 'alice@example.com', '1995-08-25', 28);

-- Insert into TourPackage
INSERT INTO TourPackage (PackageName, Description, Duration, Price) VALUES
('Beach Paradise', 'A relaxing week on a tropical beach', 7, 1500.00),
('Mountain Adventure', 'A thrilling trek through the mountains', 10, 2000.00),
('City Explorer', 'A comprehensive tour of the city\'s landmarks', 5, 1000.00);

-- Insert into Reservation
INSERT INTO Reservation (TouristID, PackageID, NoOfPeople, BookingDate) VALUES
(1, 1, 2, '2024-07-01'),
(2, 2, 4, '2024-07-05'),
(3, 3, 1, '2024-07-10');

-- Insert into Transportation
INSERT INTO Transportation (BookingID, TransportType, Departure, Arrival) VALUES
(1, 'Flight', '2024-07-01 08:00:00', '2024-07-01 12:00:00'),
(2, 'Train', '2024-07-05 09:00:00', '2024-07-05 15:00:00'),
(3, 'Bus', '2024-07-10 07:00:00', '2024-07-10 10:00:00');

-- Insert into Accommodation
INSERT INTO Accommodation (BookingID, HotelName, Location, Ratings) VALUES
(1, 'Beach Resort', 'Tropical Beach', 4.5),
(2, 'Mountain Lodge', 'High Mountains', 4.8),
(3, 'City Hotel', 'Downtown', 4.2);

-- Insert into Payment
INSERT INTO Payment (BookingID, Amount, Method, PaymentDate, Status) VALUES
(1, 3000.00, 'Credit Card', '2024-06-20', 'Paid'),
(2, 8000.00, 'Bank Transfer', '2024-06-25', 'Paid'),
(3, 1000.00, 'PayPal', '2024-06-30', 'Paid');

CREATE TABLE admin (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL -- Consider using a longer VARCHAR for hashed passwords
);

-- Insert an admin user (remember to hash the password)
INSERT INTO admin (username, password) VALUES ('ananya', '1234'); -- Remember to hash passwords

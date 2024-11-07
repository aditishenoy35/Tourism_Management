import streamlit as st
import mysql.connector
from mysql.connector import Error, pooling
import pandas as pd
from decimal import Decimal
from PIL import Image
import os


# Database connection pool
def create_connection_pool():
    return mysql.connector.pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=5,
        host="localhost",
        user="root",
        password="xyz",
        database="t2",
    )


connection_pool = create_connection_pool()


def set_app_style():
    """
    Defines custom CSS styles for the Streamlit app.
    """
    image_path = r"C:\\Users\\Desktop\\bg2.jpg"
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5)), url("data:image/png;base64,{image_to_base64(image_path)}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                color: #000000; /* Make all text dark black */
            }}
            .stSidebarContent {{
                background: rgba(255, 255, 255, 0.8); /* Transparent white background for the sidebar */
                color: #000000; /* Sidebar text color */
            }}
            h1, h2, h3, h4, h5, h6 {{
                color: #000000; /* Heading colors */
            }}
            .stMarkdown p {{
                color: #000000; /* Paragraph text color */
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def image_to_base64(image_path):
    """
    Converts an image to a base64 string.
    """
    import base64

    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()



def create_connection():
    """
    Creates and returns a database connection from the connection pool.
    """
    try:
        connection = connection_pool.get_connection()
        st.write("Database connection established")
        return connection
    except Error as e:
        st.error(f"Database connection error: {e}")
    return None


def check_credentials(username, password, role):
    """
    Checks user credentials against the database.
    """
    connection = create_connection()
    if connection is None:
        return None

    cursor = connection.cursor(dictionary=True)
    try:
        if role == "Admin":
            cursor.execute(
                "SELECT * FROM admin WHERE username=%s AND password=%s",
                (username, password),
            )
        else:
            cursor.execute(
                "SELECT * FROM Tourist WHERE EmailID=%s AND PhoneNo=%s",
                (username, password),
            )
        user = cursor.fetchone()
        return user
    except Error as e:
        st.error(f"SQL error: {e}")
    finally:
        connection.close()


def format_data(data):
    """
    Formats data for display.
    """
    for item in data:
        for key, value in item.items():
            if isinstance(value, Decimal):
                item[key] = float(value)
            elif hasattr(value, "isoformat"):
                item[key] = value.isoformat()
    return data


def admin_dashboard():
    """
    Displays the admin dashboard with options to add, view, update, or delete data.
    """
    st.title("Admin Dashboard")
    operation = st.sidebar.selectbox(
        "Select Operation", ["Add", "Update", "Delete", "View"]
    )
    table = st.sidebar.selectbox(
        "Select Table",
        [
            "Tourist",
            "TourPackage",
            "Reservation",
            "Transportation",
            "Accommodation",
            "Payment",
        ],
    )

    if operation == "Add":
        add_entry(table)
    elif operation == "Update":
        update_entry(table)
    elif operation == "Delete":
        delete_entry(table)
    elif operation == "View":
        view_entries(table)


def add_entry(table):
    """
    Provides forms to add data to various tables.
    """
    st.subheader(f"Add {table}")
    with st.form(key=f"add_{table.lower()}_form"):
        if table == "Tourist":
            name = st.text_input("Name")
            phone_no = st.text_input("Phone Number")
            email_id = st.text_input("Email ID")
            dob = st.date_input("Date of Birth")
            age = st.number_input("Age", min_value=0, max_value=120)
            submit_button = st.form_submit_button("Add Tourist")
            if submit_button:
                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute(
                    """
                    INSERT INTO Tourist (Name, PhoneNo, EmailID, DOB, Age) 
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (name, phone_no, email_id, dob, age),
                )
                connection.commit()
                connection.close()
                st.success("Tourist added successfully!")
        elif table == "TourPackage":
            name = st.text_input("Package Name")
            description = st.text_area("Description")
            duration = st.number_input("Duration (days)", min_value=1)
            price = st.number_input("Price", format="%.2f")
            submit_button = st.form_submit_button("Add Tour Package")
            if submit_button:
                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute(
                    """
                    INSERT INTO TourPackage (PackageName, Description, Duration, Price) 
                    VALUES (%s, %s, %s, %s)
                    """,
                    (name, description, duration, price),
                )
                connection.commit()
                connection.close()
                st.success("Tour Package added successfully!")
        elif table == "Reservation":
            tourist_id = st.number_input("Tourist ID")
            package_id = st.number_input("Package ID")
            no_of_people = st.number_input("Number of People", min_value=1)
            booking_date = st.date_input("Booking Date")
            submit_button = st.form_submit_button("Add Reservation")
            if submit_button:
                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute(
                    """
                    INSERT INTO Reservation (TouristID, PackageID, NoOfPeople, BookingDate) 
                    VALUES (%s, %s, %s, %s)
                    """,
                    (tourist_id, package_id, no_of_people, booking_date),
                )
                connection.commit()
                connection.close()
                st.success("Reservation added successfully!")
        elif table == "Transportation":
            booking_id = st.number_input("Booking ID")
            transport_type = st.text_input("Transport Type")
            departure = st.date_input("Departure Date and Time")
            arrival = st.date_input("Arrival Date and Time")
            submit_button = st.form_submit_button("Add Transportation")
            if submit_button:
                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute(
                    """
                    INSERT INTO Transportation (BookingID, TransportType, Departure, Arrival) 
                    VALUES (%s, %s, %s, %s)
                    """,
                    (booking_id, transport_type, departure, arrival),
                )
                connection.commit()
                connection.close()
                st.success("Transportation added successfully!")
        elif table == "Accommodation":
            booking_id = st.number_input("Booking ID")
            hotel_name = st.text_input("Hotel Name")
            location = st.text_input("Location")
            ratings = st.number_input(
                "Ratings", min_value=0.0, max_value=5.0, format="%.1f"
            )
            submit_button = st.form_submit_button("Add Accommodation")
            if submit_button:
                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute(
                    """
                    INSERT INTO Accommodation (BookingID, HotelName, Location, Ratings) 
                    VALUES (%s, %s, %s, %s)
                    """,
                    (booking_id, hotel_name, location, ratings),
                )
                connection.commit()
                connection.close()
                st.success("Accommodation added successfully!")
        elif table == "Payment":
            booking_id = st.number_input("Booking ID")
            amount = st.number_input("Amount", format="%.2f")
            method = st.text_input("Payment Method")
            payment_date = st.date_input("Payment Date")
            status = st.text_input("Status")
            submit_button = st.form_submit_button("Add Payment")
            if submit_button:
                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute(
                    """
                    INSERT INTO Payment (BookingID, Amount, Method, PaymentDate, Status) 
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (booking_id, amount, method, payment_date, status),
                )
                connection.commit()
                connection.close()
                st.success("Payment added successfully!")


def update_entry(table):
    """
    Provides forms to update data in various tables.
    """
    st.subheader(f"Update {table}")
    id_to_update = st.number_input(f"{table} ID to Update", min_value=1)

    if not id_to_update:
        st.warning("Please enter a valid ID to update.")
        return

    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        if table == "Tourist":
            cursor.execute("SELECT * FROM Tourist WHERE TouristID=%s", (id_to_update,))
            data = cursor.fetchone()
            if data:
                name = st.text_input("Name", value=data["Name"])
                phone_no = st.text_input("Phone Number", value=data["PhoneNo"])
                email_id = st.text_input("Email ID", value=data["EmailID"])
                dob = st.date_input("Date of Birth", value=data["DOB"])
                age = st.number_input(
                    "Age", value=int(data["Age"]), min_value=0, max_value=120
                )
                if st.button("Update Tourist"):
                    cursor.execute(
                        """
                        UPDATE Tourist 
                        SET Name=%s, PhoneNo=%s, EmailID=%s, DOB=%s, Age=%s 
                        WHERE TouristID=%s
                        """,
                        (name, phone_no, email_id, dob, age, id_to_update),
                    )
                    connection.commit()
                    st.success("Tourist updated successfully!")
            else:
                st.warning(f"No tourist found with ID {id_to_update}")
        elif table == "TourPackage":
            cursor.execute(
                "SELECT * FROM TourPackage WHERE PackageID=%s", (id_to_update,)
            )
            data = cursor.fetchone()
            if data:
                name = st.text_input("Package Name", value=data["PackageName"])
                description = st.text_area("Description", value=data["Description"])
                duration = st.number_input(
                    "Duration (days)", value=int(data["Duration"]), min_value=1
                )
                price = st.number_input(
                    "Price", value=float(data["Price"]), format="%.2f"
                )
                if st.button("Update Tour Package"):
                    cursor.execute(
                        """
                        UPDATE TourPackage 
                        SET PackageName=%s, Description=%s, Duration=%s, Price=%s 
                        WHERE PackageID=%s
                        """,
                        (name, description, duration, price, id_to_update),
                    )
                    connection.commit()
                    st.success("Tour Package updated successfully!")
            else:
                st.warning(f"No tour package found with ID {id_to_update}")
        elif table == "Reservation":
            cursor.execute(
                "SELECT * FROM Reservation WHERE BookingID=%s", (id_to_update,)
            )
            data = cursor.fetchone()
            if data:
                tourist_id = st.number_input("Tourist ID", value=int(data["TouristID"]))
                package_id = st.number_input("Package ID", value=int(data["PackageID"]))
                no_of_people = st.number_input(
                    "Number of People", value=int(data["NoOfPeople"]), min_value=1
                )
                booking_date = st.date_input("Booking Date", value=data["BookingDate"])
                if st.button("Update Reservation"):
                    cursor.execute(
                        """
                        UPDATE Reservation 
                        SET TouristID=%s, PackageID=%s, NoOfPeople=%s, BookingDate=%s 
                        WHERE BookingID=%s
                        """,
                        (
                            tourist_id,
                            package_id,
                            no_of_people,
                            booking_date,
                            id_to_update,
                        ),
                    )
                    connection.commit()
                    st.success("Reservation updated successfully!")
            else:
                st.warning(f"No reservation found with ID {id_to_update}")
        elif table == "Transportation":
            cursor.execute(
                "SELECT * FROM Transportation WHERE TransportID=%s", (id_to_update,)
            )
            data = cursor.fetchone()
            if data:
                booking_id = st.number_input("Booking ID", value=int(data["BookingID"]))
                transport_type = st.text_input(
                    "Transport Type", value=data["TransportType"]
                )
                departure = st.date_input(
                    "Departure Date and Time", value=data["Departure"]
                )
                arrival = st.date_input("Arrival Date and Time", value=data["Arrival"])
                if st.button("Update Transportation"):
                    cursor.execute(
                        """
                        UPDATE Transportation 
                        SET BookingID=%s, TransportType=%s, Departure=%s, Arrival=%s 
                        WHERE TransportID=%s
                        """,
                        (booking_id, transport_type, departure, arrival, id_to_update),
                    )
                    connection.commit()
                    st.success("Transportation updated successfully!")
            else:
                st.warning(f"No transportation found with ID {id_to_update}")
        elif table == "Accommodation":
            cursor.execute(
                "SELECT * FROM Accommodation WHERE BookingID=%s", (id_to_update,)
            )
            data = cursor.fetchone()
            if data:
                booking_id = st.number_input("Booking ID", value=int(data["BookingID"]))
                hotel_name = st.text_input("Hotel Name", value=data["HotelName"])
                location = st.text_input("Location", value=data["Location"])
                ratings = st.number_input(
                    "Ratings",
                    value=float(data["Ratings"]),
                    min_value=0.0,
                    max_value=5.0,
                    format="%.1f",
                )
                if st.button("Update Accommodation"):
                    cursor.execute(
                        """
                        UPDATE Accommodation 
                        SET BookingID=%s, HotelName=%s, Location=%s, Ratings=%s 
                        WHERE BookingID=%s
                        """,
                        (booking_id, hotel_name, location, ratings, id_to_update),
                    )
                    connection.commit()
                    st.success("Accommodation updated successfully!")
            else:
                st.warning(f"No accommodation found with ID {id_to_update}")
        elif table == "Payment":
            cursor.execute("SELECT * FROM Payment WHERE PaymentID=%s", (id_to_update,))
            data = cursor.fetchone()
            if data:
                booking_id = st.number_input("Booking ID", value=int(data["BookingID"]))
                amount = st.number_input(
                    "Amount", value=float(data["Amount"]), format="%.2f"
                )
                method = st.text_input("Payment Method", value=data["Method"])
                payment_date = st.date_input("Payment Date", value=data["PaymentDate"])
                status = st.text_input("Status", value=data["Status"])
                if st.button("Update Payment"):
                    cursor.execute(
                        """
                        UPDATE Payment 
                        SET BookingID=%s, Amount=%s, Method=%s, PaymentDate=%s, Status=%s 
                        WHERE PaymentID=%s
                        """,
                        (
                            booking_id,
                            amount,
                            method,
                            payment_date,
                            status,
                            id_to_update,
                        ),
                    )
                    connection.commit()
                    st.success("Payment updated successfully!")
            else:
                st.warning(f"No payment found with ID {id_to_update}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        connection.close()


def delete_entry(table):
    st.subheader(f"Delete {table}")
    id_to_delete = st.number_input(f"{table} ID to Delete", min_value=1)

    if st.button("Delete Entry"):
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Define the primary key column for each table
        primary_keys = {
            "Tourist": "TouristID",
            "TourPackage": "PackageID",
            "Reservation": "BookingID",
            "Transportation": "TransportID",
            "Accommodation": "HotelID",
            "Payment": "PaymentID",
        }

        if table in primary_keys:
            primary_key = primary_keys[table]

            # Delete dependent rows
            if table == "Tourist":
                cursor.execute(
                    "SELECT BookingID FROM Reservation WHERE TouristID=%s",
                    (id_to_delete,),
                )
                booking_ids = cursor.fetchall()

                for booking_id in booking_ids:
                    booking_id = booking_id[0]
                    cursor.execute(
                        "DELETE FROM Transportation WHERE BookingID=%s", (booking_id,)
                    )
                    cursor.execute(
                        "DELETE FROM Accommodation WHERE BookingID=%s", (booking_id,)
                    )
                    cursor.execute(
                        "DELETE FROM Payment WHERE BookingID=%s", (booking_id,)
                    )

                cursor.execute(
                    "DELETE FROM Reservation WHERE TouristID=%s", (id_to_delete,)
                )

            elif table == "TourPackage":
                cursor.execute(
                    "SELECT BookingID FROM Reservation WHERE PackageID=%s",
                    (id_to_delete,),
                )
                booking_ids = cursor.fetchall()

                for booking_id in booking_ids:
                    booking_id = booking_id[0]
                    cursor.execute(
                        "DELETE FROM Transportation WHERE BookingID=%s", (booking_id,)
                    )
                    cursor.execute(
                        "DELETE FROM Accommodation WHERE BookingID=%s", (booking_id,)
                    )
                    cursor.execute(
                        "DELETE FROM Payment WHERE BookingID=%s", (booking_id,)
                    )

                cursor.execute(
                    "DELETE FROM Reservation WHERE PackageID=%s", (id_to_delete,)
                )

            elif table == "Reservation":
                cursor.execute(
                    "DELETE FROM Transportation WHERE BookingID=%s", (id_to_delete,)
                )
                cursor.execute(
                    "DELETE FROM Accommodation WHERE BookingID=%s", (id_to_delete,)
                )
                cursor.execute(
                    "DELETE FROM Payment WHERE BookingID=%s", (id_to_delete,)
                )

            # Now delete the row from the selected table
            cursor.execute(
                f"DELETE FROM {table} WHERE {primary_key}=%s", (id_to_delete,)
            )
            connection.commit()
            st.success(f"{table} deleted successfully!")
        else:
            st.error("Invalid table selected")

        connection.close()


def view_entries(table, tourist_id=None):
    """
    Displays data from various tables. Optionally filters by tourist ID.
    """
    st.subheader(f"View {table} Data")
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    if tourist_id:
        if table == "TourPackage":
            cursor.execute("""
                SELECT tp.* 
                FROM TourPackage tp 
                JOIN Reservation r ON tp.PackageID = r.PackageID 
                WHERE r.TouristID = %s
            """, (tourist_id,))
        else:
            query = f"""
                SELECT * FROM {table} 
                WHERE BookingID IN (
                    SELECT BookingID FROM Reservation WHERE TouristID = %s
                )
            """
            cursor.execute(query, (tourist_id,))
    else:
        cursor.execute(f"SELECT * FROM {table}")

    data = cursor.fetchall()
    data = format_data(data)
    st.dataframe(pd.DataFrame(data))
    connection.close()

def tourist_dashboard():
    """
    Displays the tourist dashboard with options to view data.
    """
    st.title("Tourist Dashboard")
    user = st.session_state.get("user", {})

    # Display tourist details
    name = user.get("Name", "User")
    phone_no = user.get("PhoneNo", "N/A")
    tourist_id = user.get("TouristID")

    st.write(f"Welcome, {name}!")
    st.write(f"Phone Number: {phone_no}")

    operation = st.sidebar.selectbox(
        "Select Operation",
        [
            "View Tour Packages",
            "View Reservations",
            "View Payments",
            "View Accommodation",
            "View Transportation",
        ],
    )

    if operation == "View Tour Packages":
        view_entries("TourPackage", tourist_id)
    elif operation == "View Reservations":
        view_entries("Reservation", tourist_id)
    elif operation == "View Payments":
        view_entries("Payment", tourist_id)
    elif operation == "View Accommodation":
        view_entries("Accommodation", tourist_id)
    elif operation == "View Transportation":
        view_entries("Transportation", tourist_id)

def show_image_carousel():
    """
    Displays an image carousel with navigation arrows and a unique dark caption for each image.
    """
    st.subheader("Image Carousel")

    # List of image file paths
    image_files = [
        r"C:\\Users\\Desktop\\forest.jpg",
        r"C:\\Users\\Desktop\\tajmahal (2).png",
        r"C:\\Users\\Desktop\\image.jpg",
    ]

    # Corresponding captions for each image
    captions = [
        "A serene forest view.",
        "The majestic Taj Mahal.",
        "A breathtaking mountain scene.",
    ]

    # Initialize session state if not already initialized
    if "image_index" not in st.session_state:
        st.session_state.image_index = 0

    if not image_files:
        st.write("No images found.")
        return

    num_images = len(image_files)

    # Display the current image
    current_image_path = image_files[st.session_state.image_index]
    image = Image.open(current_image_path)
    st.image(
        image,
        use_column_width=True,
    )

    # Display dark caption using Markdown and HTML
    caption_html = f"""
    <p style="color: black; font-size: 16px; text-align: center;">
        {captions[st.session_state.image_index]}
    </p>
    """
    st.markdown(caption_html, unsafe_allow_html=True)

    # Navigation
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("◀"):
            if st.session_state.image_index > 0:
                st.session_state.image_index -= 1
            else:
                st.session_state.image_index = num_images - 1
    with col3:
        if st.button("▶"):
            if st.session_state.image_index < num_images - 1:
                st.session_state.image_index += 1
            else:
                st.session_state.image_index = 0


def login():
    """
    Handles user login and sets session state.
    """
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    role = st.sidebar.radio("Role", ["Admin", "Tourist"])

    if st.sidebar.button("Login"):
        user = check_credentials(username, password, role)
        if user:
            st.session_state.update({"user": user, "role": role})
            st.success(f"Welcome, {username}!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")
    show_image_carousel()


def main():
    set_app_style()
    st.title("Tourism Management system")
    st.write("Check out our packages")
    if "user" not in st.session_state:
        login()
    else:
        if st.session_state["role"] == "Admin":
            admin_dashboard()
        else:
            tourist_dashboard()
            show_image_carousel()
            st.text("Check out our packages which are perfect for the weather")


if __name__ == "__main__":
    main()

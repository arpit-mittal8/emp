import mysql.connector
from prettytable import PrettyTable

def connect_to_database():
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="company"
        )
        return conn
    except mysql.connector.Error as err:
        print("Error connecting to database:", err)
        return None

def get_access_level(conn, user_id):
    if user_id == 2002:
        return 'HR'
    else:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT access_level FROM emp WHERE emp_id = %s", (user_id,))
            access_level = cursor.fetchone()
            cursor.close()
            return access_level[0] if access_level else None
        except mysql.connector.Error as err:
            print("Error retrieving access level:", err)
            return None

def get_data_for_user(conn, user_id):
    print("User ID:", user_id)  # Debug output
    access_level = get_access_level(conn, user_id)
    print("Access Level:", access_level)  # Debug output
    if access_level == 'HR':
        try:
            # Query to fetch all data
            query = """
                SELECT e.emp_id, e.name, e.mobile_no, e.email, e.branch, e.date_of_joining,
                       a.ctc, a.full_day, a.half_day, a.total_leaves, a.total_attendance
                FROM emp e
                JOIN attendance a ON e.emp_id = a.emp_id
            """
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
            return data
        except mysql.connector.Error as err:
            print("Error fetching data for HR:", err)
            return None
    elif access_level:
        try:
            # Query to fetch data for the specific user
            query = """
                SELECT e.emp_id, e.name, e.mobile_no, e.email, e.branch, e.date_of_joining,
                       a.ctc, a.full_day, a.half_day, a.total_leaves, a.total_attendance
                FROM emp e
                JOIN attendance a ON e.emp_id = a.emp_id
                WHERE e.emp_id = %s
            """
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            data = cursor.fetchall()
            cursor.close()
            return data
        except mysql.connector.Error as err:
            print("Error fetching data for employee:", err)
            return None
    else:
        return None

def show_table(data):
    if data:
        # Create PrettyTable instance
        table = PrettyTable()
        table.field_names = ["emp_id", "Name", "Mobile No", "Email", "Branch", "Date of Joining",
                             "CTC", "Full Day", "Half Day", "Total Leaves", "Total Attendance"]

        # Add rows to the table
        for row in data:
            table.add_row(row)

        # Print the table
        print(table)
    else:
        print("No data to display")

# Example usage
try:
    conn = connect_to_database()
    if conn:
        user_id = int(input("Enter your user id: "))  # Assuming 'p1' is the user ID for HR
        data = get_data_for_user(conn, user_id)
        show_table(data)
    else:
        print("Failed to establish connection to the database.")
except ValueError:
    print("Invalid user ID. Please enter a valid numeric user ID.")

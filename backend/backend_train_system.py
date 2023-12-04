import sqlite3
import pandas as pd

# Adjust the database path as per your setup
DB_NAME = 'trains.db'  # Replace with your database path

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

def clear_tables():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = cursor.fetchall()
    print(table_names)
    for table in table_names:
        table_name = table[0]
        cursor.execute(f"DROP TABLE {table_name};")
        
def trim_string(s):
    if isinstance(s, str):
        return s.strip()
    else:
        return s

def import_csv():
    # Adjust the paths of CSV files as per your setup
    csv_list = ['Train.csv', 
                'booked.csv', 
                'Passenger.csv', 
                'Train_status.csv']

    for csv_file in csv_list:
        df = pd.read_csv(csv_file)
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

        columns_list = df.columns.tolist()
        new_column_list = [column_name.strip() for column_name in columns_list]

        df.columns = new_column_list
        table_name = csv_file.split('.')[0]

        df.to_sql(table_name, conn, if_exists='replace', index=False)

def view_db():
    csv_list = ['Train.csv', 'booked.csv', 'Passenger.csv', 'Train_status.csv']

    for csv_file in csv_list:
        table_name = csv_file.split('.')[0]
        query = f'SELECT * FROM {table_name}'
        df = pd.read_sql_query(query, conn)
        print('\n')
        print(f"{table_name}")
        print("\n")
        print(df)

def find_booking_by_name(first_name, last_name):
    query = f"SELECT * FROM Passenger WHERE first_name = '{first_name}' AND last_name = '{last_name}'"
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows[0]

def find_by_date(date):
    query1 = f'SELECT * FROM Train_status WHERE TrainDate = "{date}"'
    cursor.execute(query1)
    rows = list(cursor.fetchall())
    train_name = rows[0][1]

    query2 = f'SELECT * FROM Train WHERE "Train Name" = "{train_name}"'
    cursor.execute(query2)
    rows1 = list(cursor.fetchall())
    train_number = rows1[0][0]

    query3 = f'SELECT Passanger_ssn FROM booked WHERE Train_Number = {train_number} AND Status = "Booked"'
    cursor.execute(query3)
    rows2 = list(cursor.fetchall())

    all_passengers = []
    for ssn in rows2:
        query4 = f'SELECT * FROM Passenger WHERE SSN = {ssn[0]}'
        cursor.execute(query4)
        rows3 = cursor.fetchone()
        all_passengers.append(rows3)

    return all_passengers

def find_passengers_by_age_range(age_min, age_max):
    query = f'''
    SELECT 
        t.Train_Number, t."Train Name", t.Source, t.Destination, 
        p.Name, p.Address, p.Category, b.Staus 
    FROM 
        Passenger p 
    JOIN 
        booked b ON p.SSN = b.Passanger_ssn
    JOIN 
        Train t ON b.Train_Number = t.Train_Number
    WHERE 
        p.Age BETWEEN {age_min} AND {age_max}
    '''

    cursor.execute(query)
    all_trains = cursor.fetchall()
    return all_trains

def find_available_trains():
    query = f'''
    SELECT 
        t."Train Name",
        COUNT(b.Passanger_ssn) AS PassengerCount
    FROM 
        Train t
    JOIN 
        booked b ON t."Train Number" = b.Train_Number
    GROUP BY 
        t."Train Name"
    '''

    cursor.execute(query)
    rows = cursor.fetchall()
    return rows




def find_passengers_by_train(train_name):
    query = f'''
    SELECT 
        p.Name, p.SSN 
    FROM 
        Passenger p 
    JOIN 
        booked b ON p.SSN = b.Passanger_ssn
    JOIN 
        Train t ON b.Train_Number = t.Train_Number
    WHERE 
        t."Train Name" = "{train_name}" AND b.Status = "Booked"
    '''

    cursor.execute(query)
    passengers = cursor.fetchall()

    return passengers

def cancel_ticket_and_update_waiting_list(passenger_ssn):
    # Cancel the ticket
    cancel_query = f"DELETE FROM booked WHERE Passanger_ssn = {passenger_ssn} AND Status = 'Booked'"
    cursor.execute(cancel_query)

    # Optional: Update the first passenger in the waiting list
    update_query = '''
    UPDATE booked
    SET Status = 'Booked'
    WHERE Passanger_ssn = (
        SELECT Passanger_ssn 
        FROM booked 
        WHERE Status = 'Waiting'
        ORDER BY Booking_ID ASC
        LIMIT 1
    )
    '''
    cursor.execute(update_query)

def main():
    clear_tables()
    import_csv()

    # View database contents
    view_db()

    # Find booking by name
    booking_info = find_booking_by_name("John", "Doe")
    print(f"\nBooking Info for John Doe:\n{booking_info}")

    # Find passengers by date
    passengers_by_date = find_by_date("2022-02-20")
    print(f"\nPassengers on 2022-02-20:\n{passengers_by_date}")

    # Find passengers between ages 50 and 60
    passengers_in_age_range = find_passengers_by_age_range(50, 60)
    print("\nPassengers between ages 50 and 60:")
    for passenger in passengers_in_age_range:
        print(passenger)

    # Find passengers by train
    train_name = "Express"
    passengers_in_train = find_passengers_by_train(train_name)
    print(f"\nPassengers in {train_name}:")
    for passenger in passengers_in_train:
        print(passenger)

    # Cancel a ticket and update waiting list
    passenger_ssn_to_cancel = 123456789  # Replace with an actual SSN
    cancel_ticket_and_update_waiting_list(passenger_ssn_to_cancel)
    print(f"\nTicket for SSN {passenger_ssn_to_cancel} cancelled and waiting list updated.")

    conn.commit()
    conn.close()

main()

# (1, John, Butt, Orient Express)

{
    "Train_Number": rows[0]
}

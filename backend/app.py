from flask import Flask, request, jsonify
import sqlite3
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

DB_NAME = 'trains.db'  # Make sure this path is correct

# Database Helper Functions
def connect_db():
    return sqlite3.connect(DB_NAME)

def execute_query(query, args=(), fetch_one=False):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, args)
    if fetch_one:
        result = cursor.fetchone()
    else:
        result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result

def find_booking_by_name(first_name, last_name):
    query = f"SELECT * FROM Passenger WHERE first_name = ? AND last_name = ?"
    result = execute_query(query,(first_name, last_name))
    final_result = []
    for each_result in result:
        details = {}
        details["Train_Number"] = each_result[0]
        details["TrainName"] = each_result[1]
        details["Source"] = each_result[2]
        details["Destination"] = each_result[3]
        final_result.append(details)

    print(final_result)
    return final_result

def find_by_date(date):
    query = """
    SELECT Passanger_ssn, first_name, last_name, address, city, county, phone, SSN, bdate
    FROM booked b
    JOIN Passenger p ON b.Passanger_ssn = p.SSN
    JOIN Train_status ts ON b.Train_Number = b.Train_Number
    WHERE b.Staus = 'Booked' AND ts.TrainDate = ?
    """
    result = execute_query(query, (date,))
    results = []
    print(result)
    for each_result in result:
        details = {
		"Passanger_ssn": each_result[0],
		"first_name": each_result[1],
		"last_name": each_result[2],
		"address": each_result[3],
		"city": each_result[4],
		"county": each_result[5],
		"phone": each_result[6],
		"SSN": each_result[7],
		"bdate": each_result[8]
	    }
        results.append(details)
    response = {"columns":["Passanger_ssn", "first_name", "last_name", "address", "city"
                        "county", "phone", "SSN" , "bdate"], "response":results}
    return response



def find_passengers_by_train(train_name):
    query = """
    SELECT p."first_name", p."last_name", p."SSN"
    FROM Passenger p
    JOIN booked b ON p."SSN" = b."Passanger_ssn"
    JOIN Train t ON b."Train_Number" = t."Train Number"
    WHERE t."Train Name" = ? AND b.Staus = 'Booked'
    """
    result = execute_query(query, (train_name,))
    
    return result


def find_available_trains():
    query = """
    SELECT 
        t."Train Name",
        COUNT(b.Passanger_ssn) AS PassengerCount
    FROM 
        Train t
    JOIN 
        booked b ON t."Train Number" = b.Train_Number
    GROUP BY 
        t."Train Name"
    """

    result = execute_query(query)

    return result

def cancel_ticket_and_update_waiting_list(passenger_ssn):
    cancel_query = "DELETE FROM booked WHERE Passanger_ssn = ? AND Staus = 'Booked'"
    execute_query(cancel_query, (passenger_ssn,))

    update_query = """
    UPDATE booked
    SET Staus = 'Booked'
    WHERE Passanger_ssn = (
        SELECT Passanger_ssn 
        FROM booked 
        WHERE Staus = 'Waiting'
        LIMIT 1
    )
    """
    execute_query(update_query)

    # Fetch the updated passenger details
    new_booked_query = """
    SELECT first_name, last_name, SSN
    FROM Passenger 
    WHERE SSN = (
        SELECT Passanger_ssn 
        FROM booked 
        WHERE Staus = 'Booked'
        LIMIT 1
    )
    """
    result = execute_query(new_booked_query, fetch_one=True)
    details = {"first_name":result[0],
               "last_name":result[1],
               "Passanger_ssn":result[2],}
    return details

# Flask API Endpoints

@app.route('/booked_tickets', methods=['POST', 'OPTIONS'])
def get_trains_for_passenger():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    print(first_name, last_name)

    if not first_name or not last_name:
        return jsonify({"error": "First name and last name are required"}), 400

    try:
        query = """
        SELECT 
            t."Train Number", 
            t."Train Name", 
            t."Source Station", 
            t."Destination Station"
        FROM 
            Passenger p
        JOIN 
            booked b ON p.SSN = b.Passanger_ssn
        JOIN 
            Train t ON b.Train_Number = t."Train Number"
        WHERE 
            p.first_name = ? AND 
            p.last_name = ?
        """
        results = execute_query(query, (first_name, last_name))
        response = {"columns":["Train_Number", "TrainName", "Source", "Destination"], "result":None}
        final_result = []
        for each_result in results:
            details = {}
            details["Train_Number"] = each_result[0]
            details["TrainName"] = each_result[1]
            details["Source"] = each_result[2]
            details["Destination"] = each_result[3]
            final_result.append(details)
        response["result"] = final_result
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/confirmed_tickets', methods=['POST', 'OPTIONS'])
def confirmed_tickets():
    data = request.json
    date = data['TrainDate']
    result = find_by_date(date)
    print(result)
    return jsonify(result)

from datetime import datetime

@app.route('/passengers_in_age_range', methods=['POST', 'OPTIONS'])
def passengers_in_age_range():
    try:
        data = request.json
        min_age = data.get('min_age')
        max_age = data.get('max_age')

        if min_age is None or max_age is None:
            return jsonify({"error": "Minimum and maximum age are required"}), 400

        # Current year for age calculation
        current_year = datetime.now().year

        # Formulating the SQL query with proper string formatting
        query = f"""
         SELECT t."Train Number", t."Train Name", t."Source Station", t."Destination Station",
        p.first_name || ' ' || p.last_name AS passengerName,
        p.address, b.Ticket_Type, b.Staus
        FROM train t
        JOIN booked b ON t."Train Number" = b.Train_Number
        JOIN passenger p ON b.Passanger_ssn = p.SSN
        WHERE ({current_year} - CAST(strftime('%Y', '19' || substr(p.bdate, 7, 2) || '-' || 
                       substr(p.bdate, 1, 2) || '-' || 
                       substr(p.bdate, 4, 2)) AS INTEGER)) BETWEEN {min_age} AND {max_age}

        """
        results = execute_query(query)
        final_result = []
        print(results)
        # for result in results:
        #     final_result["Train_Number"] = 
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@app.route('/available_trains', methods=['GET', 'OPTIONS'])
def available_trains():
    try:
        results = find_available_trains()
        final_result = [] 
        response = {"columns":["TrainName", "passengerCount"], "response":None}
        for result in results:
            details = {}
            details["TrainName"] = result[0]
            details["passengerCount"] = result[1]
            final_result.append(details)
        response["response"] = final_result
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



@app.route('/confirmed_passengers', methods=['POST', 'OPTIONS'])
def confirmed_passengers():
    try:
        data = request.json
        train_name = data.get('TrainName')
        if not train_name:
            return jsonify({"error": "Train name is required"}), 400
        final_result = []
        response = {"columns":["first_name", "last_name", "SSN"], "response":None}
        results = find_passengers_by_train(train_name)
        for result in results:
            details = {}
            details["first_name"] = result[0]
            details["last_name"] = result[1]
            details["SSN"] = result[2]
            final_result.append(details)
        response["response"] = final_result
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/deleted_passenger', methods=['POST', 'OPTIONS'])
def deleted_passenger():
    data = request.json
    passenger_ssn = data['Passenger_ssn']
    updated_passenger = cancel_ticket_and_update_waiting_list(passenger_ssn)
    return jsonify(updated_passenger)

if __name__ == '__main__':
    app.run(debug = True, port=5001)


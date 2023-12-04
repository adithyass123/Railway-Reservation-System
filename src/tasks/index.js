import apis from '../config';
import Task1 from './task1';
import Task2 from './task2';
import Task3 from './task3';
import Task4 from './task4';
import Task5 from './task5';
import Task6 from './task6';
import "./tasks.css";

function Railway() {
    return (
        <div className="App">
            <h1 className="text-center">Programming Assignment #4</h1>
            <h1 className="text-center">Railway Reservation System</h1>
            <Task1 endpoint={apis.booked_trains} />
            <Task2 endpoint={apis.confirmed_tickets} />
            <Task3 endpoint={apis.passengers_details} />
            <Task4 endpoint={apis.available_trains} />
            <Task5 endpoint={apis.confirmed_passengers} />
            <Task6 endpoint={apis.deleted_passenger} />
        </div>
    );
}

export default Railway;

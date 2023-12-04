import { useState } from "react";
import TableData from "../tableData";
import axios from "axios";

function Task3(props) {
  const [formData, setData] = useState({
    passenger_age: 50
  });

  const [columns, setColumns] = useState(['Train_Number', 'TrainName', 'source_station', 'destination_station', 'first_name', 'last_name', 'address', 'categories', 'Status'])
  const [passegersDetails, setPassengersDetails] = useState({Train_Number: '3',
    TrainName: 'Golden Arrow',
    source_station: 'Victoria',
    destination_station: 'Dover',
    first_name: 'Minna',
    last_name: 'Amigon',
    address: '2371 Jerrold Ave',
    categories: 'Montgomery',
    Status: 'Waitlist'
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setData({ ...formData, [name]: value, });
  };

  const getpassegersDetails = () => {
    axios.post(props.endpoint, {...formData})
    .then((response) => {
        const {columns, data} = response;
        setColumns(columns);
        setPassengersDetails(data)
    });
  };
  
  return (
    <div className="task-3 mt-20">
      <p>
        3. User input the age of the passenger (50 to 60) and UI display the train information (Train Number, Train Name, Source and Destination) and passenger information (Name, Address, Category, ticket status) of passengers who are between the ages of 50 to 60
      </p>
      <div className="form">
        <div className="form-fields">
          <label htmlFor="passenger_age">Passenger Age: {formData.passenger_age}</label>
          <input
            type="range"
            id="passenger_age"
            name="passenger_age"
            value={formData.passenger_age || ""}
            onChange={handleChange}
            min="50"
            max="60"
          />
        </div>
        <button
          className="button"
          disabled={!formData.passenger_age}
          onClick={getpassegersDetails}
        >
          Submit
        </button>
      </div>
      {columns.length > 0 && <TableData columns={columns} data={passegersDetails} />}
    </div>
  );
}

export default Task3;

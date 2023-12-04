import { useState } from "react";
import TableData from "../tableData";
import axios from "axios";

function Task1(props) {
  const [formData, setData] = useState({
    first_name: "",
    last_name: "",
  });
  const [columns, setColumns] = useState([
    "Train_Number",
    "TrainName",
    "Source",
    "Destination"
]);
  const [bookedTrains, setBookedTrains] = useState([
    {
        "Destination": "London",
        "Source": "Edinburgh",
        "TrainName": "Flying Scottsman",
        "Train_Number": 2
    },
    {
        "Destination": "Goa",
        "Source": "Bangalore",
        "TrainName": "Golden Chariot",
        "Train_Number": 4
    }
]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setData({ ...formData, [name]: value });
  };

  const getBookedTrains = () => {
    const config = {
      method: 'post',
      url: props.endpoint,
      headers: {
        'content-type': 'application/json', // Set the Content-Type header for JSON data
      },
      data: {...formData}
    };
    axios.request(config).then((response) => {
      const { columns, data } = response;
      setColumns(columns);
      setBookedTrains(data);
      console.log(response);
    }).catch(e => {
      console.log(e);
    });
  };

  return (
    <div className="task-1">
      <p>
        1. User input the passenger’s last name and first name and retrieve all
        trains they are booked on.
      </p>
      <div className="form">
        <div className="form-fields">
          <label htmlFor="first_name">First name:</label>
          <input
            type="text"
            id="first_name"
            name="first_name"
            value={formData.first_name || ""}
            onChange={handleChange}
          />
        </div>
        <div className="form-fields">
          <label htmlFor="last_name">Last name:</label>
          <input
            type="text"
            id="last_name"
            name="last_name"
            value={formData.last_name || ""}
            onChange={handleChange}
          />
        </div>
        <button
          className="button"
          disabled={formData.first_name.length === 0}
          onClick={getBookedTrains}
        >
          Submit
        </button>
      </div>
      {columns.length > 0 && (
        <TableData columns={columns} data={bookedTrains} />
      )}
    </div>
  );
}

export default Task1;

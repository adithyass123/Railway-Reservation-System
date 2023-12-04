import { useState } from "react";
import TableData from "../tableData";
import axios from "axios";

function Task2(props) {
  const [formData, setData] = useState({
    TrainDate: ''
  });
  const [columns, setColumns] = useState(["Passanger_ssn", "address",
  "first_name", "last_name", "city", "county", "phone", "bdate"])
  const [confirmedTickets, setConfirmedTickets] = useState([
        {
            "Passanger_ssn": 240471168,
            "first_name": "Josephine",
            "last_name": "Darakjy",
            "address": "4 B Blue Ridge Blvd",
            "city": "Brighton",
            "county": "Livingston",
            "phone": "810-374-9840",
            "bdate": "11/1/75",
        },
        {
            "Passanger_ssn": 317434088,
            "first_name": "Fletcher",
            "last_name": "Flosi",
            "address": "394 Manchester Blvd",
            "city": "Rockford",
            "county": "Winnebago",
            "phone": "815-426-5657",
            "bdate": "4/4/61",
        }
      ]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setData({ ...formData, [name]: value, });
  };

  const getConfirmedTickets = () => {
    axios.post(props.endpoint, { ...formData})
    .then((response) => {
        const {columns, data} = response;
        setColumns(columns);
        setConfirmedTickets(data)
    });
  };
  
  return (
    <div className="task-2 mt-20">
      <p>
        2. User input the Date and list of passengers travelling on entered day with confirmed tickets displays on UI.
      </p>
      <div className="form">
        <div className="form-fields">
          <label htmlFor="TrainDate">Train Date:</label>
          <input
            type="date"
            id="TrainDate"
            name="TrainDate"
            value={formData.TrainDate || ""}
            onChange={handleChange}
          />
        </div>
        <button
          className="button"
          disabled={!formData.TrainDate}
          onClick={getConfirmedTickets}
        >
          Submit
        </button>
      </div>
      {columns.length > 0 && <TableData columns={columns} data={confirmedTickets} />}
    </div>
  );
}

export default Task2;

import { useState } from "react";
import TableData from "../tableData";
import axios from "axios";

function Task6(props) {
  const [formData, setData] = useState({
    Passenger_ssn: null,
  });
  const [columns, setColumns] = useState([])
  const [passengerDetails, setPassengerDetails] = useState([]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setData({ ...formData, [name]: value, });
  };

  const getPassengerDetails = () => {
    axios.post(props.endpoint, ...formData).then((response) => {
        const { columns, data } = response;
        setColumns(columns);
        setPassengerDetails(data)
    });
  };
  
  return (
    <div className="task-6 mt-20">
      <p>6. User Cancel a ticket (delete a record) and show that passenger in waiting list get ticket confirmed.</p>
      <div className="form">
        <div className="form-fields">
          <label htmlFor="Passanger_ssn">Passenger SSN:</label>
          <input
            type="text"
            id="Passanger_ssn"
            name="Passanger_ssn"
            value={formData.Passanger_ssn || ""}
            onChange={handleChange}
          />
        </div>
        <button
          className="button"
          disabled={!formData.Passanger_ssn}
          onClick={getPassengerDetails}
        >
          Submit
        </button>
      </div>
      {columns.length > 0 && <TableData columns={columns} data={passengerDetails} />}
    </div>
  );
}

export default Task6;

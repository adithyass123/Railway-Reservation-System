import { useState } from "react";
import TableData from "../tableData";
import axios from "axios";

function Task5(props) {
  const [formData, setData] = useState({
    TrainName: "",
  });
  const [columns, setColumns] = useState(["SSN", "first_name", "last_name"]);
  const [confirmedPassengers, setConfirmedPassengers] = useState([
    {
      SSN: 240471168,
      first_name: "Josephine",
      last_name: "Darakjy",
    },
    {
      SSN: 317434088,
      first_name: "Fletcher",
      last_name: "Flosi",
    },
    {
      SSN: 310908858,
      first_name: "Sage",
      last_name: "Wieser",
    },
    {
      SSN: 322273872,
      first_name: "Kris",
      last_name: "Marrier",
    },
  ]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setData({ ...formData, [name]: value });
  };

  const getConfirmedPassengers = () => {
    axios.post(props.endpoint, { ...formData }).then((response) => {
      const { columns, data } = response;
      setColumns(columns);
      setConfirmedPassengers(data);
    });
  };

  return (
    <div className="task-5 mt-20">
      <p>
        5. Enter a train name and retrieve all the passengers with confirmed
        status travelling in that train.
      </p>
      <div className="form">
        <div className="form-fields">
          <label htmlFor="TrainName">Train name:</label>
          <input
            type="text"
            id="TrainName"
            name="TrainName"
            value={formData.TrainName || ""}
            onChange={handleChange}
          />
        </div>
        <button
          className="button"
          disabled={!formData.TrainName}
          onClick={getConfirmedPassengers}
        >
          Submit
        </button>
      </div>
      {columns.length > 0 && (
        <TableData columns={columns} data={confirmedPassengers} />
      )}
    </div>
  );
}

export default Task5;

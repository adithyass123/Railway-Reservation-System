import { useState } from "react";
import TableData from "../tableData";
import axios from "axios";

function Task4(props) {
  const [columns, setColumns] = useState([
    "TrainName",
    "passengerCount"
])
  const [availableTrains, setAvailableTrains] = useState([
    {
      "TrainName": "Flying Scottsman",
      "passengerCount": 5
  },
  {
      "TrainName": "Golden Arrow",
      "passengerCount": 6
  },
  {
      "TrainName": "Golden Chariot",
      "passengerCount": 10
  }
]);

  const getAvailableTrains = () => {
    axios.get(props.endpoint).then((response) => {
        const {columns, data} = response;
        setColumns(columns);
        setAvailableTrains(data)
    });
  };
  
  return (
    <div className="task-4 mt-20">
      <p>4. List all the train name along with count of passengers it is carrying.</p>
        <button
          className="button"
          onClick={getAvailableTrains}
        >
          Show Data
        </button>
      {columns.length > 0 && <TableData columns={columns} data={availableTrains} />}
    </div>
  );
}

export default Task4;

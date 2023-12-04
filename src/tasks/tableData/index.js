function Table(props) {
  const { columns, data } = props;

  return (
    <div className="table">
      <div className="table-content">
        {columns.length > 0 ? (
          <table id="table-data">
            <tr>
              {columns.map((column) => (
                <th key={column}>{column}</th>
              ))}
            </tr>
            {Array.isArray(data)
              ? data.map((colData, index) => {
                  return (
                    <tr key={colData + index}>
                      {Object.values(colData).map((col, index) => {
                        return <td key={col + index}>{col}</td>;
                      })}
                    </tr>
                  );
                })
              : Object.values(data).map((colData, index) => {
                  return <td key={colData + index}>{colData}</td>;
                })}
          </table>
        ) : (
          <p>No Data</p>
        )}
      </div>
    </div>
  );
}

export default Table;

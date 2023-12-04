let host;
if (!process.env.NODE_ENV || process.env.NODE_ENV === "development") {
  // demo APis
  host = " http://127.0.0.1:5001"
} else {
  host = "http://35.154.23.122:7873";
}

export default {
    booked_trains: `${host}/booked_tickets`,
    confirmed_tickets: `${host}/confirmed_tickets`,
    passengers_details: `${host}/passengers_in_age_range `,
    available_trains: `${host}/available_trains`,
    confirmed_passengers: `${host}/confirmed_passengers`,
    deleted_passenger: `${host}/deleted_passenger`
}
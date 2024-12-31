import React, { useState } from "react";
import FileUpload from "./FileUpload";
import CalendarView from "./CalendarView";

const Events = () => {
  const [events, setEvents] = useState([]);

  const handleParsedEvents = (parsedEvents) => {
    setEvents(parsedEvents);
  };

  return (
    <div>
      <FileUpload onEventsParsed={handleParsedEvents} />
      {events.length > 0 && <CalendarView events={events} />}
    </div>
  );
};

export default Events;

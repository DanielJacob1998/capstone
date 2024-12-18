// frontend/src/components/Sidebar.js
import React from "react";
import { Link } from "react-router-dom";
import "./Sidebar.css"; // Style as needed

const Sidebar = () => {
  return (
    <nav className="sidebar">
      <h2>Dashboard</h2>
      <ul>
        <li><Link to="/scanner">File Scanner</Link></li>
        <li><Link to="/finances">Finances</Link></li>
        <li><Link to="/events">Events</Link></li>
      </ul>
    </nav>
  );
};

export default Sidebar;


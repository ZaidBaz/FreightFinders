import React from "react";
import { FaSearch } from "react-icons/fa"; // Icon library for the search icon
import "frontend\src\Components\left-sidebar.css";

const Sidebar = () => {
  return (
    <div className="sidebar">
      <ul className="sidebar-list">
        <li className="sidebar-item">Home</li>
        <li className="sidebar-item">
          <FaSearch className="sidebar-icon" /> Search
        </li>
        <li className="sidebar-item">My Loads</li>
        <li className="sidebar-item">Fuel Savings</li>
        <li className="sidebar-item">Trailer Rental</li>
        <li className="sidebar-item">More</li>
      </ul>
    </div>
  );
};

export default Sidebar;

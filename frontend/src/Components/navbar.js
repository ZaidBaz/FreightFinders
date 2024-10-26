import React from "react";
import "frontend\src\Components\navbar.css"; // 
const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-left">
        <h1 className="brand">
          <span className="brand-primary">Schneider</span> <span className="brand-secondary">FreightPower</span>
        </h1>
        <a href="#search" className="search-link">Search Load #</a>
      </div>
      <div className="navbar-right">
        <p>Welcome, Pearl</p>
      </div>
    </nav>
  );
};

export default Navbar;

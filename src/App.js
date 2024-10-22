import React, { useState } from 'react';
import './App.css'; // Import the CSS for styling

const LoadSearch = () => {
  // State to manage selected capacity types
  const [selectedCapacity, setSelectedCapacity] = useState([]);
  // State to track the active section (New Search, Recent Search, etc.)
  const [activeSection, setActiveSection] = useState('New Search');
  const [origin, setOrigin] = useState('');
  const [destination, setDestination] = useState('');
  const [pickupDate, setPickupDate] = useState(''); // New state for pickup date
  const [dropoffDate, setDropoffDate] = useState(''); // New state for drop-off date
  const [minMiles, setMinMiles] = useState('');
  const [maxMiles, setMaxMiles] = useState('');

  const handleCapacityChange = (event) => {
    const value = event.target.value;
    setSelectedCapacity((prev) =>
      prev.includes(value) ? prev.filter((v) => v !== value) : [...prev, value]
    );
  };

  // Handle section change on horizontal navigation click
  const handleSectionClick = (section) => {
    setActiveSection(section);
  };

  const handleClear = () => {
    setSelectedCapacity([]);
    setOrigin('');
    setDestination('');
    setPickupDate('');
    setDropoffDate('');
    setMinMiles('');
    setMaxMiles('');
  };

  return (
    <div className="container">
      {/* Header Section */}
      <header className="header">
        <div className="horizontal-line"></div>
        <div className="header-content">
          <h1 className="header-title">
            <span className="header-title-orange">Schneider</span>
            <br />
            <span className="header-title-black">FreightPower</span>
          </h1>
        </div>
      </header>

      {/* Left Sidebar Section */}
      <aside className="left-sidebar">
        <div className="sidebar-item">
          <img src="house-drawing.png" className="sidebar-icon" alt="Home Icon" />
          <span></span>
        </div>
        <div className="sidebar-item"><span>Search</span></div>
        <div className="sidebar-item"><span>My Loads</span></div>
        <div className="sidebar-item manage-capacity">
          <span>Manage</span>
          <span className="sidebar-subtitle">Capacity</span>
        </div>
        <div className="sidebar-item"><span>Fuel Savings</span></div>
        <div className="sidebar-item trailer-rental">
          <span>Trailer</span>
          <span className="sidebar-subtitle">Rental</span>
        </div>
        <div className="sidebar-item more-option">
          <span>More</span>
          <div className="more-icon">
            <span className="circle"></span>
            <span className="circle"></span>
            <span className="circle"></span>
          </div>
        </div>
      </aside>

      {/* Right Sidebar Section */}
      <aside className="right-sidebar">
        <h2 className="right-sidebar-title">Top Recommendations</h2>
        <div className="right-sidebar-content">
          <div className="recommendation-box">
            <strong>From GREEN-BAY, WI</strong>
            <p>Nov 22 6:00am - 7:30am</p>
            <p>Drop Empty Trailer</p>
            <p>Pick Up Loaded Trailer</p>
            <div className="spacer"></div> {/* Space between sections */}
            <strong>To MADISON, WI</strong>
            <p>Dec 22 9:30am - 11:30am</p>
            <p>Drop Loaded Trailer</p>
            <p>Pick Up Empty Trailer</p>
            <button className="contact-button">Contact to Book</button>
          </div>
          <div className="recommendation-box">
            <strong>From CHICAGO, IL</strong>
            <div className="spacer"></div>
            <strong>To GLENVIEW, IL</strong>
            <button className="contact-button">More Details</button>
          </div>
        </div>
      </aside>




      {/* Main Content Section */}
      <main className="main-content">
        {/* Horizontal Sidebar Section */}
        <div className="horizontal-sidebar">
          <button
            className={`horizontal-btn ${activeSection === 'New Search' ? 'active' : ''}`}
            onClick={() => handleSectionClick('New Search')}
          >
            New Search
          </button>
          <button
            className={`horizontal-btn ${activeSection === 'Recent Search' ? 'active' : ''}`}
            onClick={() => handleSectionClick('Recent Search')}
          >
            Recent Search
          </button>
          <button
            className={`horizontal-btn ${activeSection === 'Favorite Search' ? 'active' : ''}`}
            onClick={() => handleSectionClick('Favorite Search')}
          >
            Favorite Search
          </button>
          <button
            className={`horizontal-btn ${activeSection === 'Watched Loads' ? 'active' : ''}`}
            onClick={() => handleSectionClick('Watched Loads')}
          >
            Watched Loads
          </button>
        </div>

        {/* Conditionally render based on the active section */}
        {activeSection === 'New Search' && (
          <div>
            <form className="search-form">
              <div className="form-left">
                <label htmlFor="capacity-type" className="form-label">Capacity Type</label>
                <div className="checkbox-group">
                  {['power-only', 'dry-van', 'dray', 'refrigerated', 'specialty'].map((capacity) => (
                    <div key={capacity} className="checkbox-item">
                      <input
                        type="checkbox"
                        id={capacity}
                        value={capacity}
                        onChange={handleCapacityChange}
                        checked={selectedCapacity.includes(capacity)}
                      />
                      <label htmlFor={capacity}>{capacity.replace('-', ' ').toUpperCase()}</label>
                    </div>
                  ))}
                </div>

                {/* Origin and Pickup Date Group */}
                <div className="input-group">
                  <label htmlFor="origin" className="form-label">Origin</label>
                  <input
                    type="text"
                    id="origin"
                    placeholder="Enter origin"
                    value={origin}
                    onChange={(e) => setOrigin(e.target.value)}
                  />
                  <label htmlFor="pickup-date" className="form-label">Pickup Date</label>
                  <input
                    type="date"
                    id="pickup-date"
                    value={pickupDate}
                    onChange={(e) => setPickupDate(e.target.value)}
                  />
                </div>

                {/* Destination and Drop-off Date Group */}
                <div className="input-group">
                  <label htmlFor="destination" className="form-label">Destination</label>
                  <input
                    type="text"
                    id="destination"
                    placeholder="Enter destination"
                    value={destination}
                    onChange={(e) => setDestination(e.target.value)}
                  />
                  <label htmlFor="dropoff-date" className="form-label">Drop-off Date</label>
                  <input
                    type="date"
                    id="dropoff-date"
                    value={dropoffDate}
                    onChange={(e) => setDropoffDate(e.target.value)}
                  />
                </div>
              </div>

              <div className="form-right">
                <div className="miles-section">
                  <h2>Miles to be travelled</h2>
                  <div className="miles-inputs">
                    <div>
                      <label htmlFor="minMiles">Minimum</label>
                      <input
                        type="number"
                        id="minMiles"
                        placeholder="Min miles"
                        value={minMiles}
                        onChange={(e) => setMinMiles(e.target.value)}
                      />
                    </div>
                    <div>
                      <label htmlFor="maxMiles">Maximum</label>
                      <input
                        type="number"
                        id="maxMiles"
                        placeholder="Max miles"
                        value={maxMiles}
                        onChange={(e) => setMaxMiles(e.target.value)}
                      />
                    </div>
                  </div>
                </div>
              </div>

              <div className="form-bottom">
                <button type="button" className="clear-btn" onClick={handleClear}>Clear</button>
                <button type="button" className="favorite-btn"><strong>Favorite</strong></button>
                <button type="submit" className="search-btn">Search</button>
              </div>
            </form>
          </div>
        )}

        {activeSection === 'Recent Search' && (
          <div className="recent-search-section">
            <h2>Recent Searches</h2>
            {/* Placeholder content for Recent Search */}
            <ul>
              <li>Search 1 - [Origin -> Destination]</li>
              <li>Search 2 - [Origin -> Destination]</li>
              <li>Search 3 - [Origin -> Destination]</li>
            </ul>
          </div>
        )}

        {activeSection === 'Favorite Search' && (
          <div className="favorite-search-section">
            <h2>Favorite Searches</h2>
            {/* Placeholder content for Favorite Search */}
            <ul>
              <li>Favorite Search 1</li>
              <li>Favorite Search 2</li>
              <li>Favorite Search 3</li>
            </ul>
          </div>
        )}

        {activeSection === 'Watched Loads' && (
          <div className="watched-loads-section">
            <h2>Watched Loads</h2>
            {/* Placeholder content for Watched Loads */}
            <ul>
              <li>Load 1 - [Details]</li>
              <li>Load 2 - [Details]</li>
              <li>Load 3 - [Details]</li>
            </ul>
          </div>
        )}
      </main>
    </div>
  );
};

export default LoadSearch;
import React, { useState } from 'react';
import './App.css'; 

import Navbar from './Components/Navbar/Navbar.js';
import Button from './Components/Button/Button.js';
import Search from './Components/Search/Search.js';
import LeftSidebar from './Components/LeftSidebar/LeftSidebar.js';
import Dropdown from './Components/Dropdown/Dropdown.js';
import Card from './Components/Card'; // Import the Card component

const App = () => {
  // State to toggle sidebar visibility
  const [isSidebarVisible, setIsSidebarVisible] = useState(true);

  // State to track which button is active
  const [activeButton, setActiveButton] = useState(null);

  // State for tracking the selected menu item in the sidebar
  const [selectedMenuItem, setSelectedMenuItem] = useState(null);

  // Define states
  const [selectedCapacity, setSelectedCapacity] = useState([]); // Ensure this is defined
  const [origin, setOrigin] = useState(''); // Define the origin state
  const [destination, setDestination] = useState(''); // Define the destination state
  const [pickupDate, setPickupDate] = useState(''); // Define the pickup date state
  const [dropoffDate, setDropoffDate] = useState(''); // Define the dropoff date state
  const [minMiles, setMinMiles] = useState(''); // Define the min miles state
  const [maxMiles, setMaxMiles] = useState(''); // Define the max miles state
  const [results, setResults] = useState([]); // Define results state

  // Handler for toggling sidebar visibility
  const toggleSidebar = () => {
    setIsSidebarVisible((prevState) => !prevState);
  };

  // Handler to set the active button
  const handleButtonClick = (buttonIndex) => {
    setActiveButton(buttonIndex);
  };

  

  // Handler for selecting a menu item in the sidebar
  const handleMenuItemClick = (item) => {
    setSelectedMenuItem(item);
  };

  // Handle clear button
  const handleClear = () => {
    setSelectedCapacity([]);
    setOrigin('');
    setDestination('');
    setPickupDate('');
    setDropoffDate('');
    setMinMiles('');
    setMaxMiles('');
  };

  // Handle Search Button
  const handleSearch = async (event) => {
    event.preventDefault();
    const searchData = {
        origin_city: origin,
        destination_city: destination,
        earliest_start_date: pickupDate,
        latest_start_date: dropoffDate,
        transport_modes: selectedCapacity.join(','),  // Convert array to comma-separated string
      };
      console.log("HIPearl", searchData)
      const queryParams = new URLSearchParams(searchData).toString();


      try {
            // Send data to the backend (Django)
            const response = await fetch(`http://127.0.0.1:8000/filter-loads/?${queryParams}`, {
              method: 'GET',
              // headers: {
              //   'Content-Type': 'application/json',
              // },
              // body: JSON.stringify(searchData),
      });


      const result = await response.json();
            console.log('API Response:', result);
      setResults(result); // Set the search results from backend response
    } catch (error) {
      console.error('Errors during search from Backend:', error);
    }
  };



  return (
    <div className="app">
      {/* Navbar component with a toggle button */}
      <Navbar toggleSidebar={toggleSidebar} />

      {/* Main content with conditional Left Sidebar rendering */}
      <div className="main-content">
        <div className="button-container">
          {["New Search", "Recent Search", "Favorite Search", "Watched Loads", "Rec. Loads"].map((label, index) => (
            <Button 
              key={index}
              label={label}
              onClick={() => handleButtonClick(index)}
              isActive={activeButton === index} // Pass the active state to the button
            />
          ))}
        </div>

        {isSidebarVisible && (
          <LeftSidebar
            selectedMenuItem={selectedMenuItem}
            onMenuItemClick={handleMenuItemClick}
          />
        )}

        {/* White box container for the Card */}
        <div className="card-container">
          <h2 className="card-title">Top Recommendations</h2>
          <Card />
          <Card />
        </div>

        <div className="search-filter-container">
          <div className='dropdown-container'>
            <h3 className="dropdown-title">Select an Option:</h3>
            <Dropdown
             setSelectedCapacity= {setSelectedCapacity}
             selectedCapacity={selectedCapacity}/>
          </div>
          {/* Origin and Pickup Date Group */}
          <div className="input-group">
            <div className="input-row">
              <label htmlFor="origin" className="form-label">Origin</label>
              <input
                type="text"
                id="origin"
                placeholder="origin"
                value={origin}
                onChange={(e) => setOrigin(e.target.value)}
              />
            </div>
            <div className="input-row">
              <input
                type="date"
                id="pickup-date"
                value={pickupDate}
                onChange={(e) => setPickupDate(e.target.value)}
              />
            </div>
          </div>

          {/* Destination and Drop-off Date Group */}
          <div className="input-group">
            <div className="input-row">
              <label htmlFor="destination" className="form-label">Destination</label>
              <input
                type="text"
                id="destination"
                placeholder="destination"
                value={destination}
                onChange={(e) => setDestination(e.target.value)}
              />
            </div>
            <div className="input-row">
              <input
                type="date"
                id="dropoff-date"
                value={dropoffDate}
                onChange={(e) => setDropoffDate(e.target.value)}
              />
            </div>
          </div>

          <div className="button-container-2">
            <Search
              label="Search"
              onClick={handleSearch} // Updated to the correct function name
              isActive={activeButton === 0} // Assuming activeButton is used for state tracking
            />
          </div>

          {results.length > 0 && (
                      <div className="results-section">
                        <h2>Search Results</h2>
                        <ul>
                          {results.map((result, index) => (
                            <li key={index}>
                              <strong>From {result.load_stops[0]?.city} to {result.load_stops[result.load_stops.length - 1]?.city}</strong>
                              <p>LOAD ID: {result.load_id}, TRANSPORT MODE: {result.transport_mode}</p>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}


        </div>
      </div>
    </div>
  );
};

export default App;

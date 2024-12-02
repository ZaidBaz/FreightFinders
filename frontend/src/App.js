import React, { useState } from 'react';
import './App.css'; 
import Navbar from './Components/Navbar/Navbar.js';
import Button from './Components/Button/Button.js';
import Search from './Components/Search/Search.js';
import LeftSidebar from './Components/LeftSidebar/LeftSidebar.js';
import Dropdown from './Components/Dropdown/Dropdown.js';
import Card from './Components/Card';
import Checkbox from './Components/Checkbox/Checkbox';
import CustomSlider from './Components/CustomSlider/CustomSlider';
import CityAutoComplete from './Components/Autofill/CityAutoComplete';
import ClearButton from './Components/ClearButton/ClearButton';

const App = () => {
  const [isSidebarVisible, setIsSidebarVisible] = useState(true);
  const [activeButton, setActiveButton] = useState(null);
  const [selectedMenuItem, setSelectedMenuItem] = useState(null);
  const [selectedCapacity, setSelectedCapacity] = useState([]);
  const [origin, setOrigin] = useState('');
  const [origin_lat_lon_zip, setOriginLatLonZip] = useState(null);
  const [destination, setDestination] = useState('');
  const [destination_lat_lon_zip, setDestinationLatLonZip] = useState(null);
  const [earliestPickupDate, setEarliestPickupDate] = useState('');
  const [latestPickupDate, setLatestPickupDate] = useState('');
  const [destinationStartDate, setDestinationStartDate] = useState('');
  const [destinationEndDate, setDestinationEndDate] = useState('');
  const [maxMiles, setMaxMiles] = useState(100);
  const [originRadius, setOriginRadius] = useState(25);
  const [destinationRadius, setDestinationRadius] = useState(25);
  const [results, setResults] = useState([]);

  // **Added state variables for the checkboxes**
  const [originAnywhereChecked, setOriginAnywhereChecked] = useState(false);
  const [destinationAnywhereChecked, setDestinationAnywhereChecked] = useState(false);

  const toggleSidebar = () => setIsSidebarVisible((prevState) => !prevState);
  const handleButtonClick = (buttonIndex) => setActiveButton(buttonIndex);

  // Clear functions
  const clearCapacityTypes = () => setSelectedCapacity([]);

  const clearOrigin = () => {
    setOrigin('');
    setOriginLatLonZip(null);
    setEarliestPickupDate('');
    setLatestPickupDate('');
    setOriginRadius(25);
    setOriginAnywhereChecked(false); // Reset the origin checkbox
  };

  const clearDestination = () => {
    setDestination('');
    setDestinationLatLonZip(null);
    setDestinationStartDate('');
    setDestinationEndDate('');
    setDestinationRadius(25);
    setDestinationAnywhereChecked(false); // Reset the destination checkbox
  };

  const handleClear = () => {
    clearCapacityTypes();
    clearOrigin();
    clearDestination();
    setMaxMiles(100);
  };

  const handleSearch = async (event) => {
    event.preventDefault();
    const searchData = {
      origin: origin,
      origin_full_addr: JSON.stringify(origin_lat_lon_zip),
      destination: destination,
      destination_full_addr: JSON.stringify(destination_lat_lon_zip),
      earliest_start_date: earliestPickupDate,
      latest_start_date: latestPickupDate,
      earliest_end_date: destinationStartDate,
      latest_end_date: destinationEndDate,
      transport_modes: selectedCapacity.join(','),
      origin_radius: originRadius,
      destination_radius: destinationRadius,
      min_distance: 0,
      max_distance: maxMiles
    };

    const queryParams = new URLSearchParams(searchData).toString();

    try {
      const response = await fetch(`http://127.0.0.1:8000/filter-loads/?${queryParams}`, { method: 'GET' });
      const result = await response.json();
      setResults(result);
    } catch (error) {
      console.error('Errors during search from Backend:', error);
    }
  };

  return (
    <div className="app">
      <Navbar toggleSidebar={toggleSidebar} />
      <div className="main-content">
        <div className="button-container">
          {["New Search", "Recent Search", "Favorite Search", "Watched Loads", "Rec. Loads"].map((label, index) => (
            <Button 
              key={index}
              label={label}
              onClick={() => handleButtonClick(index)}
              isActive={activeButton === index}
            />
          ))}
        </div>

        {isSidebarVisible && (
          <LeftSidebar
            selectedMenuItem={selectedMenuItem}
            onMenuItemClick={(item) => setSelectedMenuItem(item)}
          />
        )}

        {/* Top Recommendations Section */}
        <div className="card-container">
          <h2 className="card-title">Top Recommendations</h2>
          <Card loadId="1000534119" transportMode="Power Only" originCity="GREEN BAY, WI" destinationCity="GLENVIEW, IL" totalDistance="189" totalWeight="22000" />
          <Card loadId="1000534120" transportMode="Power Only" originCity="MILWAUKEE, WI" destinationCity="CHICAGO, IL" totalDistance="94" totalWeight="25000" />
        </div>

        <div className="search-results-wrapper">
          {/* Search Filter and Results Section */}
          <div className="search-filter-container">
            {/* Capacity Type Section */}
            <div className="dropdown-container">
              <div className="section-header">
                <h3 className="dropdown-title">Capacity Type</h3>
                <ClearButton onClick={clearCapacityTypes} label="Reset" />
              </div>
              <Dropdown setSelectedCapacity={setSelectedCapacity} selectedCapacity={selectedCapacity} />
            </div>

            {/* Origin and Pickup Date Group */}
            <div className="input-group">
              <div className="section-header">
                <label htmlFor="origin" className="form-label">Origin</label>
                <ClearButton onClick={clearOrigin} label="Reset" />
              </div>
              <div className="input-row">
                <CityAutoComplete
                  query={origin}
                  setQuery={setOrigin}
                  queryLatLonZip={origin_lat_lon_zip}
                  setQueryLatLonZip={setOriginLatLonZip}
                />
                <Checkbox
                  label="Anywhere"
                  checked={originAnywhereChecked} // Bind checked state
                  onChange={(e) => {
                    setOriginAnywhereChecked(e.target.checked);
                    if (e.target.checked) {
                      setOrigin('Anywhere');
                      setOriginLatLonZip(null);
                    } else {
                      setOrigin('');
                    }
                  }}
                />
              </div>
              <div className="input-row-second">
                <input
                  type="date"
                  id="earliest-pickup-date"
                  value={earliestPickupDate}
                  onChange={(e) => setEarliestPickupDate(e.target.value)}
                />
                <input
                  type="date"
                  id="latest-pickup-date"
                  value={latestPickupDate}
                  onChange={(e) => setLatestPickupDate(e.target.value)}
                />
              </div>
            </div>

            <div className="input-group">
              <CustomSlider
                label="Origin location radius"
                min="25"
                max="250"
                step="25"
                defaultSliderVal="25"
                inputValue={originRadius}
                setInputValue={setOriginRadius}
              />
            </div>

            {/* Destination and Destination Date Range Group */}
            <div className="input-group">
              <div className="section-header">
                <label htmlFor="destination" className="form-label">Destination</label>
                <ClearButton onClick={clearDestination} label="Reset" />
              </div>
              <div className="input-row">
                <CityAutoComplete
                  query={destination}
                  setQuery={setDestination}
                  queryLatLonZip={destination_lat_lon_zip}
                  setQueryLatLonZip={setDestinationLatLonZip}
                />
                <Checkbox
                  label="Anywhere"
                  checked={destinationAnywhereChecked} // Bind checked state
                  onChange={(e) => {
                    setDestinationAnywhereChecked(e.target.checked);
                    if (e.target.checked) {
                      setDestination('Anywhere');
                      setDestinationLatLonZip(null);
                    } else {
                      setDestination('');
                    }
                  }}
                />
              </div>
              <div className="input-row-second">
                <input
                  type="date"
                  id="destination-start-date"
                  placeholder="Start Date"
                  value={destinationStartDate}
                  onChange={(e) => setDestinationStartDate(e.target.value)}
                />
                <input
                  type="date"
                  id="destination-end-date"
                  placeholder="End Date"
                  value={destinationEndDate}
                  onChange={(e) => setDestinationEndDate(e.target.value)}
                />
              </div>
            </div>

            <div className="input-group">
              <CustomSlider
                label="Drop off location radius"
                min="25"
                max="250"
                step="25"
                defaultSliderVal="25"
                inputValue={destinationRadius}
                setInputValue={setDestinationRadius}
              /> 
            </div>

            {/* Miles to be travelled Section */}
            <div className="input-group">
              <div className="section-header">
                <label htmlFor="distance" className="form-label">Miles to be travelled</label>
                {/* Optional: Add a reset button if needed */}
                {/* <ClearButton onClick={() => setMaxMiles(100)} label="Reset" /> */}
              </div>
            </div>

            <div className="input-group">
              <CustomSlider
                min="100"
                max="1000"
                step="100"
                defaultSliderVal="100"
                inputValue={maxMiles}
                setInputValue={setMaxMiles}
              />
            </div>

            <div className="button-container-2">
              <Search label="Search" onClick={handleSearch} isActive={activeButton === 0} />
            </div>
          </div>

          {/* Search Results Section */}
          <div className="results-section">
            <h2>Search Results</h2>
            <div className="results-card-container">
              {results.length > 0 ? (
                results.map((result, index) => (
                  <Card
                    key={index}
                    loadId={result.load_id}
                    transportMode={result.transport_mode}
                    originCity={result.load_stops[0]?.city}
                    destinationCity={result.load_stops[result.load_stops.length - 1]?.city}
                    totalDistance={result.total_distance}
                    totalWeight={result.total_weight}
                  />
                ))
              ) : (
                <p>No search results found.</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;

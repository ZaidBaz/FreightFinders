import React, { useState } from 'react';
import './App.css'; 
import Navbar from './Components/Navbar/Navbar.js';
import Button from './Components/Button/Button.js';
import Search from './Components/Search/Search.js';
import LeftSidebar from './Components/LeftSidebar/LeftSidebar.js';
import Dropdown from './Components/Dropdown/Dropdown.js';
import Card from './Components/Card';
import Checkbox from './Components/Checkbox/Checkbox';
import RadiusSlider from './Components/RadiusSlider/RadiusSlider';
import CustomSlider from './Components/CustomSlider/CustomSlider';
import CityAutoComplete from './Components/Autofill/CityAutoComplete';

const App = () => {
  const [isSidebarVisible, setIsSidebarVisible] = useState(true);
  const [activeButton, setActiveButton] = useState(null);
  const [selectedMenuItem, setSelectedMenuItem] = useState(null);
  const [selectedCapacity, setSelectedCapacity] = useState([]);
  const [origin, setOrigin] = useState('');
  const [destination, setDestination] = useState('');
  const [earliestPickupDate, setEarliestPickupDate] = useState('');
  const [latestPickupDate, setLatestPickupDate] = useState('');
  const [dropoffDate, setDropoffDate] = useState('');
  const [destinationStartDate, setDestinationStartDate] = useState(''); // Destination start date
  const [destinationEndDate, setDestinationEndDate] = useState(''); // Destination end date
  const [minMiles, setMinMiles] = useState('');
  const [maxMiles, setMaxMiles] = useState('');
  const [originRadius, setOriginRadius] = useState(250);
  const [destinationRadius, setDestinationRadius] = useState(250);
  const [results, setResults] = useState([]); // State for search results

  const toggleSidebar = () => setIsSidebarVisible((prevState) => !prevState);
  const handleButtonClick = (buttonIndex) => setActiveButton(buttonIndex);

  const handleClear = () => {
    setSelectedCapacity([]);
    setOrigin('');
    setDestination('');
    setEarliestPickupDate('');
    setLatestPickupDate('');
    setDropoffDate('');
    setDestinationStartDate('');
    setDestinationEndDate('');
    setMinMiles('');
    setMaxMiles('');
  };


  const handleSearch = async (event) => {
    event.preventDefault();
    const searchData = {
      origin_city: origin,
      destination_city: destination,
      earliest_start_date: earliestPickupDate,
      latest_start_date: dropoffDate,
      destination_start_date: destinationStartDate,
      destination_end_date: destinationEndDate,
      transport_modes: selectedCapacity.join(','),
      origin_radius: originRadius,
      destination_radius: destinationRadius,
      max_distance: maxMiles
    };

    const queryParams = new URLSearchParams(searchData).toString();

    try {
      const response = await fetch(`http://127.0.0.1:8000/filter-loads/?${queryParams}`, { method: 'GET' });
      const result = await response.json();
      console.log('API Response:', result); // Log the response to confirm
      setResults(result); // Set the search results
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

        <div className = "search-results-wrapper">
          {/* Search Filter and Results Section */}
          <div className="search-filter-container">
            <div className="dropdown-container">
              <h3 className="dropdown-title">Capacity Type:</h3>
              <Dropdown setSelectedCapacity={setSelectedCapacity} selectedCapacity={selectedCapacity} />
            </div>

            {/* Origin and Pickup Date Group */}
            <div className="input-group">
              <div className="input-row">
                <label htmlFor="origin" className="form-label">Origin</label>
                <CityAutoComplete onCitySelect={(city) => setOrigin(city)} />
                <Checkbox label="Anywhere" onClick={(e) => e.target.checked ? setOrigin('Anywhere') : null} />
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
              <CustomSlider label = "Origin location radius" min = "25" max = "250" step = "25" defaultSliderVal = "25" setInputValue={setOriginRadius}/>
            </div>

            {/* Destination and Destination Date Range Group */}
            <div className="input-group">
              <div className="input-row">
                <label htmlFor="destination" className="form-label">Destination</label>
                <CityAutoComplete onCitySelect={(city) => setDestination(city)} />
                <Checkbox label="Anywhere" onClick={(e) => e.target.checked ? setDestination('Anywhere') : null} />
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
              <CustomSlider label = "Drop off location radius" min = "25" max = "250" step = "25" defaultSliderVal = "25" setInputValue={setDestinationRadius}/> 
            </div>

            <div className = "input-group">
              <div className = "input-row">
                <label htmlFor = "distance" className = "form-label">Miles to be travelled</label>
              </div>
            </div>

            <div className = "input-group">
              <CustomSlider min = "100" max = "1000" step = "100" defaultSliderVal = "100" setInputValue={setMaxMiles}/>
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
        {/* </div> */}
      </div>
    </div>
  );
};

export default App;

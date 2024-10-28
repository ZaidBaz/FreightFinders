import React, { useState } from 'react';
import './App.css'; // Import the CSS for styling

// Import components
import Navbar from './Components/Navbar/Navbar.js';
import Button from './Components/Button/Button.js';
import LeftSidebar from './Components/LeftSidebar/LeftSidebar.js';
import Dropdown from './Components/Dropdown/Dropdown.js'
import Card from './Components/Card'; // Import the Card component

const App = () => {
  // State to toggle sidebar visibility
  const [isSidebarVisible, setIsSidebarVisible] = useState(true);

  // State to track which button is active
  const [activeButton, setActiveButton] = useState(null);

  // State for tracking the selected menu item in the sidebar
  const [selectedMenuItem, setSelectedMenuItem] = useState(null);

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
          <Card />
          <Card/>
        </div>

        <div className = "search-filter-container">
          <Dropdown />
        </div>
      </div>
    </div>
  );
};

export default App;

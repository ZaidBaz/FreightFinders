import React, { useState } from 'react';
import './App.css'; // Import the CSS for styling

// Import components
import Navbar from './Components/Navbar/Navbar.js';
import Button from './Components/Button/Button.js';
import LeftSidebar from './Components/LeftSidebar/LeftSidebar.js';
// import RightSidebar from './Components/RightSidebar/RightSidebar.js';

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
          {["New Search", "Recent Search", "Favorite Search", "Watched Loads","Rec. Loads"].map((label, index) => (
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

      
      </div>
    </div>
  );
};

export default App;


// // import RightSidebar from './Components/RightSidebar/RightSidebar';


// const App = () => {
//   // State for search results
//   const [searchResults, setSearchResults] = useState([
//     {
//       id: '1000534132',
//       startLocation: 'GREEN BAY, WI',
//       endLocation: 'MILWAUKEE, WI',
//       date: 'Sep 30, 7:00am - 5:00pm',
//       details: 'Drop Empty Trailer, Pick Up Loaded Trailer',
//       distance: 'Deadhead 0 mi',
//       watched: false
//     },
//     {
//       id: '1000534119',
//       startLocation: 'GREEN BAY, WI',
//       endLocation: 'MILWAUKEE, WI',
//       date: 'Sep 30, 9:28am - 9:28am',
//       details: 'Drop Relay, Pick Up Empty Trailer',
//       distance: 'Deadhead 0 mi',
//       watched: false
//     }
//   ]);

//   // State for filter options
//   const [pickupDate, setPickupDate] = useState('');
//   const [distance, setDistance] = useState(0);

//   // Handler for updating pickup date
//   const handleDateChange = (newDate) => {
//     setPickupDate(newDate);
//     // Could trigger a filtered search based on the selected date here
//   };

//   // Handler for updating distance
//   const handleDistanceChange = (newDistance) => {
//     setDistance(newDistance);
//     // Could filter search results based on distance here
//   };

//   // Handler for toggling watch status
//   const toggleWatch = (id) => {
//     setSearchResults((prevResults) =>
//       prevResults.map((result) =>
//         result.id === id ? { ...result, watched: !result.watched } : result
//       )
//     );
//   };

//   return (
//     <div className="app">
//       {/* Navbar component */}
//       <Navbar />

//       {/* Main content with left sidebar, content area, and right sidebar */}
//       <div className="main-content">
//         {/* Left Sidebar component */}
//         <LeftSidebar />

//         {/* Central Content Area */}
//         <div className="content">
//           {/* Search Options */}
//           <div className="search-options">
//             <Button label="New Search" active />
//             <Button label="Recent Search" />
//             <Button label="Favorite Search" />
//             <Button label="Watched Loads" />
//             <Button label="Rec. Loads" />
//           </div>

//           {/* Search Results */}
//           <div className="search-results">
//             {/* Filter bar with Dropdown and Distance Scrollbar */}
//             <div className="filter-bar">
//               <DropdownMenu label="Pick-Up Date" onChange={handleDateChange} />
//               <DistanceScrollbar onChange={handleDistanceChange} />
//             </div>

//             {/* List of Search Results */}
//             {searchResults.map((result) => (
//               <div key={result.id} className="search-result-item">
//                 <div className="route-info">
//                   <p><strong>{result.startLocation}</strong> to <strong>{result.endLocation}</strong></p>
//                   <p>{result.date}</p>
//                   <p>{result.details}</p>
//                   <p>{result.distance}</p>
//                 </div>
//                 <Button label="Contact to Book" />
//                 <button onClick={() => toggleWatch(result.id)}>
//                   {result.watched ? 'Unwatch' : 'Watch'}
//                 </button>
//               </div>
//             ))}
//           </div>
//         </div>

//         {/* Right Sidebar component
//         <RightSidebar /> */}
//       </div>
//     </div>
//   );
// // };

// export default App;



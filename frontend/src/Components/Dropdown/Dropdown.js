import React, { useState } from 'react';
import './Dropdown.css';

const Dropdown = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedOptions, setSelectedOptions] = useState({
    dray: false,
    dryVan: false,
    refrigerated:false,
    powerOnly: false,
    speciality: false,
  });

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const handleCheckboxChange = (option) => {
    setSelectedOptions(prevState => ({
      ...prevState,
      [option]: !prevState[option],
    }));
  };

  return (
    <div className="dropdown">
      <div className="dropdown-header" onClick={toggleDropdown}>
        <span className="dropdown-text">Select capacity types to search</span>
        <span className="dropdown-arrow">{isOpen ? '▲' : '▼'}</span>
      </div>
      {isOpen && (
        <div className="dropdown-menu">
          <label>
            <input
              type="checkbox"
              checked={selectedOptions.dray}
              onChange={() => handleCheckboxChange('dray')}
            />
            Dray
          </label>
          <label>
            <input
              type="checkbox"
              checked={selectedOptions.powerOnly}
              onChange={() => handleCheckboxChange('powerOnly')}
            />
            Power Only
          </label>
          <label>
            <input
              type="checkbox"
              checked={selectedOptions.dryVan}
              onChange={() => handleCheckboxChange('dryVan')}
            />
            Dry Van
          </label>
          <label>
            <input
              type="checkbox"
              checked={selectedOptions.refrigerated}
              onChange={() => handleCheckboxChange('refrigerated')}
            />
            Refrigerated
          </label>
          <label>
            <input
              type="checkbox"
              checked={selectedOptions.speciality}
              onChange={() => handleCheckboxChange('speciality')}
            />
            Speciality
          </label>
        </div>
      )}
    </div>
  );
};

export default Dropdown;

import React, { useState } from 'react';
import './Dropdown.css';

const Dropdown = ({ setSelectedCapacity, selectedCapacity }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const handleCapacityChange = (event) => {
    const value = event.target.value;
    setSelectedCapacity((prev) =>
      prev.includes(value) ? prev.filter((v) => v !== value) : [...prev, value]
    );
  };

  return (
    <div className="dropdown">
      <div className="dropdown-header" onClick={toggleDropdown}>
        <span className="dropdown-text">Select capacity types to search</span>
        <span className="dropdown-arrow">{isOpen ? '▲' : '▼'}</span>
      </div>
      {isOpen && (
        <div className="dropdown-content">
          {['power only', 'dry van', 'dray', 'refrigerated', 'specialty'].map((capacity) => (
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
      )}
    </div>
  );
};

export default Dropdown;
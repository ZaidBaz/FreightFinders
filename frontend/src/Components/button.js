import React, { useState } from 'react';

const SimpleButton = ({ label, onClick }) => {
  const [isHovered, setIsHovered] = useState(false);
  const [isActive, setIsActive] = useState(false);

  return (
    <button
      onClick={onClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onMouseDown={() => setIsActive(true)}
      onMouseUp={() => setIsActive(false)}
      style={{
        padding: '10px 20px',
        fontSize: '16px',
        color: '#000',
        backgroundColor: isHovered ? '#FFA07A' : '#CFCFCF', // Faded orange on hover
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        transition: 'background-color 0.3s ease',
        position: 'relative',
        // Adds the orange line on the left when active
        boxShadow: isActive ? 'inset 5px 0 0 #FFA500' : 'none',
      }}
    >
      {label}
    </button>
  );
};

export default SimpleButton;

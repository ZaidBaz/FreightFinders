import React from 'react';
import './ClearButton.css';

const ClearButton = ({ onClick, label }) => {
  return (
    <button className="reset-button" onClick={onClick}>
      {label}
    </button>
  );
};

export default ClearButton;

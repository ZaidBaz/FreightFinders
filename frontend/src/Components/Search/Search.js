// Button.js
import React from 'react';
import './Search.css';

const Button = ({ label, onClick, isActive }) => {
  return (
    <button
      className={`custom-search-button ${isActive ? 'active' : ''}`}
      onClick={onClick}
    >
      {label}
    </button>
  );
};

export default Button;

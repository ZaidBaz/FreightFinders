// Button.js
import React from 'react';
import './Button.css';

const Button = ({ label, onClick, isActive }) => {
  return (
    <button
      className={`custom-button ${isActive ? 'active' : ''}`}
      onClick={onClick}
    >
      {label}
    </button>
  );
};

export default Button;

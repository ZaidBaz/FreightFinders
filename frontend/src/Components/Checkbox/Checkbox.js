import React from 'react';
import './Checkbox.css';

const Checkbox = ({ label, onClick }) => {
    return (
        <div className = "checkbox-wrapper">
            <input
            type= "checkbox"
            onClick = {onClick} />
            <label>{label}</label>
        </div>
    );
  };

export default Checkbox;
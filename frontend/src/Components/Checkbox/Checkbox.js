import React from 'react';
import './Checkbox.css';

const Checkbox = ({ label, onChange }) => {
    return (
        <div className = "checkbox-wrapper">
            <input
            type= "checkbox"
            onChange = {(e) => {
                console.log('Checkbox clicked, checked:', e.target.checked); // Debug log
                onChange(e);
            }} />
            <label>{label}</label>
        </div>
    );
  };

export default Checkbox;
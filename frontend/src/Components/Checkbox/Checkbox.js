import React from 'react';
import './Checkbox.css';

const Checkbox = ({ label, onChange }) => {
    return (
        <div className = "checkbox-wrapper">
            <input
            type= "checkbox"
            onChange = {(e) => {
                onChange(e);
            }} />
            <label>{label}</label>
        </div>
    );
  };

export default Checkbox;
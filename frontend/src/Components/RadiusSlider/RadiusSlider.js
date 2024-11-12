// RadiusSlider.js
import React, { useState, useEffect } from 'react';
import './RadiusSlider.css';

const RadiusSlider = ({ label, inputValue, setInputValue }) => {

//   useEffect(() => {
//     setInputValue(0);
// }, []); 

  // Update slider value
  const handleSliderChange = (event) => {
    setInputValue(Number(event.target.value))
    // setRadius(Number(event.target.value));
  };

  // Increment the slider value
  const incrementRadius = () => {
    setInputValue((prev) => (prev < 250 ? prev + 25 : prev));
  };

  // Decrement the slider value
  const decrementRadius = () => {
    setInputValue((prev) => (prev >= 25 ? prev - 25 : prev));
  };

  return (
    <div className="radius-slider-container">
      <div className="radius-info">
        <p>{label}</p>
        <p className="radius-value">{inputValue} miles</p>
      </div>
      <div className="slider-wrapper">
        <input
          type="range"
          min="0"
          max="250"
          step="25"
          value={inputValue}
          onChange={handleSliderChange}
          className="slider"
        />
        <div className="increment-decrement-buttons">
          <button onClick={incrementRadius}>+</button>
          <button onClick={decrementRadius}>−</button>
        </div>
      </div>
      <div className="slider-labels">
        <span></span>
        <span>25</span>
        <span>75</span>
        <span>125</span>
        <span>175</span>
        <span>225</span>
        <span></span>
      </div>
    </div>
  );
};

export default RadiusSlider;

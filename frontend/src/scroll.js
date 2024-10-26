// RadiusSlider.js
import React, { useState } from 'react';
import './RadiusSlider.css';

const RadiusSlider = () => {
  const [radius, setRadius] = useState(25); // Initial value of the slider

  // Update slider value
  const handleSliderChange = (event) => {
    setRadius(Number(event.target.value));
  };

  // Increment the slider value
  const incrementRadius = () => {
    setRadius((prev) => (prev < 250 ? prev + 25 : prev));
  };

  // Decrement the slider value
  const decrementRadius = () => {
    setRadius((prev) => (prev > 25 ? prev - 25 : prev));
  };

  return (
    <div className="radius-slider-container">
      <div className="radius-info">
        <p>Pick up location radius</p>
        <p className="radius-value">{radius} miles</p>
      </div>
      <input
        type="range"
        min="25"
        max="250"
        step="25"
        value={radius}
        onChange={handleSliderChange}
        className="slider"
      />
      <div className="slider-labels">
        <span>25 mi</span>
        <span>50 mi</span>
        <span>75 mi</span>
        <span>200 mi</span>
        <span>225 mi</span>
        <span>250 mi</span>
      </div>
      <div className="increment-decrement-buttons">
        <button onClick={incrementRadius}>+</button>
        <button onClick={decrementRadius}>−</button>
      </div>
    </div>
  );
};

export default RadiusSlider;

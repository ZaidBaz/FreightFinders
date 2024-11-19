import React, { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';
import './CustomSlider.css';

function valuetext(value) {
  return `${value} mi`;
}

const CustomSlider = ({
  label, // Default label is an empty string
  min, // Default minimum value
  max, // Default maximum value
  step,
  defaultSliderVal,
  setInputValue
})  => {

  const [sliderValue, setSliderValue] = useState(parseInt(defaultSliderVal));
  const [marks, setMarks] = useState([]);

  useEffect(() => {

    const parsedMin = parseInt(min, 10); // Convert min to an integer
    const parsedMax = parseInt(max, 10); // Convert max to an integer
    const parsedStep = parseInt(step, 10); 

    const generatedMarks = [];
    for (let i = parsedMin; i <= parsedMax; i += parsedStep) {
      generatedMarks.push({ value: i, label: `${i} mi` });
    }
    setMarks(generatedMarks);
  }, [min, max, step]); 

  const handleSliderChange = (event, newValue) => {
    setInputValue(newValue);
    setSliderValue(newValue);
  };

  const handleIncrement = () => {
    setSliderValue((prev) => Math.min(prev + parseInt(step, 10), parseInt(max, 10)));
  };

  const handleDecrement = () => {
    setSliderValue((prev) => Math.max(prev - parseInt(step, 10), parseInt(min, 10)));
  };

  return (
    <div className="custom-slider-container">
      {label && (<div className="title-row">
        <p className="slider-title">{label}</p>
      </div>)}
      <div className="slider-row">
        <Box sx={{ flexGrow: 1 }}>
          <Slider
            aria-label="Distance slider"
            value={sliderValue}
            onChange={handleSliderChange}
            getAriaValueText={valuetext}
            min={parseInt(min, 10)}
            max={parseInt(max, 10)}
            step={parseInt(step, 10)}
            marks={marks}
            valueLabelDisplay="on"
            sx={{
              color: 'rgb(255, 106, 0)', // Slider track and thumb color
              '& .MuiSlider-thumb': {
                boxShadow: '0 0 0 8px rgba(255, 165, 0, 0.16)', // Thumb glow effect
              },
            }}
          />
        </Box>
        <div className="increment-decrement-buttons">
          <button onClick={handleIncrement}>+</button>
          <button onClick={handleDecrement}>−</button>
        </div>
      </div>
    </div>
  );
};

export default CustomSlider;
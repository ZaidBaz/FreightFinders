import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './CityAutoComplete.css';

const CityAutoComplete = ({ onCitySelect, query, setQuery }) => {
  // const [query, setQuery] = useState('');
  const [open, setOpen] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);

  const suggestionsRef = useRef(null); // Ref for the suggestions list container
  const inputRef = useRef(null); // Ref for the input field

  // Fetch cities based on the query
  const fetchCities = async (cityName) => {
    if (!cityName) {
      setSuggestions([]);
      return;
    }

    setLoading(true);
    try {
      const response = await axios.get(`http://127.0.0.1:8000/single-search/?query=${cityName}`);
      console.log(response);
      const cities = response.data.Locations.map((location) => ({
        city: location.Address.City,
        state: location.Address.StateName,
      }));
      setSuggestions(cities);
    } catch (error) {
      console.error('Error fetching cities:', error);
      setSuggestions([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (query) {
      fetchCities(query);
    } else {
      setSuggestions([]);
    }
  }, [query]);

  // Close the suggestions list if clicked outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        suggestionsRef.current && !suggestionsRef.current.contains(event.target) &&
        inputRef.current && !inputRef.current.contains(event.target)
      ) {
        setOpen(false); // Close the suggestions if clicked outside
      }
    };

    // Add event listener for clicks outside
    document.addEventListener('mousedown', handleClickOutside);

    // Cleanup the event listener when the component is unmounted
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleInputChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSelectCity = (city, state) => {
    onCitySelect(`${city}, ${state}`); // Notify parent component
    setQuery(`${city}, ${state}`); // Set input field value
    setOpen(false); // Hide suggestions
  };

  return (
    <div style={{ position: 'relative', width: '50%' }}> {/* Anchor the dropdown */}
      <input
        type="text"
        value={query}
        onFocus={() => setOpen(true)} // Show suggestions on input focus
        onChange={handleInputChange}
        className="city-input"
        ref={inputRef} // Attach input reference
      />
      {open && suggestions.length > 0 && (
        <ul className="suggestions-list" ref={suggestionsRef}> {/* Attach suggestions reference */}
          {suggestions.map((suggestion, index) => (
            <li
              key={index}
              onClick={() => handleSelectCity(suggestion.city, suggestion.state)}
              className="suggestion-item"
            >
              {suggestion.city}, {suggestion.state}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default CityAutoComplete;
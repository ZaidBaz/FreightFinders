import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './CityAutoComplete.css';

const CityAutoComplete = ({ onCitySelect }) => {
  const [query, setQuery] = useState('');
  const [open, setOpen] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchCities = async (cityName) => {
    if (!cityName) {
      setSuggestions([]);
      return;
    }

    setLoading(true);
    try {
      const response = await axios.get(`http://127.0.0.1:8000/single-search/?query=${cityName}`);
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

  const handleInputChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSelectCity = (city, state) => {
    onCitySelect(`${city}, ${state}`); // Notify parent component
    setQuery(`${city}, ${state}`); // Set input field value
    setOpen(false); // Hide suggestions

  };

  return (
    <div>
      <input
        type="text"
        value={query}
        onFocus={() => setOpen(true)} // Show suggestions on input focus
        onChange={handleInputChange}
        className="city-input"
      />
      {loading && <div>Loading...</div>}
      {open && suggestions.length > 0 && (
        <ul className="suggestions-list">
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

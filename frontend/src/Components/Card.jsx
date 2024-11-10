import React from "react";

const Card = ({ loadId, transportMode, originCity, destinationCity, totalDistance, totalWeight }) => {
  return (
    <div style={styles.cardContainer}>
      <div style={styles.infoSection}>
        <p style={styles.infoId}>Load ID: {loadId}</p>
        <p style={styles.infoText}>Distance: {totalDistance} Miles</p>
        <p style={styles.infoText}>Mode: {transportMode}</p>
        <p style={styles.infoText}>Weight: {totalWeight} lbs</p>
      </div>

      <div style={styles.detailsSection}>
        <div style={styles.locationHeader}>
          <span style={styles.dot}></span>
          <h2 style={styles.locationTitle}>{originCity}</h2>
        </div>
        <p style={styles.taskText}>to</p>
        <h2 style={styles.locationTitle}>{destinationCity}</h2>
      </div>

      <button style={styles.button}>CONTACT TO BOOK</button>
    </div>
  );
};

const styles = {
  cardContainer: {
    marginTop: "15px",
    display: "flex",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.4)",
    flexDirection: "column",
    width: "100%",  // Use full width of the parent container
    maxWidth: "400px",  // Optional: Set a max width for large screens
    borderRadius: "8px",
    padding: "16px",
    fontFamily: "Arial, sans-serif",
    backgroundColor: "white",  // Ensure card background is white
  },
  infoSection: {
    textAlign: "left",
    marginBottom: "10px",
    color: "#333",
  },
  infoId: {
    fontWeight: "bold",
    margin: "0",
  },
  infoText: {
    margin: "0",
    fontSize: "14px",
  },
  detailsSection: {
    textAlign: "left",
  },
  locationHeader: {
    display: "flex",
    alignItems: "center",
  },
  dot: {
    height: "8px",
    width: "8px",
    backgroundColor: "orange",
    borderRadius: "50%",
    marginRight: "8px",
  },
  locationTitle: {
    margin: "0",
    fontWeight: "bold",
    fontSize: "16px",
  },
  taskText: {
    margin: "4px 0 12px",
    fontSize: "14px",
    color: "#555",
  },
  button: {
    backgroundColor: "#ff6a00",
    color: "white",
    border: "none",
    padding: "12px",
    borderRadius: "8px",
    fontWeight: "bold",
    cursor: "pointer",
    textAlign: "center",
    marginTop: "10px",
  },
};

export default Card;
import React from "react";

const Card = () => {
  return (
    <div style={styles.cardContainer}>
      <div style={styles.infoSection}>
        <p style={styles.infoId}>1000534119</p>
        <p style={styles.infoText}>189 Miles</p>
        <p style={styles.infoText}>Power Only</p>
        <p style={styles.infoText}>22,000 lbs</p>
      </div>

      <div style={styles.detailsSection}>
        <div style={styles.locationHeader}>
          <span style={styles.dot}></span>
          <h2 style={styles.locationTitle}>GREEN BAY, WI</h2>
        </div>
        <p style={styles.dateText}>Sep 28, 7 am - Sep 29, 1 am</p>
        <p style={styles.taskText}>Drop Empty Trailer, Pick Up Loaded Trailer</p>

        <h2 style={styles.locationTitle}>GLENVIEW, IL</h2>
        <p style={styles.dateText}>Oct 28, 7 am - Sep 29, 1 am</p>
        <p style={styles.taskText}>Drop Empty Trailer, Pick Up Loaded Trailer</p>
      </div>

      <button style={styles.button}>CONTACT TO BOOK</button>
    </div>
  );
};

const styles = {
  cardContainer: {
    marginTop: "15px",
    display: "flex",
    boxShadow:" 0 4px 8px rgba(0, 0, 0, 0.4)", /* Darker shadow */
    flexDirection: "column",
    width: "300px",
    // border: "1px solid #d2a6ff",
    borderRadius: "8px",
    padding: "16px",
    fontFamily: "Arial, sans-serif",
    position: "relative",
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
  dateText: {
    margin: "0",
    fontSize: "14px",
    color: "#555",
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

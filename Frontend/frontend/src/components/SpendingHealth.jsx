import React from "react";

function SpendingHealth({ analytics }) {
  if (!analytics) return null;

  const {
    total_debit = 0,
    total_credit = 0,
    daily_average_spent = 0,
  } = analytics;

  // Simple health logic
  let health = "Good";
  let color = "#22c55e";

  if (total_debit > total_credit) {
    health = "Warning";
    color = "#facc15";
  }

  if (total_debit > total_credit * 1.2) {
    health = "Risky";
    color = "#ef4444";
  }

  return (
    <div style={styles.card}>
      <h3>Spending Health</h3>

      <p>💸 Total Spent: ₹{total_debit.toFixed(2)}</p>
      <p>💰 Total Income: ₹{total_credit.toFixed(2)}</p>
      <p>📅 Daily Avg: ₹{daily_average_spent.toFixed(2)}</p>

      <div style={{ ...styles.badge, background: color }}>
        {health}
      </div>
    </div>
  );
}

const styles = {
  card: {
    background: "#020617",
    padding: 20,
    borderRadius: 12,
    width: "100%",
  },
  badge: {
    marginTop: 12,
    padding: "6px 12px",
    borderRadius: 20,
    color: "#000",
    fontWeight: "bold",
    display: "inline-block",
  },
};

export default SpendingHealth;
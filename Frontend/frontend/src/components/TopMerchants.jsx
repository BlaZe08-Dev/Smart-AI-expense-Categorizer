import React from "react";

function TopMerchants({ merchantTotals }) {
  if (!merchantTotals) return null;

  const sorted = Object.entries(merchantTotals)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5);

  return (
    <div style={styles.card}>
      <h3>Top Merchants</h3>

      <ul style={styles.list}>
        {sorted.map(([merchant, amount]) => (
          <li key={merchant}>
            <span>{merchant}</span>
            <span>₹{amount.toFixed(2)}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

const styles = {
  card: {
    background: "#020617",
    padding: 20,
    borderRadius: 12,
    marginTop: 30,
  },
  list: {
    listStyle: "none",
    padding: 0,
  },
};

export default TopMerchants;

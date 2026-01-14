import React from "react";

function TopMerchants({ merchantTotals }) {
  if (!merchantTotals) return null;

  const sorted = Object.entries(merchantTotals)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5);

  return (
    <div style={styles.card}>
      <h3 style={styles.title}>Top Merchants</h3>

      <ul style={styles.list}>
        {sorted.map(([merchant, amount]) => (
          <li key={merchant} style={styles.item}>
            <span style={styles.merchant}>{merchant}</span>
            <span style={styles.amount}>₹{amount.toFixed(2)}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

const styles = {
  card: {
    width: "100%",
    background: "#020617",
    padding: "16px",
    borderRadius: 14,
    boxSizing: "border-box",
  },

  title: {
    marginBottom: 12,
    fontSize: "1.2rem",
  },

  list: {
    listStyle: "none",
    padding: 0,
    margin: 0,
    display: "flex",
    flexDirection: "column",
    gap: 10,
  },

  item: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "flex-start",
    gap: 10,
    paddingBottom: 6,
    borderBottom: "1px solid rgba(255,255,255,0.08)",
  },

  merchant: {
    fontSize: "0.95rem",
    lineHeight: 1.4,
    wordBreak: "break-word",
    flex: 1,
  },

  amount: {
    fontSize: "0.95rem",
    whiteSpace: "nowrap",
    opacity: 0.9,
  },
};

export default TopMerchants;
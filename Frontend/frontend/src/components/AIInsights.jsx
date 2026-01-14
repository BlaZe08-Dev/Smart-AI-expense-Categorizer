import React from "react";

function AIInsights({ analytics }) {
  if (!analytics) return null;

  const {
    category_totals = {},
    total_spent = 0,
    total_credit = 0,
    total_debit = total_spent,
  } = analytics;

  // 🔹 Highest spending category
  const topCategory = Object.entries(category_totals).sort(
    (a, b) => b[1] - a[1]
  )[0];

  const netFlow = total_credit - total_debit;

  // 🔹 Spending health message
  let healthMessage = "✅ Spending looks balanced.";
  if (total_debit > total_credit) {
    healthMessage = "⚠️ You are spending more than you earn.";
  }
  if (total_debit > total_credit * 1.5) {
    healthMessage = "🔴 High risk: expenses are much higher than income.";
  }

  return (
    <div style={styles.card}>
      <h3>AI Insights</h3>

      <p>
        💸 <b>Total Spent:</b> ₹{total_debit.toFixed(2)}
      </p>

      <p>
        💰 <b>Total Received:</b> ₹{total_credit.toFixed(2)}
      </p>

      <p>
        📊 <b>Net Cash Flow:</b>{" "}
        <span style={{ color: netFlow >= 0 ? "#22c55e" : "#ef4444" }}>
          {netFlow >= 0 ? "+" : "-"}₹{Math.abs(netFlow).toFixed(2)}
        </span>
      </p>

      {topCategory && (
        <p>
          🏷️ Highest spending category:{" "}
          <b>{topCategory[0]}</b> (₹{topCategory[1].toFixed(2)})
        </p>
      )}

      <p style={styles.health}>{healthMessage}</p>
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
  health: {
    marginTop: 10,
    fontWeight: 500,
  },
};

export default AIInsights;
import React from "react";

function AIInsights({ analytics }) {
  if (!analytics) return null;

  const categories = analytics.category_totals || {};
  const totalSpent = analytics.total_spent || 0;

  const topCategory = Object.entries(categories).sort(
    (a, b) => b[1] - a[1]
  )[0];

  return (
    <div style={styles.card}>
      <h3>AI Insights</h3>

      <p>
        💡 You spent <b>₹{totalSpent.toFixed(2)}</b> in total.
      </p>

      {topCategory && (
        <p>
          📊 Highest spending category is{" "}
          <b>{topCategory[0]}</b> (₹{topCategory[1].toFixed(2)}).
        </p>
      )}

      {topCategory?.[0].includes("TRANSFER") && (
        <p>
          ⚠️ Large amount spent on transfers.  
          Consider tracking friend-wise expenses.
        </p>
      )}
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
};

export default AIInsights;

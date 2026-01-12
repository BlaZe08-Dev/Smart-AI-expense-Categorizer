import React from "react";

function SummaryCards() {
  const analytics = JSON.parse(localStorage.getItem("analytics"));

  if (!analytics) return null;

  const totalSpent = analytics.total_spent || 0;
  const transactions = analytics.transactions_count || 0;

  const sourceHealth = analytics.source_health || {};
  const ruleCount = sourceHealth.RULE || 0;
  const aiCount = sourceHealth.AI_UNCERTAIN || 0;

  const currentMonth =
    Object.keys(analytics.monthly_totals || {})[0] || "This Month";

  return (
    <div style={styles.container}>
      <Card title="Total Spent" value={`₹ ${totalSpent}`} />
      <Card title="Transactions" value={transactions} />
      <Card title="Rule vs AI" value={`${ruleCount} / ${aiCount}`} />
      <Card title="Month" value={currentMonth} />
    </div>
  );
}

function Card({ title, value }) {
  return (
    <div style={styles.card}>
      <p style={styles.title}>{title}</p>
      <h2 style={styles.value}>{value}</h2>
    </div>
  );
}

const styles = {
  container: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
    gap: 20,
    marginBottom: 30,
  },
  card: {
    background: "#020617",
    border: "1px solid #1e293b",
    borderRadius: 12,
    padding: 20,
    textAlign: "center",
  },
  title: {
    color: "#94a3b8",
    fontSize: 14,
    marginBottom: 8,
  },
  value: {
    fontSize: 22,
    fontWeight: "bold",
    color: "#38bdf8",
  },
};

export default SummaryCards;

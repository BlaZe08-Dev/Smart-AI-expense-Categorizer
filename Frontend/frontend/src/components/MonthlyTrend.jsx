import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function MonthlyTrend({ dailyTotals }) {
  if (!dailyTotals || Object.keys(dailyTotals).length === 0) {
    return <p>No trend data available</p>;
  }

  const data = Object.entries(dailyTotals).map(([date, amount]) => ({
    date,
    amount,
  }));

  return (
    <div style={styles.card}>
      <h3>Spending Trend</h3>

      <ResponsiveContainer width="100%" height={250}>
        <LineChart data={data}>
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="amount"
            stroke="#38bdf8"
            strokeWidth={3}
          />
        </LineChart>
      </ResponsiveContainer>
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

export default MonthlyTrend;

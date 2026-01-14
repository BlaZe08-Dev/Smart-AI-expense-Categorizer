import React from "react";
import {
  ComposedChart,
  Bar,
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

  // 1️⃣ Sort by date
  const sorted = Object.entries(dailyTotals)
    .map(([date, amount]) => ({ date, daily: amount }))
    .sort((a, b) => new Date(a.date) - new Date(b.date));

  // 2️⃣ Build cumulative data
  let runningTotal = 0;
  const data = sorted.map((item) => {
    runningTotal += item.daily;
    return {
      date: item.date,
      daily: item.daily,
      cumulative: runningTotal,
    };
  });

  return (
    <div style={styles.card}>
      <h3>Daily Spending & Cumulative Trend</h3>

      <ResponsiveContainer width="100%" height={280}>
        <ComposedChart data={data}>
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          
          {/* Daily spending bars */}
          <Bar dataKey="daily" fill="#22c55e" radius={[4, 4, 0, 0]} />

          {/* Cumulative spending line */}
          <Line
            type="monotone"
            dataKey="cumulative"
            stroke="#38bdf8"
            strokeWidth={3}
            dot={{ r: 4 }}
          />
        </ComposedChart>
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
import React, { useMemo, useState } from "react";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const COLORS = [
  "#38bdf8",
  "#22c55e",
  "#facc15",
  "#f97316",
  "#ef4444",
  "#a855f7",
  "#14b8a6",
  "#eab308",
  "#fb7185",
];

const MIN_PERCENT = 4; // 👈 merge categories below 4%

function CategoryPie({ categorySummary }) {
  const [showOthersBreakdown, setShowOthersBreakdown] = useState(false);

  const { chartData, othersBreakdown, total } = useMemo(() => {
    if (!categorySummary || Object.keys(categorySummary).length === 0) {
      return { chartData: [], othersBreakdown: {}, total: 0 };
    }

    const totalAmount = Object.values(categorySummary).reduce(
      (a, b) => a + b,
      0
    );

    const main = [];
    const others = {};

    Object.entries(categorySummary).forEach(([cat, amt]) => {
      const percent = (amt / totalAmount) * 100;
      if (percent < MIN_PERCENT) {
        others[cat] = amt;
      } else {
        main.push({
          name: cat,
          value: amt,
          percent: percent.toFixed(1),
        });
      }
    });

    if (Object.keys(others).length) {
      const othersTotal = Object.values(others).reduce((a, b) => a + b, 0);
      main.push({
        name: "Others",
        value: othersTotal,
        percent: ((othersTotal / totalAmount) * 100).toFixed(1),
      });
    }

    return {
      chartData: main,
      othersBreakdown: others,
      total: totalAmount,
    };
  }, [categorySummary]);

  if (!chartData.length) {
    return <p>No category data available</p>;
  }

  return (
    <div style={styles.wrapper}>
      <h2 style={styles.title}>Category Breakdown</h2>

      <ResponsiveContainer width="100%" height={360}>
        <PieChart>
          <Pie
            data={chartData}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            innerRadius={80}
            outerRadius={130}
            paddingAngle={3}
            isAnimationActive
          >
            {chartData.map((_, index) => (
              <Cell
                key={index}
                fill={COLORS[index % COLORS.length]}
                onClick={() =>
                  chartData[index].name === "Others" &&
                  setShowOthersBreakdown(!showOthersBreakdown)
                }
                style={{ cursor: "pointer" }}
              />
            ))}
          </Pie>

          <Tooltip
            formatter={(value, name) => [
              `₹${value.toFixed(2)}`,
              name,
            ]}
          />
          <Legend />
        </PieChart>
      </ResponsiveContainer>

      {/* 👇 OTHERS BREAKDOWN */}
      {showOthersBreakdown && (
        <div style={styles.othersBox}>
          <h4>Included in “Others”</h4>
          <ul>
            {Object.entries(othersBreakdown).map(([cat, amt]) => (
              <li key={cat}>
                {cat} — ₹{amt.toFixed(2)}
              </li>
            ))}
          </ul>
        </div>
      )}

      <p style={styles.total}>Total Spent: ₹{total.toFixed(2)}</p>
    </div>
  );
}

const styles = {
  wrapper: {
    width: "100%",
    maxWidth: 700,
    margin: "0 auto",
    background: "#020617",
    borderRadius: 16,
    padding: 20,
  },
  title: {
    textAlign: "center",
    marginBottom: 10,
  },
  othersBox: {
    marginTop: 15,
    padding: 12,
    background: "#0f172a",
    borderRadius: 10,
    fontSize: 14,
  },
  total: {
    marginTop: 10,
    textAlign: "center",
    opacity: 0.8,
  },
};

export default CategoryPie;

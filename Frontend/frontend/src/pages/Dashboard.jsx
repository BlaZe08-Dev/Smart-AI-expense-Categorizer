import { useEffect, useState } from "react";
import CategoryPie from "../components/CategoryPie";
import TransactionTable from "../components/TransactionsTable";
import MonthlyTrend from "../components/MonthlyTrend";
import TopMerchants from "../components/TopMerchants";
import AIInsights from "../components/AIInsights";

function Dashboard() {
  const [transactions, setTransactions] = useState([]);
  const [categoryTotals, setCategoryTotals] = useState({});
  const [analytics, setAnalytics] = useState(null);

  // 🔹 Load saved data from localStorage
  useEffect(() => {
    const storedTransactions = JSON.parse(localStorage.getItem("transactions"));
    const storedAnalytics = JSON.parse(localStorage.getItem("analytics"));

    if (storedTransactions) {
      setTransactions(storedTransactions);
      recalcCategoryTotals(storedTransactions);
    }

    if (storedAnalytics) {
      setAnalytics(storedAnalytics);
    }
  }, []);

  // 🔹 Recalculate category totals (after edit)
  const recalcCategoryTotals = (txns) => {
  if (!txns || !txns.length) return;

  const totals = {};
  let totalSpent = 0;

  txns.forEach((txn) => {
    if (txn.type !== "debit") return;

    const cat = txn.category || "Others";
    totals[cat] = (totals[cat] || 0) + txn.amount;
    totalSpent += txn.amount;
  });

  const updatedAnalytics = {
    ...analytics,
    category_totals: totals,
    total_spent: totalSpent,
  };

  setCategoryTotals(totals);
  setAnalytics(updatedAnalytics);

  localStorage.setItem("analytics", JSON.stringify(updatedAnalytics));
  localStorage.setItem("transactions", JSON.stringify(txns));
};


  // 🔹 When category changes in table
  const handleTransactionsUpdate = (updated) => {
    setTransactions(updated);
    recalcCategoryTotals(updated);
  };

  if (!transactions.length) {
    return (
      <div style={styles.page}>
        <h1>Dashboard</h1>
        <p>No data available yet — upload a PDF first.</p>
      </div>
    );
  }

  return (
    <div style={styles.page}>
      <h1>Dashboard</h1>

      {/* 🔹 MAIN GRID */}
      <div style={styles.grid}>
        {/* LEFT COLUMN */}
        <div style={styles.left}>
          <AIInsights analytics={analytics} />

          <CategoryPie categorySummary={categoryTotals} />

          {analytics?.daily_totals && (
            <MonthlyTrend dailyTotals={analytics.daily_totals} />
          )}
        </div>

        {/* RIGHT COLUMN */}
        <div style={styles.right}>
          {analytics?.merchant_totals && (
            <TopMerchants merchantTotals={analytics.merchant_totals} />
          )}
        </div>
      </div>

      {/* 🔹 TRANSACTIONS TABLE (FULL WIDTH) */}
      <div style={styles.tableSection}>
        <TransactionTable
          transactions={transactions}
          onTransactionsUpdate={handleTransactionsUpdate}
        />
      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    padding: 20,
    background: "#020617",
    color: "#fff",
  },

  grid: {
    display: "grid",
    gridTemplateColumns: "2fr 1fr",
    gap: 24,
    marginTop: 20,
  },

  left: {
    display: "flex",
    flexDirection: "column",
    gap: 30,
  },

  right: {
    display: "flex",
    flexDirection: "column",
    gap: 30,
  },

  tableSection: {
    marginTop: 40,
    overflowX: "auto",
  },
};

export default Dashboard;

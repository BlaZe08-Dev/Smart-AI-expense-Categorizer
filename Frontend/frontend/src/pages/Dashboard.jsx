import { useEffect, useState } from "react";
import CategoryPie from "../components/CategoryPie";
import TransactionTable from "../components/TransactionsTable";
import TopMerchants from "../components/TopMerchants";
import AIInsights from "../components/AIInsights";
import MonthlyTrend from "../components/MonthlyTrend";
import SpendingHealth from "../components/SpendingHealth";

function Dashboard() {
  const [transactions, setTransactions] = useState([]);
  const [categoryTotals, setCategoryTotals] = useState({});
  const [analytics, setAnalytics] = useState(null);
  const [isDesktop, setIsDesktop] = useState(
    window.innerWidth >= 1024
  );

  // 🔹 Handle screen resize properly
  useEffect(() => {
    const handleResize = () => {
      setIsDesktop(window.innerWidth >= 1024);
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  // 🔹 Load saved data
  useEffect(() => {
    const storedTransactions = JSON.parse(
      localStorage.getItem("transactions")
    );
    const storedAnalytics = JSON.parse(
      localStorage.getItem("analytics")
    );

    if (storedTransactions?.length) {
      setTransactions(storedTransactions);
      recalcCategoryTotals(storedTransactions, storedAnalytics);
    }

    if (storedAnalytics) {
      setAnalytics(storedAnalytics);
    }
  }, []);

  // 🔹 Recalculate totals (safe)
  const recalcCategoryTotals = (txns, existingAnalytics = analytics) => {
    if (!txns?.length) return;

    const totals = {};
    let totalSpent = 0;

    txns.forEach((txn) => {
      if (txn.type !== "debit") return;

      const cat = txn.category || "Others";
      totals[cat] = (totals[cat] || 0) + txn.amount;
      totalSpent += txn.amount;
    });

    const updatedAnalytics = {
      ...(existingAnalytics || {}),
      category_totals: totals,
      total_spent: totalSpent,
    };

    setCategoryTotals(totals);
    setAnalytics(updatedAnalytics);

    localStorage.setItem(
      "analytics",
      JSON.stringify(updatedAnalytics)
    );
    localStorage.setItem(
      "transactions",
      JSON.stringify(txns)
    );
  };

  // 🔹 Category edit callback
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
      <div
        style={{
          ...styles.grid,
          gridTemplateColumns: isDesktop ? "2fr 1fr" : "1fr",
        }}
      >
        {/* LEFT */}
        <div style={styles.left}>
          <AIInsights analytics={analytics} />
          <CategoryPie categorySummary={categoryTotals} />

          {analytics?.daily_totals && (
            <MonthlyTrend dailyTotals={analytics.daily_totals} />
          )}
        </div>

        {/* RIGHT */}
        <div style={styles.right}>
          <SpendingHealth analytics={analytics} />
          
          {analytics?.merchant_totals && (
            <TopMerchants
              merchantTotals={analytics.merchant_totals}
            />
          )}
        </div>
      </div>

      {/* 🔹 TABLE */}
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
    width: "100%",
    padding: "clamp(12px, 4vw, 32px)",
    background: "#020617",
    color: "#fff",
    boxSizing: "border-box",
  },

  grid: {
    display: "grid",
    gap: "clamp(16px, 4vw, 32px)",
    marginTop: 20,
    width: "100%",
  },

  left: {
    display: "flex",
    flexDirection: "column",
    gap: "clamp(16px, 3vw, 28px)",
  },

  right: {
    display: "flex",
    flexDirection: "column",
    gap: "clamp(16px, 3vw, 28px)",
  },

  tableSection: {
    marginTop: 32,
    width: "100%",
    overflowX: "auto",
  },
};

export default Dashboard;
import React from "react";

function TransactionTable({ transactions, onTransactionsUpdate }) {
  if (!transactions.length) {
    return <p>No transactions available</p>;
  }

  // 🔥 Dynamic categories from transactions
  const categories = Array.from(
    new Set(transactions.map((t) => t.category || "Others"))
  );

  const handleCategoryChange = async (index, merchant, newCategory) => {
    await fetch("http://127.0.0.1:8000/overrides/add", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ merchant, category: newCategory }),
    });

    const updated = [...transactions];
    updated[index] = {
      ...updated[index],
      category: newCategory,
      source: "USER_OVERRIDE",
    };

    onTransactionsUpdate(updated);
  };

  return (
    <div style={styles.wrapper}>
      <h3 style={styles.title}>Transactions</h3>

      <div style={styles.tableContainer}>
        <table style={styles.table}>
          <thead>
            <tr>
              <th>Merchant</th>
              <th>Amount</th>
              <th>Category</th>
            </tr>
          </thead>

          <tbody>
            {transactions.map((txn, index) => (
              <tr key={index}>
                <td style={styles.merchant}>{txn.raw_text}</td>

                <td style={styles.amount}>₹{txn.amount.toFixed(2)}</td>

                <td>
                  <select
                    style={styles.select}
                    value={txn.category || "Others"}
                    onChange={(e) => {
                      if (e.target.value === "__custom__") {
                        const custom = prompt("Enter new category");
                        if (custom) {
                          handleCategoryChange(
                            index,
                            txn.raw_text,
                            custom
                          );
                        }
                      } else {
                        handleCategoryChange(
                          index,
                          txn.raw_text,
                          e.target.value
                        );
                      }
                    }}
                  >
                    {categories.map((cat) => (
                      <option key={cat} value={cat}>
                        {cat}
                      </option>
                    ))}
                    <option value="__custom__">+ Custom Category</option>
                  </select>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

const styles = {
  wrapper: {
    width: "100%",
    marginTop: 40,
  },

  title: {
    marginBottom: 12,
  },

  tableContainer: {
    width: "100%",
    overflowX: "auto",
    background: "#020617",
    borderRadius: 12,
    padding: 10,
  },

  table: {
    width: "100%",
    borderCollapse: "collapse",
    minWidth: 600, // 👈 enables scroll on mobile
  },

  merchant: {
    wordBreak: "break-word",
    maxWidth: 260,
  },

  amount: {
    whiteSpace: "nowrap",
  },

  select: {
    padding: "6px 8px",
    borderRadius: 6,
    background: "#0f172a",
    color: "#fff",
    border: "1px solid #1e293b",
    width: "100%",
  },
};

export default TransactionTable;
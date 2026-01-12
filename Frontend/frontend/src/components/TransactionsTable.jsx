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
    <div>
      <h3>Transactions</h3>

      <table>
        <tbody>
          {transactions.map((txn, index) => (
            <tr key={index}>
              <td>{txn.raw_text}</td>
              <td>₹{txn.amount}</td>
              <td>
                <select
                  value={txn.category || "Others"}
                  onChange={(e) => {
                    if (e.target.value === "__custom__") {
                      const custom = prompt("Enter new category");
                      if (custom) {
                        handleCategoryChange(index, txn.raw_text, custom);
                      }
                    } else {
                      handleCategoryChange(index, txn.raw_text, e.target.value);
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
  );
}

export default TransactionTable;

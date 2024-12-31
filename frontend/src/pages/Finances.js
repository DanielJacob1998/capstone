import React, { useState } from "react";
import FileUploader from "./FileUploader";

const Finances = () => {
  const [transactions, setTransactions] = useState([]);

  const handleFileUploadSuccess = (response) => {
    if (response && response.transactions) {
      setTransactions(response.transactions);
    } else {
      console.error("Invalid response from the server");
    }
  };

  return (
    <div className="finances">
      <h1>Finance Management</h1>
      <FileUploader
        endpoint="/files/parse-finance"
        onSuccess={handleFileUploadSuccess}
        acceptedFormats=".csv"
      />
      <h2>Transactions</h2>
      {transactions.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Amount</th>
              <th>Category</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((transaction, index) => (
              <tr key={index}>
                <td>{transaction.date}</td>
                <td>{transaction.amount}</td>
                <td>{transaction.category}</td>
                <td>{transaction.description}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No transactions to display.</p>
      )}
    </div>
  );
};

export default Finances;

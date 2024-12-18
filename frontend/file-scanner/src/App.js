import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import FileScanner from "./pages/FileScanner";
import Finances from "./pages/Finances";
import Events from "./pages/Events";
import "./App.css";

function App() {
  return (
    <Router>
      <div className="app-container">
        <Sidebar />
        <div className="content">
          <Routes>
            <Route path="/scanner" element={<FileScanner />} />
            <Route path="/finances" element={<Finances />} />
            <Route path="/events" element={<Events />} />
            <Route path="/" element={<h1>Welcome to the Dashboard!</h1>} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;

import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar"; // Import Sidebar
import Dashboard from "./components/Dashboard";
import FileUpload from "./pages/FileUpload";
import Finances from "./pages/Finances";
import CalendarView from "./pages/CalendarView";
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <div className="app-container" style={{ display: "flex" }}>
        <Sidebar /> {/* Sidebar always visible */}
        <main style={{ flex: 1 }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/scanner" element={<FileUpload />} />
            <Route path="/finances" element={<Finances />} />
            <Route path="/events" element={<CalendarView />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;

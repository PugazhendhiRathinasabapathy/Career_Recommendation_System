import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./HomePage";
import Questions from "./Questions";
import Result from "./Result";  // Import Result Page

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/questions" element={<Questions />} />
                <Route path="/result" element={<Result />} /> 
            </Routes>
        </Router>
    );
}

export default App;
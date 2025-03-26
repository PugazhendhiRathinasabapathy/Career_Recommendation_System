import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';  // Import useLocation
import './Result.css';

const Result = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const careers = location.state?.careers || [];

    return (
        <div className="result-container">
            <header className="header">
                <h1 className="title"> 🎯 Your Career Recommendations</h1>
                <p className="subtitle">Based on your answers, here are your best matches:</p>
            </header>
            {careers.length > 0 ? (
                <div className="results-container">
                    <ul>
                        {careers.map((career, index) => (
                            <li key={index}>{career}</li>
                        ))}
                    </ul>
                    <button className="restart-button" onClick={() => navigate('/')}>Take Quiz Again</button>
                </div>
            ) : (
                <p>No recommendations found. Please try again.</p>
            )}
        </div>
    );
};

export default Result;
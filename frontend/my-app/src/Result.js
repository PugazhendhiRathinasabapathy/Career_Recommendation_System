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
                    {careers.map((career, index) => (
                        <div className="career-card" key={index}>
                            <h2 className="career-title">{career.title}</h2>
                            <p className="career-section-content"><strong>Description:</strong> {career.description}</p>
                            <h3 className="career-section-title">Technology Skills</h3>
                            <ul>{career.technology_skills.map((skill, i) => <li key={i}>{skill}</li>)}</ul>
                            <h3 className="career-section-title">Skills</h3>
                            <ul>{career.skills.map((skill, i) => <li key={i}>{skill}</li>)}</ul>
                            <h3 className="career-section-title">Knowledge</h3>
                            <ul>{career.knowledge.map((item, i) => <li key={i}>{item}</li>)}</ul>
                            <p className="career-meta"><strong>Median Wages:</strong> {career.median_wages}</p>
                            <p className="career-meta"><strong>Projected Openings:</strong> {career.projected_openings}</p>
                            <h3 className="career-section-title">Related Occupations</h3>
                            <ul>{career.related_occupations.map((item, i) => <li key={i}>{item}</li>)}</ul>
                        </div>
                    ))}
                    <button className="restart-button" onClick={() => navigate('/')}>Take Quiz Again</button>
                </div>
            ) : (
                <p>No recommendations found. Please try again.</p>
            )}
        </div>
    );
};

export default Result;
import React from 'react';
import { useNavigate } from 'react-router-dom';  // Import useNavigate
import './HomePage.css'; 

const HomePage = () => {
  const navigate = useNavigate();  // Hook for navigation

  const handleClick = () => {
    navigate('/questions');  // Navigate to Questions.js
  };

  return (
    <div className="home-container">
        <header className="header">
            <h1 className="title">💡 CareerPathAI</h1>
            <p className="subtitle">Unlock Your Potential with Personalized Career Guidance!</p>
            <button className="begin-button" onClick={handleClick}>Let’s Begin</button>
        </header>

        <section className="intro">
            <h2 className="section-title">What is CareerPathAI?</h2>
            <p>
                CareerPathAI is an intelligent career recommendation system that helps you discover the perfect career path based on your skills, interests, and preferences.
                Answer a few questions and let AI guide you through your journey to success!
            </p>
        </section>

        <section className="features">
            <h2 className="section-title">Key Features</h2>
            <ul>
                <li>AI-powered career recommendations.</li>
                <li>Personalized career quizzes.</li>
                <li>Provides top 3 career options.</li>
                <li>Provides all requirement info.</li>
            </ul>
        </section>

        <footer className="footer">
            <p>© 2025 CareerPathAI. All rights reserved.</p>
        </footer>
    </div>
  );
};

export default HomePage;
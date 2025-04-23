import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';
import Logo from './Logo.png';
import PreQuizDialog from './PreQuizDialog';

const HomePage = () => {
  const navigate = useNavigate();
  const [dialogOpen, setDialogOpen] = useState(false);

  const handleDialogSubmit = (answers) => {
    localStorage.setItem('preQuizHistory', JSON.stringify(answers));
    navigate('/questions');
  };

  const handleClick = () => {
    setDialogOpen(true);
  };

  return (
    <div className="home-container">
      <header className="header">
        <div className="logo-title">
          <img src={Logo} alt="CareerPathAI Logo" className="logo-img" />
          <h1 className="title">CareerPathAI</h1>
        </div>
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

      <PreQuizDialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        onSubmit={handleDialogSubmit}
      />

      <footer className="footer">
        <p>© 2025 CareerPathAI. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default HomePage;
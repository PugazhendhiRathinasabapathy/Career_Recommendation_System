import React, { useState } from 'react';
import './Questions.css'; // Import the CSS file for styling

const Questions = () => {
  const [selectedOption, setSelectedOption] = useState('');

  const handleOptionChange = (event) => {
    setSelectedOption(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    if (!selectedOption) {
        alert("Please select an option!");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/submit-answer/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ selected_option: selectedOption }),
        });

        const data = await response.json();
        alert(data.message); // Show response from the backend
    } catch (error) {
        console.error("Error sending data:", error);
    }
};

  return (
    <div className="questions-container">
      <header className="header">
        <h1 className="title">Career Quiz</h1>
        <p className="subtitle">Answer the questions to find your best career path!</p>
      </header>
      <form className="question-form" onSubmit={handleSubmit}>
        <div className="option">
          <input
            type="radio"
            id="option1"
            name="careerOption"
            value="Option 1"
            checked={selectedOption === 'Option 1'}
            onChange={handleOptionChange}
          />
          <label htmlFor="option1">Option 1</label>
        </div>
        <div className="option">
          <input
            type="radio"
            id="option2"
            name="careerOption"
            value="Option 2"
            checked={selectedOption === 'Option 2'}
            onChange={handleOptionChange}
          />
          <label htmlFor="option2">Option 2</label>
        </div>
        <div className="option">
          <input
            type="radio"
            id="option3"
            name="careerOption"
            value="Option 3"
            checked={selectedOption === 'Option 3'}
            onChange={handleOptionChange}
          />
          <label htmlFor="option3">Option 3</label>
        </div>
        <div className="option">
          <input
            type="radio"
            id="option4"
            name="careerOption"
            value="Option 4"
            checked={selectedOption === 'Option 4'}
            onChange={handleOptionChange}
          />
          <label htmlFor="option4">Option 4</label>
        </div>
        <button className="submit-button" type="submit">Submit</button>
      </form>
    </div>
  );
};

export default Questions;
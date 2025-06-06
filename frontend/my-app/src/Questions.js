import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; 
import axios from 'axios';
import './Questions.css';

const API_URL = "https://careerpathai-7i5h.onrender.com";
// const API_URL = "http://127.0.0.1:8000";

const Questions = () => {
    const navigate = useNavigate();
    const [question, setQuestion] = useState('');
    const [options, setOptions] = useState([]);
    const [selectedOption, setSelectedOption] = useState('');
    const [step, setStep] = useState(1);
    const [loading, setLoading] = useState(false); // Loading state

    useEffect(() => {
        setStep(0);
        const preQuizHistory = JSON.parse(localStorage.getItem('preQuizHistory') || '{}');
        // Send preQuizHistory to backend
        axios.post(`${API_URL}/pre-quiz-history/`, preQuizHistory)
          .then(() => fetchQuestion())
          .catch((err) => {
            console.error("Error sending preQuizHistory:", err);
            fetchQuestion();
          });
    }, []);

    const fetchQuestion = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`${API_URL}/get-question/`);
            const text = response.data.question;

            if (typeof text !== "string") {
                throw new Error("Invalid response format: Expected a string");
            }

            const parsedOptions = text.match(/[A-D]\) (.+)/g) || [];
            if (parsedOptions.length !== 4) {
                fetchQuestion();
                return;
            }
            setQuestion(text.split("A)")[0].trim());
            setOptions(parsedOptions);
        } catch (error) {
            console.error("Error fetching question:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        if (!selectedOption) {
            alert("Please select an option!");
            return;
        }

        setLoading(true);
        try {
            const response = await axios.post(`${API_URL}/submit-answer/`, {
                selected_option: selectedOption,
                question: question
            });

            if (response.data.careers) {
                navigate('/result', { state: { careers: response.data.careers } });
            } else {
                const text = response.data.question;
                console.log("Full API Response:", response.data); 
                if (typeof text === "string") {
                    setQuestion(text.split("A)")[0].trim());
                    setOptions(text.match(/[A-D]\) (.+)/g) || []);
                } else {
                    console.error("Invalid question format received:", text);
                }
                setSelectedOption('');
                setStep(step + 1);
            }
        } catch (error) {
            console.error("Error submitting answer:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="questions-container">
            <header className="header">
                <h1 className="title"> 🤔 Career Quiz</h1>
                <p className="subtitle">Answer {19 - step + 1} more questions to get your career recommendations!</p>
            </header>

            {loading ? (
                <div className="loading-spinner"></div>
            ) : (
                <form className="question-form" onSubmit={handleSubmit}>
                    <h2>{question}</h2>
                    {options.map((option, index) => (
                        <label
                            className="option"
                            key={index}
                            htmlFor={`option${index}`}
                            style={{ display: 'block', cursor: 'pointer' }}
                        >
                            <input
                                type="radio"
                                id={`option${index}`}
                                name="careerOption"
                                value={option}
                                checked={selectedOption === option}
                                onChange={(e) => setSelectedOption(e.target.value)}
                                style={{ marginRight: '10px' }}
                            />
                            {option}
                        </label>
                    ))}
                    {/* Option E: Irrelevant / Skip */}
                    <label
                        className="option"
                        key="optionE"
                        htmlFor="optionE"
                        style={{ display: 'block', cursor: 'pointer' }}
                    >
                        <input
                            type="radio"
                            id="optionE"
                            name="careerOption"
                            value="E) Irrelevant / Skip"
                            checked={selectedOption === "E) Irrelevant / Skip"}
                            onChange={(e) => setSelectedOption(e.target.value)}
                            style={{ marginRight: '10px' }}
                        />
                        E) Irrelevant / Skip
                    </label>
                    <button className="submit-button" type="submit">Next</button>
                </form>
            )}
        </div>
    );
};

export default Questions;
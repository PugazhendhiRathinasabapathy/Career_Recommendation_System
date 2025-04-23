import React, { useState } from 'react';

const PreQuizDialog = ({ open, onClose, onSubmit }) => {
  const [form, setForm] = useState({
    education: '',
    major: '',
    passion: '',
    hobbies: '',
    strengths: ''
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(form);
    onClose();
  };

  if (!open) return null;

  return (
    <div className="dialog-backdrop">
      <div className="dialog">
        <h2>Tell us about yourself</h2>
        <form onSubmit={handleSubmit}>
          <label>
            What is your highest education qualification?
            <select name="education" value={form.education} onChange={handleChange} required>
              <option value="">Select</option>
              <option>High School Diploma</option>
              <option>Associate Degree</option>
              <option>Bachelor’s Degree</option>
              <option>Master’s Degree</option>
              <option>Doctorate (PhD)</option>
              <option>Other</option>
            </select>
          </label>
          <label>
            What was your field of study or major?
            <input
              type="text"
              name="major"
              value={form.major}
              onChange={handleChange}
              placeholder="E.g., Computer Science"
              required
            />
          </label>
          <label>
            What are you passionate about?
            <textarea
              name="passion"
              value={form.passion}
              onChange={handleChange}
              placeholder="E.g., Solving problems with code"
              required
            />
          </label>
          <label>
            What are your hobbies or activities you enjoy outside work/study?
            <textarea
              name="hobbies"
              value={form.hobbies}
              onChange={handleChange}
              placeholder="E.g., Playing guitar, hiking"
              required
            />
          </label>
          <label>
            What are your biggest strengths?
            <textarea
              name="strengths"
              value={form.strengths}
              onChange={handleChange}
              placeholder="E.g., Problem-solving, creativity"
              required
            />
          </label>
          <button type="submit">Start Quiz</button>
        </form>
      </div>
    </div>
  );
};

export default PreQuizDialog;
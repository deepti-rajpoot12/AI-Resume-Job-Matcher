import { useState } from 'react'

function InterviewQuestions({ items }) {
  const [openQuestion, setOpenQuestion] = useState(null)
  return <section className="interview-section" aria-labelledby="interview-heading"><div className="section-heading compact"><p className="section-kicker">Interview preparation</p><h2 id="interview-heading">Interview Preparation</h2><p>Practice questions generated from your resume and the target role.</p></div>{items.length ? <div className="accordion-list">{items.map((item, index) => { const isOpen = openQuestion === index; return <article className="accordion-item" key={`${item}-${index}`}><button type="button" aria-expanded={isOpen} onClick={() => setOpenQuestion(isOpen ? null : index)}><span className="question-number">Question {String(index + 1).padStart(2, '0')}</span><span className="question-text">{item}</span><span className="accordion-toggle" aria-hidden="true">{isOpen ? '−' : '+'}</span></button>{isOpen && <div className="accordion-panel"><p>Use this question to prepare a concise example from your experience that is relevant to the role.</p></div>}</article> })}</div> : <p className="empty-result">No interview questions generated.</p>}</section>
}

export default InterviewQuestions

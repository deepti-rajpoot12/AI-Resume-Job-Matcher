function StrengthsCard({ items }) {
  return <section className="result-card strengths-card"><div className="result-card-heading"><span className="result-icon blue" aria-hidden="true">✦</span><h3>Your Strengths</h3></div>{items.length ? <ul className="strength-list">{items.map((item, index) => <li key={`${item}-${index}`}><span aria-hidden="true">✓</span>{item}</li>)}</ul> : <p className="empty-result">No strengths were identified.</p>}</section>
}
export default StrengthsCard

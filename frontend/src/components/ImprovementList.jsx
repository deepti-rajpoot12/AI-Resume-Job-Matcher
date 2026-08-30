function ImprovementList({ items }) {
  return <section className="result-card improvement-card"><div className="result-card-heading"><span className="result-icon purple" aria-hidden="true">↗</span><h3>How to Improve Your Match</h3></div>{items.length ? <ol className="improvement-list">{items.map((item, index) => <li key={`${item}-${index}`}><span>{String(index + 1).padStart(2, '0')}</span><p>{item}</p></li>)}</ol> : <p className="empty-result">No improvement suggestions were identified.</p>}</section>
}
export default ImprovementList

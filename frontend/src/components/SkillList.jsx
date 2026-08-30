function SkillList({ title, items, type }) {
  const isGaps = type === 'gaps'
  const emptyText = isGaps ? 'No major skill gaps identified.' : 'No matching skills identified yet.'
  return <section className="result-card skill-card"><div className="result-card-heading"><span className={`result-icon ${isGaps ? 'amber' : 'green'}`} aria-hidden="true">{isGaps ? '!' : '✓'}</span><h3>{title}</h3></div>{items.length ? <ul className={`skill-pills ${isGaps ? 'gaps' : ''}`}>{items.map((item, index) => <li key={`${item}-${index}`}>{item}</li>)}</ul> : <p className="empty-result">{emptyText}</p>}</section>
}

export default SkillList

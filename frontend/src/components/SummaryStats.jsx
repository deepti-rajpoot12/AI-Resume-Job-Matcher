function SummaryStats({ analysis }) {
  const stats = [[`${analysis.match_score}%`, 'Match'], [analysis.matching_skills.length, 'Matching Skills'], [analysis.missing_skills.length, 'Skill Gaps'], [analysis.interview_questions.length, 'Interview Questions']]
  return <section className="summary-stats" aria-label="Analysis summary">{stats.map(([value, label]) => <div key={label}><strong>{value}</strong><span>{label}</span></div>)}</section>
}
export default SummaryStats

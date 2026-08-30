function scoreDetails(score) {
  if (score >= 90) return ['Excellent Match', 'Your profile aligns exceptionally well with the requirements of this role.']
  if (score >= 75) return ['Strong Match', 'Your profile aligns strongly with the requirements of this role.']
  if (score >= 60) return ['Moderate Match', 'Your profile meets several requirements, with room to strengthen your match.']
  return ['Needs Improvement', 'Your profile has opportunities to better align with this role.']
}

function MatchScore({ score }) {
  const [label, message] = scoreDetails(score)
  return <section className="match-score-card"><div className="score-ring" style={{ '--score': score }}><div><strong>{score}%</strong><span>Match score</span></div></div><div className="score-copy"><p className="section-kicker">{label}</p><h3>{message}</h3><p>The score reflects how closely your resume aligns with the target job description.</p></div></section>
}

export default MatchScore

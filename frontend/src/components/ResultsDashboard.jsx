import ImprovementList from './ImprovementList'
import InterviewQuestions from './InterviewQuestions'
import MatchScore from './MatchScore'
import SkillList from './SkillList'
import StrengthsCard from './StrengthsCard'
import SummaryStats from './SummaryStats'
import CareerRoadmap from './CareerRoadmap'

function ResultsDashboard({ analysis, guidance, guidanceError, isGeneratingGuidance, onGenerateGuidance, resultsRef, onStartNew }) {
  return <section className="results-section section-wrap" ref={resultsRef} aria-labelledby="results-heading"><div className="section-heading results-heading"><div><p className="section-kicker">Analysis complete</p><h2 id="results-heading">Resume Match Analysis</h2><p>AI-generated insights based on your resume and the target job.</p></div><span className="complete-badge">✓ Analysis ready</span></div><MatchScore score={analysis.match_score} /><SummaryStats analysis={analysis} /><div className="skills-grid"><SkillList title="Matching Skills" items={analysis.matching_skills} type="matching" /><SkillList title="Skill Gaps" items={analysis.missing_skills} type="gaps" /></div><StrengthsCard items={analysis.strengths} /><ImprovementList items={analysis.improvement_suggestions} /><InterviewQuestions items={analysis.interview_questions} /><CareerRoadmap guidance={guidance} error={guidanceError} isLoading={isGeneratingGuidance} onGenerate={onGenerateGuidance} /><div className="new-analysis"><div><h3>Ready to explore another role?</h3><p>Start fresh with a different resume or job description.</p></div><button type="button" className="secondary-button" onClick={onStartNew}>Analyze another resume <span aria-hidden="true">→</span></button></div></section>
}
export default ResultsDashboard

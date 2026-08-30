function Header({ onHistory, onHome }) {
  return <header className="site-header"><div className="header-inner"><button className="brand" onClick={onHome} aria-label="AI Resume and Job Matcher home"><span className="brand-mark" aria-hidden="true">A</span><span>AI Resume &amp; Job Matcher</span><span className="ai-badge">AI-Powered</span></button><div className="header-meta" aria-label="Application status"><button className="history-nav" onClick={onHistory}>Analysis History</button><span className="gemini-status"><span aria-hidden="true" />Gemini AI</span></div></div></header>
}
export default Header

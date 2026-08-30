function AnalyzeButton({ disabled, isLoading }) { return <button className="analyze-button" type="submit" disabled={disabled}>{isLoading && <span className="spinner" aria-hidden="true" />}{isLoading ? 'Analyzing resume...' : 'Analyze Resume'}<span aria-hidden="true">→</span></button> }
export default AnalyzeButton

function ErrorState({ onRetry }) { return <section className="error-state" role="alert"><span aria-hidden="true">!</span><div><h3>Analysis couldn&apos;t be completed</h3><p>Something went wrong while analyzing your resume. Please try again.</p></div><button type="button" className="secondary-button" onClick={onRetry}>Try Again</button></section> }
export default ErrorState

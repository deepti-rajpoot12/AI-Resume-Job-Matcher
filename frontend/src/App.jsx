import { useEffect, useRef, useState } from 'react'
import AnalyzeButton from './components/AnalyzeButton'
import EmptyState from './components/EmptyState'
import ErrorState from './components/ErrorState'
import Footer from './components/Footer'
import Header from './components/Header'
import Hero from './components/Hero'
import JobDescriptionInput from './components/JobDescriptionInput'
import ResultsDashboard from './components/ResultsDashboard'
import ResumeUploader from './components/ResumeUploader'
import HistoryPanel from './components/HistoryPanel'
import { analyzeResume, generateCareerGuidance } from './services/api'

const MAX_FILE_SIZE = 10 * 1024 * 1024

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [analysis, setAnalysis] = useState(null)
  const [error, setError] = useState('')
  const [fileError, setFileError] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [guidance, setGuidance] = useState(null)
  const [guidanceError, setGuidanceError] = useState('')
  const [isGeneratingGuidance, setIsGeneratingGuidance] = useState(false)
  const [view, setView] = useState('home')
  const workspaceRef = useRef(null)
  const resultsRef = useRef(null)

  useEffect(() => {
    if (analysis) resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }, [analysis])

  function chooseFile(file) {
    if (!file) return
    const isPdf = file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf')
    if (!isPdf) {
      setSelectedFile(null)
      setFileError('Please select a PDF resume.')
      return
    }
    if (file.size > MAX_FILE_SIZE) {
      setSelectedFile(null)
      setFileError('Please choose a PDF smaller than 10 MB.')
      return
    }
    setSelectedFile(file)
    setFileError('')
    setError('')
  }

  async function handleAnalyze(event) {
    event?.preventDefault()
    if (!selectedFile || !jobDescription.trim() || isAnalyzing) return
    setError('')
    setAnalysis(null)
    setIsAnalyzing(true)
    try {
      const response = await analyzeResume(selectedFile, jobDescription.trim())
      setAnalysis(response.analysis)
      setGuidance(null)
      setGuidanceError('')
    } catch (err) {
      setError(err?.message || 'Something went wrong while analyzing your resume. Please try again.')
    } finally {
      setIsAnalyzing(false)
    }
  }

  function startNewAnalysis() {
    setSelectedFile(null)
    setJobDescription('')
    setAnalysis(null)
    setError('')
    setFileError('')
    setGuidance(null)
    setGuidanceError('')
    workspaceRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }

  const canAnalyze = Boolean(selectedFile && jobDescription.trim() && !isAnalyzing)

  async function handleGenerateGuidance() {
    if (!analysis || isGeneratingGuidance) return
    setGuidanceError('')
    setIsGeneratingGuidance(true)
    try {
      const response = await generateCareerGuidance(analysis, jobDescription)
      setGuidance(response.guidance)
    } catch (err) {
      setGuidanceError(err?.message || "We couldn't generate your career roadmap. Please try again.")
    } finally {
      setIsGeneratingGuidance(false)
    }
  }

  return (
    <div className="app-shell">
      <Header onHistory={() => setView('history')} onHome={() => setView('home')} />
      <main>
        {view === 'history' ? <HistoryPanel onView={(item) => { setAnalysis(item.analysis); setGuidance(item.career_plan); setJobDescription(item.job_description); setView('home') }} /> : <>
        <Hero />
        <section className="workspace-section section-wrap" ref={workspaceRef} aria-labelledby="workspace-heading">
          <div className="section-heading">
            <p className="section-kicker">Analysis workspace</p>
            <h2 id="workspace-heading">Build your match analysis</h2>
            <p>Provide your resume and the role you are targeting to get focused, actionable insights.</p>
          </div>
          <form onSubmit={handleAnalyze}>
            <div className="workspace-grid">
              <ResumeUploader file={selectedFile} error={fileError} disabled={isAnalyzing} onChooseFile={chooseFile} onRemove={() => { setSelectedFile(null); setFileError('') }} />
              <JobDescriptionInput value={jobDescription} disabled={isAnalyzing} onChange={setJobDescription} onClear={() => setJobDescription('')} />
            </div>
            <AnalyzeButton disabled={!canAnalyze} isLoading={isAnalyzing} />
          </form>
          {error && <ErrorState onRetry={handleAnalyze} />}
          {!analysis && !error && <EmptyState />}
        </section>
        {analysis && <ResultsDashboard analysis={analysis} guidance={guidance} guidanceError={guidanceError} isGeneratingGuidance={isGeneratingGuidance} onGenerateGuidance={handleGenerateGuidance} resultsRef={resultsRef} onStartNew={startNewAnalysis} />}</>}
      </main>
      <Footer />
    </div>
  )
}

export default App

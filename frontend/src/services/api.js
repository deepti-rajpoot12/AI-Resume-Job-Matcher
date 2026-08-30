const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function analyzeResume(resume, jobDescription) {
  const formData = new FormData()
  formData.append('resume', resume)
  formData.append('job_description', jobDescription)

  const response = await fetch(`${API_BASE_URL}/api/analyze`, {
    method: 'POST',
    body: formData,
  })

  const payload = await response.json().catch(() => ({}))
  if (!response.ok) {
    throw new Error(payload.detail || 'Unable to analyze the resume. Please try again.')
  }

  return payload
}

export async function generateCareerGuidance(analysis, jobDescription) {
  const response = await fetch(`${API_BASE_URL}/api/career-guidance`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ analysis, job_description: jobDescription }),
  })

  const payload = await response.json().catch(() => ({}))
  if (!response.ok) {
    throw new Error(payload.detail || 'Unable to generate the career roadmap.')
  }

  return payload
}

export async function getHistory() { const response = await fetch(`${API_BASE_URL}/api/history`); if (!response.ok) throw new Error('History unavailable'); return response.json() }
export async function getHistoryItem(id) { const response = await fetch(`${API_BASE_URL}/api/history/${id}`); if (!response.ok) throw new Error('History item unavailable'); return response.json() }
export async function deleteHistoryItem(id) { const response = await fetch(`${API_BASE_URL}/api/history/${id}`, { method: 'DELETE' }); if (!response.ok) throw new Error('Unable to delete history item') }

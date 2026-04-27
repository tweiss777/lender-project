import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { type LenderPreview } from '@/types'
import { Button } from '@/components/ui/button'

type Stage = 'upload' | 'preview' | 'saving' | 'done'

export default function AddLenderPage() {
  const navigate = useNavigate()
  const [stage, setStage] = useState<Stage>('upload')
  const [file, setFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<LenderPreview | null>(null)
  const [isParsing, setIsParsing] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleParse = async () => {
    if (!file) return
    setIsParsing(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await fetch('/api/v1/lenders/parse', {
        method: 'POST',
        body: formData,
      })
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || 'Failed to parse PDF')
      }
      const data: LenderPreview = await res.json()
      setPreview(data)
      setStage('preview')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong')
    } finally {
      setIsParsing(false)
    }
  }

  const handleConfirm = async () => {
    if (!preview) return
    setStage('saving')
    setError(null)

    try {
      const res = await fetch('/api/v1/lenders/confirm', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(preview),
      })
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || 'Failed to save lender')
      }
      setStage('done')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong')
      setStage('preview')
    }
  }

  if (stage === 'done') {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-white rounded-xl border p-10 text-center max-w-md">
          <div className="text-5xl mb-4">✅</div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Lender Added</h2>
          <p className="text-gray-500 mb-6">
            <strong>{preview?.lender_name}</strong> has been saved with {preview?.programs.length} program(s).
          </p>
          <div className="flex gap-3 justify-center">
            <Button variant="outline" onClick={() => navigate('/lenders')}>
              View All Lenders
            </Button>
            <Button onClick={() => { setStage('upload'); setFile(null); setPreview(null) }}>
              Add Another
            </Button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white border-b px-6 py-4 flex items-center gap-4">
        <button onClick={() => navigate('/lenders')} className="text-gray-400 hover:text-gray-600">
          ←
        </button>
        <h1 className="text-xl font-semibold text-gray-900">Add Lender via PDF</h1>
      </div>

      <div className="max-w-3xl mx-auto px-6 py-8 space-y-6">
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3">
            {error}
          </div>
        )}

        {/* Upload stage */}
        {stage === 'upload' && (
          <div className="bg-white rounded-xl border p-8 text-center space-y-4">
            <div className="text-4xl">📄</div>
            <h2 className="text-lg font-semibold text-gray-900">Upload Lender Guidelines PDF</h2>
            <p className="text-sm text-gray-500">
              Upload a lender guidelines PDF. Claude will extract the credit policy criteria automatically.
            </p>
            <input
              type="file"
              accept="application/pdf"
              onChange={e => setFile(e.target.files?.[0] ?? null)}
              className="block mx-auto text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            />
            {file && (
              <p className="text-sm text-gray-600">
                Selected: <strong>{file.name}</strong>
              </p>
            )}
            <Button onClick={handleParse} disabled={!file || isParsing}>
              {isParsing ? 'Parsing PDF...' : 'Parse PDF'}
            </Button>
          </div>
        )}

        {/* Preview stage */}
        {(stage === 'preview' || stage === 'saving') && preview && (
          <div className="space-y-6">
            <div className="bg-white rounded-xl border p-6 space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-lg font-semibold text-gray-900">{preview.lender_name}</h2>
                  <p className="text-sm text-gray-500">{preview.programs.length} program(s) extracted</p>
                </div>
                <span className="text-xs bg-yellow-50 text-yellow-700 border border-yellow-200 px-2 py-1 rounded">
                  Review before saving
                </span>
              </div>

              {preview.programs.map((program, i) => (
                <div key={i} className="border rounded-lg p-4 space-y-3">
                  <h3 className="font-medium text-gray-800">{program.program_name}</h3>
                  <div className="grid grid-cols-2 gap-x-6 gap-y-1.5 text-sm">
                    {[
                      ['Min FICO', program.min_fico],
                      ['Min PayNet', program.min_paynet_score],
                      ['Min Years in Business', program.min_years_in_business ? `${program.min_years_in_business}yr` : null],
                      ['Loan Range', (program.min_loan_amount || program.max_loan_amount)
                        ? `$${(program.min_loan_amount ?? 0).toLocaleString()} – $${(program.max_loan_amount ?? 0).toLocaleString()}`
                        : null],
                      ['Term Range', (program.min_term_months || program.max_term_months)
                        ? `${program.min_term_months ?? 0}–${program.max_term_months ?? 0}mo`
                        : null],
                      ['Max Equipment Age', program.max_equipment_age_years ? `${program.max_equipment_age_years}yr` : null],
                      ['Bankruptcy Policy', program.no_bankruptcy ? 'No bankruptcies' : program.min_years_since_bankruptcy ? `${program.min_years_since_bankruptcy}yr since discharge` : null],
                      ['Judgments', program.allows_judgments === false ? 'Not allowed' : null],
                      ['Tax Liens', program.allows_liens === false ? 'Not allowed' : null],
                      ['US Citizens Only', program.requires_us_citizen ? 'Yes' : null],
                    ].filter(([, v]) => v !== null).map(([label, value]) => (
                      <div key={String(label)} className="flex justify-between">
                        <span className="text-gray-500">{label}</span>
                        <span className="font-medium text-gray-800">{String(value)}</span>
                      </div>
                    ))}
                  </div>

                  {program.excluded_industries.length > 0 && (
                    <div className="text-sm">
                      <span className="text-gray-500">Excluded Industries: </span>
                      <span className="text-gray-800">{program.excluded_industries.join(', ')}</span>
                    </div>
                  )}
                  {program.excluded_states.length > 0 && (
                    <div className="text-sm">
                      <span className="text-gray-500">Excluded States: </span>
                      <span className="text-gray-800">{program.excluded_states.join(', ')}</span>
                    </div>
                  )}
                  {program.equipment_restrictions.length > 0 && (
                    <div className="text-sm">
                      <span className="text-gray-500">Equipment Restrictions: </span>
                      <span className="text-gray-800">{program.equipment_restrictions.join(', ')}</span>
                    </div>
                  )}
                </div>
              ))}
            </div>

            <div className="flex gap-3">
              <Button variant="outline" onClick={() => setStage('upload')} disabled={stage === 'saving'}>
                ← Re-upload
              </Button>
              <Button onClick={handleConfirm} disabled={stage === 'saving'}>
                {stage === 'saving' ? 'Saving...' : 'Confirm & Save'}
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

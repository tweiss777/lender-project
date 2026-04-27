import { useEffect, useState } from 'react'
import { useParams, useSearchParams, Link } from 'react-router-dom'
import { type MatchResult } from '@/types'
import CriteriaResultCard from '@/components/CriteriaResultCard'

export default function ResultsPage() {
  const { borrower_id } = useParams()
  const [searchParams] = useSearchParams()
  const loanRequestId = searchParams.get('loan_request_id')

  const [results, setResults] = useState<MatchResult[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!borrower_id) return
    fetch(`/api/v1/borrowers/${borrower_id}/underwrite`)
      .then(r => {
        if (!r.ok) throw new Error('Failed to load results')
        return r.json()
      })
      .then((data: MatchResult[]) => {
        // If loan_request_id is in the URL, filter to that specific run
        const filtered = loanRequestId
          ? data.filter(r => r.loan_request_id === Number(loanRequestId))
          : data
        setResults(filtered.sort((a, b) => b.match_score - a.match_score))
      })
      .catch(err => setError(err.message))
      .finally(() => setIsLoading(false))
  }, [borrower_id, loanRequestId])

  const eligible = results.filter(r => r.is_eligible)
  const ineligible = results.filter(r => !r.is_eligible)

  if (isLoading) return (
    <div className="min-h-screen flex items-center justify-center text-gray-500">
      Running underwriting...
    </div>
  )

  if (error) return (
    <div className="min-h-screen flex items-center justify-center text-red-500">
      {error}
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white border-b px-6 py-4 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold text-gray-900">Underwriting Results</h1>
          <p className="text-sm text-gray-500 mt-0.5">
            {eligible.length} eligible · {ineligible.length} ineligible · {results.length} total programs evaluated
          </p>
        </div>
        <Link
          to="/apply/borrower"
          className="text-sm text-blue-600 hover:underline"
        >
          + New Application
        </Link>
      </div>

      <div className="max-w-3xl mx-auto px-6 py-8 space-y-8">
        {eligible.length > 0 && (
          <section>
            <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-green-500 inline-block" />
              Eligible Lenders ({eligible.length})
            </h2>
            <div className="space-y-4">
              {eligible.map(r => (
                <CriteriaResultCard key={r.match_id} result={r} />
              ))}
            </div>
          </section>
        )}

        {ineligible.length > 0 && (
          <section>
            <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-red-400 inline-block" />
              Ineligible Lenders ({ineligible.length})
            </h2>
            <div className="space-y-4">
              {ineligible.map(r => (
                <CriteriaResultCard key={r.match_id} result={r} />
              ))}
            </div>
          </section>
        )}

        {results.length === 0 && (
          <div className="text-center py-16 text-gray-400">
            No results found.
          </div>
        )}
      </div>
    </div>
  )
}

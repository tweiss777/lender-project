import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

interface LenderRow {
  lender_id: number
  lender_name: string
  policies: {
    policy_id: number
    program_name: string
    min_fico: number | null
    min_paynet_score: number | null
    min_years_in_business: number | null
    min_loan_amount: number | null
    max_loan_amount: number | null
    max_equipment_age_years: number | null
  }[]
}

function fmt(val: number | null, prefix = '') {
  if (val === null || val === undefined) return '—'
  return `${prefix}${val.toLocaleString()}`
}

export default function LendersPage() {
  const [lenders, setLenders] = useState<LenderRow[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch('/api/v1/lenders')
      .then(r => {
        if (!r.ok) throw new Error('Failed to load lenders')
        return r.json()
      })
      .then(setLenders)
      .catch(err => setError(err.message))
      .finally(() => setIsLoading(false))
  }, [])

  if (isLoading) return (
    <div className="min-h-screen flex items-center justify-center text-gray-500">Loading...</div>
  )
  if (error) return (
    <div className="min-h-screen flex items-center justify-center text-red-500">{error}</div>
  )

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white border-b px-6 py-4 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold text-gray-900">Lender Policies</h1>
          <p className="text-sm text-gray-500 mt-0.5">{lenders.length} lenders configured</p>
        </div>
        <Link
          to="/lenders/add"
          className="bg-blue-600 text-white text-sm px-4 py-2 rounded-md hover:bg-blue-700"
        >
          + Add Lender via PDF
        </Link>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-8 space-y-8">
        {lenders.map(lender => (
          <div key={lender.lender_id} className="bg-white rounded-lg border overflow-hidden">
            <div className="px-5 py-3 bg-gray-50 border-b">
              <h2 className="font-semibold text-gray-800">{lender.lender_name}</h2>
              <p className="text-xs text-gray-500">{lender.policies.length} program(s)</p>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-xs text-gray-500 border-b">
                    <th className="px-4 py-2 font-medium">Program</th>
                    <th className="px-4 py-2 font-medium">Min FICO</th>
                    <th className="px-4 py-2 font-medium">Min PayNet</th>
                    <th className="px-4 py-2 font-medium">Min TIB</th>
                    <th className="px-4 py-2 font-medium">Loan Range</th>
                    <th className="px-4 py-2 font-medium">Max Equip Age</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {lender.policies.map(policy => (
                    <tr key={policy.policy_id} className="hover:bg-gray-50">
                      <td className="px-4 py-3 font-medium text-gray-800">{policy.program_name}</td>
                      <td className="px-4 py-3 text-gray-600">{fmt(policy.min_fico)}</td>
                      <td className="px-4 py-3 text-gray-600">{fmt(policy.min_paynet_score)}</td>
                      <td className="px-4 py-3 text-gray-600">
                        {policy.min_years_in_business ? `${policy.min_years_in_business}yr` : '—'}
                      </td>
                      <td className="px-4 py-3 text-gray-600">
                        {policy.min_loan_amount || policy.max_loan_amount
                          ? `${fmt(policy.min_loan_amount, '$')} – ${fmt(policy.max_loan_amount, '$')}`
                          : '—'}
                      </td>
                      <td className="px-4 py-3 text-gray-600">
                        {policy.max_equipment_age_years ? `${policy.max_equipment_age_years}yr` : '—'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

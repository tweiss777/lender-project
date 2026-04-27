import { type MatchResult, type CriterionResult } from '@/types'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

interface CriteriaResultCardProps {
  result: MatchResult
}

function CriterionRow({ criterion }: { criterion: CriterionResult }) {
  return (
    <div className={`flex items-start gap-3 py-2.5 border-b last:border-0
      ${criterion.passed ? '' : 'bg-red-50 -mx-4 px-4 rounded'}
    `}>
      <span className={`mt-0.5 text-sm font-bold flex-shrink-0
        ${criterion.passed ? 'text-green-500' : 'text-red-500'}
      `}>
        {criterion.passed ? '✓' : '✗'}
      </span>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-gray-800">{criterion.name}</p>
        <p className={`text-xs mt-0.5 ${criterion.passed ? 'text-gray-500' : 'text-red-600'}`}>
          {criterion.reason}
        </p>
      </div>
    </div>
  )
}

export default function CriteriaResultCard({ result }: CriteriaResultCardProps) {
  const passedCount = result.criteria_results.filter(c => c.passed).length
  const totalCount = result.criteria_results.length

  return (
    <Card className={`border-l-4 ${result.is_eligible ? 'border-l-green-500' : 'border-l-red-400'}`}>
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-4">
          <div>
            <CardTitle className="text-base">{result.lender_name}</CardTitle>
            <p className="text-sm text-gray-500 mt-0.5">{result.program_name}</p>
          </div>
          <div className="flex flex-col items-end gap-1.5 flex-shrink-0">
            <Badge variant={result.is_eligible ? 'default' : 'destructive'}>
              {result.is_eligible ? 'Eligible' : 'Ineligible'}
            </Badge>
            <span className="text-xs text-gray-500">
              {result.match_score}% fit · {passedCount}/{totalCount} criteria
            </span>
          </div>
        </div>

        {/* Score bar */}
        <div className="mt-3 h-1.5 bg-gray-100 rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full transition-all
              ${result.match_score >= 80 ? 'bg-green-500' : result.match_score >= 50 ? 'bg-yellow-400' : 'bg-red-400'}
            `}
            style={{ width: `${result.match_score}%` }}
          />
        </div>
      </CardHeader>

      <CardContent className="pt-0">
        <div className="space-y-0">
          {result.criteria_results.map((criterion, i) => (
            <CriterionRow key={i} criterion={criterion} />
          ))}
        </div>
      </CardContent>
    </Card>
  )
}

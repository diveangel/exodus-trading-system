'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { DashboardLayout } from '@/components/layout/DashboardLayout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { PlayCircle, Clock, CheckCircle, XCircle } from 'lucide-react'
import {
  BacktestResult,
  BACKTEST_STATUS_LABELS,
  BACKTEST_STATUS_COLORS,
} from '@/types/backtest'

const backtestSchema = z.object({
  strategy_id: z.string().min(1, '전략을 선택해주세요'),
  start_date: z.string().min(1, '시작일을 선택해주세요'),
  end_date: z.string().min(1, '종료일을 선택해주세요'),
  initial_capital: z.number().min(100000, '최소 100,000원 이상 입력해주세요'),
  commission_rate: z.number().min(0).max(1),
  slippage_rate: z.number().min(0).max(1),
})

type BacktestFormData = z.infer<typeof backtestSchema>

export default function BacktestPage() {
  const router = useRouter()
  const [isRunning, setIsRunning] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<BacktestFormData>({
    resolver: zodResolver(backtestSchema),
    defaultValues: {
      initial_capital: 10000000,
      commission_rate: 0.00015,
      slippage_rate: 0.0001,
    },
  })

  // TODO: Fetch strategies from API
  const strategies = [
    { id: 1, name: '모멘텀 전략 A' },
    { id: 2, name: '평균회귀 전략 B' },
    { id: 3, name: '변동성 돌파 전략 C' },
  ]

  // TODO: Fetch backtest history from API
  const backtestHistory: BacktestResult[] = [
    {
      id: 1,
      strategy_id: 1,
      strategy_name: '모멘텀 전략 A',
      status: 'completed',
      config: {
        strategy_id: 1,
        start_date: '2023-01-01',
        end_date: '2023-12-31',
        initial_capital: 10000000,
        commission_rate: 0.00015,
        slippage_rate: 0.0001,
      },
      created_at: '2024-01-20T10:00:00Z',
      completed_at: '2024-01-20T10:05:23Z',
      total_return: 523000,
      total_return_percent: 5.23,
      annualized_return: 5.23,
      sharpe_ratio: 1.85,
      max_drawdown: -8.2,
      win_rate: 62.5,
      total_trades: 45,
    },
    {
      id: 2,
      strategy_id: 2,
      strategy_name: '평균회귀 전략 B',
      status: 'completed',
      config: {
        strategy_id: 2,
        start_date: '2023-06-01',
        end_date: '2023-12-31',
        initial_capital: 10000000,
        commission_rate: 0.00015,
        slippage_rate: 0.0001,
      },
      created_at: '2024-01-19T14:30:00Z',
      completed_at: '2024-01-19T14:33:45Z',
      total_return: 189000,
      total_return_percent: 1.89,
      annualized_return: 3.62,
      sharpe_ratio: 1.62,
      max_drawdown: -5.8,
      win_rate: 58.3,
      total_trades: 38,
    },
    {
      id: 3,
      strategy_id: 1,
      strategy_name: '모멘텀 전략 A',
      status: 'running',
      config: {
        strategy_id: 1,
        start_date: '2022-01-01',
        end_date: '2023-12-31',
        initial_capital: 10000000,
        commission_rate: 0.00015,
        slippage_rate: 0.0001,
      },
      created_at: '2024-01-21T09:15:00Z',
      started_at: '2024-01-21T09:15:30Z',
    },
    {
      id: 4,
      strategy_id: 3,
      strategy_name: '변동성 돌파 전략 C',
      status: 'failed',
      config: {
        strategy_id: 3,
        start_date: '2023-01-01',
        end_date: '2023-12-31',
        initial_capital: 10000000,
        commission_rate: 0.00015,
        slippage_rate: 0.0001,
      },
      created_at: '2024-01-18T16:20:00Z',
      error_message: '데이터 로딩 실패: 시장 데이터를 찾을 수 없습니다.',
    },
  ]

  const onSubmit = async (data: BacktestFormData) => {
    setIsRunning(true)
    try {
      // TODO: Call API to run backtest
      console.log('Running backtest:', data)

      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 2000))

      // Redirect to results page
      router.push('/backtest/1')
    } catch (error) {
      console.error('Failed to run backtest:', error)
    } finally {
      setIsRunning(false)
    }
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('ko-KR', {
      style: 'currency',
      currency: 'KRW',
      maximumFractionDigits: 0,
    }).format(amount)
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('ko-KR', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  const handleViewResult = (id: number) => {
    router.push(`/backtest/${id}`)
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Page Header */}
        <div>
          <h1 className="text-3xl font-bold tracking-tight">백테스트</h1>
          <p className="text-muted-foreground">
            전략의 과거 성과를 시뮬레이션하고 분석하세요
          </p>
        </div>

        {/* Backtest Configuration */}
        <Card>
          <CardHeader>
            <CardTitle>백테스트 실행</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              {/* Strategy Selection */}
              <div className="space-y-2">
                <Label htmlFor="strategy_id">전략 선택 *</Label>
                <select
                  id="strategy_id"
                  className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  {...register('strategy_id')}
                >
                  <option value="">전략을 선택하세요</option>
                  {strategies.map((strategy) => (
                    <option key={strategy.id} value={strategy.id}>
                      {strategy.name}
                    </option>
                  ))}
                </select>
                {errors.strategy_id && (
                  <p className="text-sm text-red-600">
                    {errors.strategy_id.message}
                  </p>
                )}
              </div>

              {/* Date Range */}
              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="start_date">시작일 *</Label>
                  <Input
                    id="start_date"
                    type="date"
                    {...register('start_date')}
                  />
                  {errors.start_date && (
                    <p className="text-sm text-red-600">
                      {errors.start_date.message}
                    </p>
                  )}
                </div>
                <div className="space-y-2">
                  <Label htmlFor="end_date">종료일 *</Label>
                  <Input id="end_date" type="date" {...register('end_date')} />
                  {errors.end_date && (
                    <p className="text-sm text-red-600">
                      {errors.end_date.message}
                    </p>
                  )}
                </div>
              </div>

              {/* Initial Capital */}
              <div className="space-y-2">
                <Label htmlFor="initial_capital">초기 자본금 (원) *</Label>
                <Input
                  id="initial_capital"
                  type="number"
                  step="100000"
                  {...register('initial_capital', { valueAsNumber: true })}
                />
                {errors.initial_capital && (
                  <p className="text-sm text-red-600">
                    {errors.initial_capital.message}
                  </p>
                )}
              </div>

              {/* Advanced Settings */}
              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="commission_rate">수수료율 (%)</Label>
                  <Input
                    id="commission_rate"
                    type="number"
                    step="0.00001"
                    {...register('commission_rate', { valueAsNumber: true })}
                  />
                  <p className="text-xs text-muted-foreground">
                    기본값: 0.015% (매수/매도 각각)
                  </p>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="slippage_rate">슬리피지율 (%)</Label>
                  <Input
                    id="slippage_rate"
                    type="number"
                    step="0.00001"
                    {...register('slippage_rate', { valueAsNumber: true })}
                  />
                  <p className="text-xs text-muted-foreground">
                    기본값: 0.01% (시장가 주문 시)
                  </p>
                </div>
              </div>

              {/* Submit Button */}
              <div className="flex justify-end">
                <Button
                  type="submit"
                  disabled={isRunning}
                  className="flex items-center gap-2"
                >
                  {isRunning ? (
                    <>
                      <Clock className="h-4 w-4 animate-spin" />
                      실행 중...
                    </>
                  ) : (
                    <>
                      <PlayCircle className="h-4 w-4" />
                      백테스트 실행
                    </>
                  )}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>

        {/* Backtest History */}
        <Card>
          <CardHeader>
            <CardTitle>백테스트 히스토리</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {backtestHistory.map((result) => (
                <div
                  key={result.id}
                  className="flex items-center justify-between border-b pb-4 last:border-0 last:pb-0"
                >
                  <div className="flex-1 space-y-2">
                    <div className="flex items-center gap-3">
                      <h4 className="font-semibold">{result.strategy_name}</h4>
                      <span
                        className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                          BACKTEST_STATUS_COLORS[result.status]
                        }`}
                      >
                        {result.status === 'running' && (
                          <Clock className="mr-1 h-3 w-3 animate-spin" />
                        )}
                        {result.status === 'completed' && (
                          <CheckCircle className="mr-1 h-3 w-3" />
                        )}
                        {result.status === 'failed' && (
                          <XCircle className="mr-1 h-3 w-3" />
                        )}
                        {BACKTEST_STATUS_LABELS[result.status]}
                      </span>
                    </div>
                    <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                      <span>
                        기간: {result.config.start_date} ~ {result.config.end_date}
                      </span>
                      <span>
                        자본금: {formatCurrency(result.config.initial_capital)}
                      </span>
                      <span>실행: {formatDate(result.created_at)}</span>
                    </div>
                    {result.status === 'completed' && (
                      <div className="flex flex-wrap gap-4 text-sm">
                        <span
                          className={
                            (result.total_return_percent ?? 0) >= 0
                              ? 'text-green-600 font-semibold'
                              : 'text-red-600 font-semibold'
                          }
                        >
                          수익률: {result.total_return_percent?.toFixed(2)}%
                        </span>
                        <span>샤프: {result.sharpe_ratio?.toFixed(2)}</span>
                        <span>승률: {result.win_rate?.toFixed(1)}%</span>
                        <span className="text-red-600">
                          MDD: {result.max_drawdown?.toFixed(1)}%
                        </span>
                      </div>
                    )}
                    {result.status === 'failed' && (
                      <p className="text-sm text-red-600">
                        {result.error_message}
                      </p>
                    )}
                  </div>
                  {result.status === 'completed' && (
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleViewResult(result.id)}
                    >
                      결과 보기
                    </Button>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  )
}

'use client'

import { useState, useEffect } from 'react'
import { useRouter, useParams } from 'next/navigation'
import { DashboardLayout } from '@/components/layout/DashboardLayout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import {
  ArrowLeft,
  Play,
  Pause,
  StopCircle,
  Edit,
  Trash2,
  TrendingUp,
  TrendingDown,
  Loader2,
  AlertCircle,
} from 'lucide-react'
import {
  Strategy,
  ExecuteStrategyResponse,
  STRATEGY_TYPE_LABELS,
  STRATEGY_STATUS_LABELS,
  STRATEGY_STATUS_COLORS,
} from '@/types/strategy'
import { Stock } from '@/types/stock'
import { strategyApi } from '@/lib/strategyApi'
import { MultiStockSelector } from '@/components/strategy/MultiStockSelector'

export default function StrategyDetailPage() {
  const router = useRouter()
  const params = useParams()
  const strategyId = parseInt(params.id as string)

  const [strategy, setStrategy] = useState<Strategy | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Strategy execution states
  const [selectedStocks, setSelectedStocks] = useState<Stock[]>([])
  const [isExecuting, setIsExecuting] = useState(false)
  const [executionResult, setExecutionResult] = useState<ExecuteStrategyResponse | null>(null)
  const [executionError, setExecutionError] = useState<string | null>(null)

  useEffect(() => {
    const fetchStrategy = async () => {
      try {
        setError(null)
        const data = await strategyApi.getStrategy(strategyId)
        setStrategy(data)
      } catch (err: any) {
        console.error('Failed to fetch strategy:', err)
        setError(err.response?.data?.detail || '전략 정보를 불러오는데 실패했습니다.')
      } finally {
        setIsLoading(false)
      }
    }

    fetchStrategy()
  }, [strategyId])

  const handleActivate = async () => {
    if (!strategy) return
    try {
      const updated = await strategyApi.activateStrategy(strategy.id)
      setStrategy(updated)
    } catch (err: any) {
      alert(err.response?.data?.detail || '전략 활성화에 실패했습니다.')
    }
  }

  const handleDeactivate = async () => {
    if (!strategy) return
    try {
      const updated = await strategyApi.deactivateStrategy(strategy.id)
      setStrategy(updated)
    } catch (err: any) {
      alert(err.response?.data?.detail || '전략 비활성화에 실패했습니다.')
    }
  }

  const handleDelete = async () => {
    if (!strategy) return
    if (!confirm('정말로 이 전략을 삭제하시겠습니까?')) return

    try {
      await strategyApi.deleteStrategy(strategy.id)
      router.push('/strategies')
    } catch (err: any) {
      alert(err.response?.data?.detail || '전략 삭제에 실패했습니다.')
    }
  }

  if (isLoading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-96">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
        </div>
      </DashboardLayout>
    )
  }

  if (error || !strategy) {
    return (
      <DashboardLayout>
        <div className="space-y-6">
          <Button
            variant="ghost"
            onClick={() => router.push('/strategies')}
            className="flex items-center gap-2"
          >
            <ArrowLeft className="h-4 w-4" />
            전략 목록으로
          </Button>
          <Card>
            <CardContent className="pt-6">
              <div className="flex flex-col items-center justify-center py-12">
                <AlertCircle className="h-12 w-12 text-red-500 mb-4" />
                <p className="text-lg font-semibold mb-2">전략을 불러올 수 없습니다</p>
                <p className="text-sm text-muted-foreground mb-4">{error}</p>
                <Button onClick={() => router.push('/strategies')}>
                  전략 목록으로
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </DashboardLayout>
    )
  }

  const recentTrades = [
    {
      id: 1,
      type: 'BUY',
      symbol: '삼성전자',
      quantity: 10,
      price: 71000,
      executed_at: '2024-01-20T10:23:15Z',
      profit_loss: null,
    },
    {
      id: 2,
      type: 'SELL',
      symbol: 'SK하이닉스',
      quantity: 5,
      price: 132000,
      executed_at: '2024-01-20T09:45:32Z',
      profit_loss: 25000,
    },
    {
      id: 3,
      type: 'BUY',
      symbol: 'NAVER',
      quantity: 8,
      price: 205000,
      executed_at: '2024-01-19T14:12:08Z',
      profit_loss: null,
    },
    {
      id: 4,
      type: 'SELL',
      symbol: 'LG화학',
      quantity: 3,
      price: 420000,
      executed_at: '2024-01-19T11:30:45Z',
      profit_loss: -15000,
    },
  ]

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

  const handleEdit = () => {
    router.push(`/strategies/${strategyId}/edit`)
  }

  const handleExecuteStrategy = async () => {
    if (!strategy || selectedStocks.length === 0) return

    setIsExecuting(true)
    setExecutionError(null)

    try {
      const symbols = selectedStocks.map(stock => stock.symbol)
      const result = await strategyApi.executeStrategy(strategy.id, symbols)
      setExecutionResult(result)
    } catch (err: any) {
      console.error('Strategy execution error:', err)
      setExecutionError(err.response?.data?.detail || '전략 실행 중 오류가 발생했습니다.')
    } finally {
      setIsExecuting(false)
    }
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Page Header */}
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="icon" onClick={() => router.back()}>
              <ArrowLeft className="h-5 w-5" />
            </Button>
            <div>
              <div className="flex items-center gap-3 mb-2">
                <h1 className="text-3xl font-bold tracking-tight">
                  {strategy.name}
                </h1>
                <span
                  className={`inline-flex items-center rounded-full px-3 py-1 text-sm font-medium ${
                    STRATEGY_STATUS_COLORS[strategy.status]
                  }`}
                >
                  {STRATEGY_STATUS_LABELS[strategy.status]}
                </span>
                <span className="inline-flex items-center rounded-full bg-blue-100 px-3 py-1 text-sm font-medium text-blue-700">
                  {STRATEGY_TYPE_LABELS[strategy.strategy_type]}
                </span>
              </div>
              {strategy.description && (
                <p className="text-muted-foreground">{strategy.description}</p>
              )}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-2">
            {strategy.status === 'ACTIVE' && (
              <Button
                variant="outline"
                size="sm"
                onClick={handleDeactivate}
                className="flex items-center gap-2"
              >
                <Pause className="h-4 w-4" />
                비활성화
              </Button>
            )}
            {(strategy.status === 'INACTIVE' || strategy.status === 'BACKTESTING') && (
              <Button
                variant="default"
                size="sm"
                onClick={handleActivate}
                className="flex items-center gap-2"
              >
                <Play className="h-4 w-4" />
                활성화
              </Button>
            )}
            <Button
              variant="outline"
              size="sm"
              onClick={handleEdit}
              className="flex items-center gap-2"
            >
              <Edit className="h-4 w-4" />
              수정
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={handleDelete}
              className="flex items-center gap-2 text-red-600 hover:text-red-700"
            >
              <Trash2 className="h-4 w-4" />
              삭제
            </Button>
          </div>
        </div>

        {/* Performance Metrics */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">총 수익/손실</CardTitle>
              {(strategy.total_profit_loss ?? 0) >= 0 ? (
                <TrendingUp className="h-4 w-4 text-green-600" />
              ) : (
                <TrendingDown className="h-4 w-4 text-red-600" />
              )}
            </CardHeader>
            <CardContent>
              <div
                className={`text-2xl font-bold ${
                  (strategy.total_profit_loss ?? 0) >= 0
                    ? 'text-green-600'
                    : 'text-red-600'
                }`}
              >
                {formatCurrency(strategy.total_profit_loss ?? 0)}
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                <span
                  className={
                    (strategy.profit_loss_percent ?? 0) >= 0
                      ? 'text-green-600'
                      : 'text-red-600'
                  }
                >
                  {(strategy.profit_loss_percent ?? 0) >= 0 ? '+' : ''}
                  {strategy.profit_loss_percent?.toFixed(2)}%
                </span>{' '}
                수익률
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">총 거래</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {strategy.total_trades ?? 0}
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                승률: {strategy.win_rate?.toFixed(1)}%
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">샤프 지수</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {strategy.sharpe_ratio?.toFixed(2)}
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                위험 대비 수익
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">최대 낙폭</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-red-600">
                {strategy.max_drawdown?.toFixed(1)}%
              </div>
              <p className="text-xs text-muted-foreground mt-1">MDD</p>
            </CardContent>
          </Card>
        </div>

        {/* Strategy Execution Section */}
        <Card>
          <CardHeader>
            <CardTitle>전략 실행</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <MultiStockSelector
              selectedStocks={selectedStocks}
              onStocksChange={setSelectedStocks}
            />

            <Button
              onClick={handleExecuteStrategy}
              disabled={selectedStocks.length === 0 || isExecuting}
              className="w-full"
            >
              {isExecuting ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  실행 중...
                </>
              ) : (
                <>
                  <Play className="mr-2 h-4 w-4" />
                  전략 실행 ({selectedStocks.length}개 종목)
                </>
              )}
            </Button>

            {executionError && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-md">
                <p className="text-sm text-red-600">{executionError}</p>
              </div>
            )}

            {executionResult && (
              <div className="space-y-3 p-4 bg-muted rounded-md">
                <h4 className="font-semibold">실행 결과</h4>
                <div className="space-y-2">
                  <div className="flex justify-between border-b pb-2">
                    <span className="text-sm text-muted-foreground">전략</span>
                    <span className="text-sm font-medium">
                      {executionResult.strategy_name}
                    </span>
                  </div>
                  <div className="flex justify-between border-b pb-2">
                    <span className="text-sm text-muted-foreground">분석 종목</span>
                    <span className="text-sm font-medium">
                      {executionResult.total_symbols}개
                    </span>
                  </div>
                  <div className="flex justify-between border-b pb-2">
                    <span className="text-sm text-muted-foreground">총 신호 개수</span>
                    <span className="text-sm font-medium">
                      {executionResult.total_signals}개
                    </span>
                  </div>
                  <div className="pt-2 text-xs text-muted-foreground">
                    실행 시각: {formatDate(executionResult.executed_at)}
                  </div>
                </div>

                {executionResult.signals.length > 0 && (
                  <div className="mt-4 space-y-3">
                    <h5 className="font-medium">생성된 신호</h5>
                    {executionResult.signals.map((signal, index) => (
                      <div key={index} className="p-3 border rounded-md bg-background">
                        <div className="space-y-2">
                          <div className="flex justify-between border-b pb-2">
                            <span className="text-sm text-muted-foreground">
                              {signal.symbol}
                            </span>
                            <span
                              className={`text-sm font-semibold ${
                                signal.signal_type === 'BUY'
                                  ? 'text-blue-600'
                                  : signal.signal_type === 'SELL'
                                  ? 'text-red-600'
                                  : 'text-gray-600'
                              }`}
                            >
                              {signal.signal_type === 'BUY'
                                ? '매수'
                                : signal.signal_type === 'SELL'
                                ? '매도'
                                : '홀드'}
                            </span>
                          </div>
                          <div className="flex justify-between border-b pb-2">
                            <span className="text-sm text-muted-foreground">가격</span>
                            <span className="text-sm font-medium">
                              {formatCurrency(signal.price)}
                            </span>
                          </div>
                          {signal.quantity && (
                            <div className="flex justify-between border-b pb-2">
                              <span className="text-sm text-muted-foreground">수량</span>
                              <span className="text-sm font-medium">
                                {signal.quantity.toLocaleString()}주
                              </span>
                            </div>
                          )}
                          <div className="flex justify-between border-b pb-2">
                            <span className="text-sm text-muted-foreground">신뢰도</span>
                            <span className="text-sm font-medium">
                              {(signal.confidence * 100).toFixed(1)}%
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-sm text-muted-foreground">사유</span>
                            <span className="text-sm font-medium text-right ml-2">
                              {signal.reason}
                            </span>
                          </div>
                          <div className="pt-1 text-xs text-muted-foreground">
                            {formatDate(signal.timestamp)}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {executionResult.signals.length === 0 && (
                  <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-md">
                    <p className="text-sm text-yellow-800">
                      선택한 종목에서 매매 신호가 생성되지 않았습니다.
                    </p>
                  </div>
                )}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Performance Chart Placeholder */}
        <Card>
          <CardHeader>
            <CardTitle>수익률 차트</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex h-64 items-center justify-center border-2 border-dashed rounded-lg">
              <p className="text-muted-foreground">
                차트 구현 예정 (Chart.js 또는 Recharts 사용)
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Two Column Layout */}
        <div className="grid gap-6 md:grid-cols-2">
          {/* Strategy Parameters */}
          <Card>
            <CardHeader>
              <CardTitle>전략 파라미터</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {Object.entries(strategy.parameters).map(([key, value]) => (
                  <div
                    key={key}
                    className="flex justify-between border-b pb-2 last:border-0"
                  >
                    <span className="text-sm text-muted-foreground">
                      {key.replace(/_/g, ' ')}
                    </span>
                    <span className="text-sm font-medium">
                      {typeof value === 'number'
                        ? value.toLocaleString()
                        : String(value)}
                    </span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Strategy Info */}
          <Card>
            <CardHeader>
              <CardTitle>전략 정보</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex justify-between border-b pb-2">
                  <span className="text-sm text-muted-foreground">생성일</span>
                  <span className="text-sm font-medium">
                    {formatDate(strategy.created_at)}
                  </span>
                </div>
                <div className="flex justify-between border-b pb-2">
                  <span className="text-sm text-muted-foreground">
                    마지막 수정
                  </span>
                  <span className="text-sm font-medium">
                    {formatDate(strategy.updated_at)}
                  </span>
                </div>
                <div className="flex justify-between border-b pb-2">
                  <span className="text-sm text-muted-foreground">전략 ID</span>
                  <span className="text-sm font-medium">{strategy.id}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">활성 상태</span>
                  <span className="text-sm font-medium">
                    {STRATEGY_STATUS_LABELS[strategy.status]}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Recent Trades */}
        <Card>
          <CardHeader>
            <CardTitle>최근 거래 내역</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentTrades.map((trade) => (
                <div
                  key={trade.id}
                  className="flex items-center justify-between border-b pb-3 last:border-0 last:pb-0"
                >
                  <div className="flex items-center gap-4 flex-1">
                    <span
                      className={`inline-flex items-center rounded px-2.5 py-1 text-xs font-semibold ${
                        trade.type === 'BUY'
                          ? 'bg-blue-100 text-blue-700'
                          : 'bg-red-100 text-red-700'
                      }`}
                    >
                      {trade.type === 'BUY' ? '매수' : '매도'}
                    </span>
                    <div className="flex-1">
                      <p className="font-medium">{trade.symbol}</p>
                      <p className="text-sm text-muted-foreground">
                        {trade.quantity}주 @ {formatCurrency(trade.price)}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-muted-foreground">
                        {formatDate(trade.executed_at)}
                      </p>
                      {trade.profit_loss !== null && (
                        <p
                          className={`text-sm font-semibold ${
                            trade.profit_loss >= 0
                              ? 'text-green-600'
                              : 'text-red-600'
                          }`}
                        >
                          {trade.profit_loss >= 0 ? '+' : ''}
                          {formatCurrency(trade.profit_loss)}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  )
}

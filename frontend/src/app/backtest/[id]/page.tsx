'use client'

import { useRouter, useParams } from 'next/navigation'
import { DashboardLayout } from '@/components/layout/DashboardLayout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import {
  ArrowLeft,
  TrendingUp,
  TrendingDown,
  Download,
} from 'lucide-react'
import {
  BacktestResult,
  BacktestTrade,
  BACKTEST_STATUS_LABELS,
  BACKTEST_STATUS_COLORS,
} from '@/types/backtest'

export default function BacktestResultPage() {
  const router = useRouter()
  const params = useParams()
  const backtestId = params.id as string

  // TODO: Fetch backtest result from API
  const result: BacktestResult = {
    id: parseInt(backtestId),
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
    started_at: '2024-01-20T10:00:30Z',
    completed_at: '2024-01-20T10:05:23Z',
    total_return: 523000,
    total_return_percent: 5.23,
    annualized_return: 5.23,
    sharpe_ratio: 1.85,
    sortino_ratio: 2.12,
    max_drawdown: -8.2,
    max_drawdown_duration: 45,
    win_rate: 62.5,
    profit_factor: 2.15,
    total_trades: 45,
    winning_trades: 28,
    losing_trades: 17,
    avg_win: 35000,
    avg_loss: -18000,
  }

  // TODO: Fetch trades from API
  const trades: BacktestTrade[] = [
    {
      id: 1,
      backtest_id: parseInt(backtestId),
      symbol: '삼성전자',
      side: 'BUY',
      quantity: 15,
      price: 68000,
      executed_at: '2023-01-15T09:30:00Z',
      position_type: 'OPEN',
    },
    {
      id: 2,
      backtest_id: parseInt(backtestId),
      symbol: '삼성전자',
      side: 'SELL',
      quantity: 15,
      price: 71000,
      executed_at: '2023-01-25T14:20:00Z',
      profit_loss: 45000,
      profit_loss_percent: 4.41,
      position_type: 'CLOSE',
    },
    {
      id: 3,
      backtest_id: parseInt(backtestId),
      symbol: 'SK하이닉스',
      side: 'BUY',
      quantity: 8,
      price: 125000,
      executed_at: '2023-02-10T10:15:00Z',
      position_type: 'OPEN',
    },
    {
      id: 4,
      backtest_id: parseInt(backtestId),
      symbol: 'SK하이닉스',
      side: 'SELL',
      quantity: 8,
      price: 132000,
      executed_at: '2023-02-28T15:45:00Z',
      profit_loss: 56000,
      profit_loss_percent: 5.6,
      position_type: 'CLOSE',
    },
    {
      id: 5,
      backtest_id: parseInt(backtestId),
      symbol: 'NAVER',
      side: 'BUY',
      quantity: 5,
      price: 210000,
      executed_at: '2023-03-05T11:20:00Z',
      position_type: 'OPEN',
    },
    {
      id: 6,
      backtest_id: parseInt(backtestId),
      symbol: 'NAVER',
      side: 'SELL',
      quantity: 5,
      price: 205000,
      executed_at: '2023-03-20T13:10:00Z',
      profit_loss: -25000,
      profit_loss_percent: -2.38,
      position_type: 'CLOSE',
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

  const handleExport = () => {
    // TODO: Export results to CSV or PDF
    console.log('Exporting backtest results...')
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
                  백테스트 결과
                </h1>
                <span
                  className={`inline-flex items-center rounded-full px-3 py-1 text-sm font-medium ${
                    BACKTEST_STATUS_COLORS[result.status]
                  }`}
                >
                  {BACKTEST_STATUS_LABELS[result.status]}
                </span>
              </div>
              <p className="text-muted-foreground">{result.strategy_name}</p>
            </div>
          </div>

          <Button
            variant="outline"
            onClick={handleExport}
            className="flex items-center gap-2"
          >
            <Download className="h-4 w-4" />
            결과 내보내기
          </Button>
        </div>

        {/* Configuration Summary */}
        <Card>
          <CardHeader>
            <CardTitle>백테스트 설정</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              <div>
                <p className="text-sm text-muted-foreground">기간</p>
                <p className="font-medium">
                  {result.config.start_date} ~ {result.config.end_date}
                </p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">초기 자본금</p>
                <p className="font-medium">
                  {formatCurrency(result.config.initial_capital)}
                </p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">수수료율</p>
                <p className="font-medium">
                  {(result.config.commission_rate * 100).toFixed(3)}%
                </p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">슬리피지율</p>
                <p className="font-medium">
                  {(result.config.slippage_rate * 100).toFixed(3)}%
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Performance Summary */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">총 수익</CardTitle>
              {(result.total_return ?? 0) >= 0 ? (
                <TrendingUp className="h-4 w-4 text-green-600" />
              ) : (
                <TrendingDown className="h-4 w-4 text-red-600" />
              )}
            </CardHeader>
            <CardContent>
              <div
                className={`text-2xl font-bold ${
                  (result.total_return ?? 0) >= 0
                    ? 'text-green-600'
                    : 'text-red-600'
                }`}
              >
                {formatCurrency(result.total_return ?? 0)}
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                <span
                  className={
                    (result.total_return_percent ?? 0) >= 0
                      ? 'text-green-600'
                      : 'text-red-600'
                  }
                >
                  {(result.total_return_percent ?? 0) >= 0 ? '+' : ''}
                  {result.total_return_percent?.toFixed(2)}%
                </span>{' '}
                수익률
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">연환산 수익률</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {result.annualized_return?.toFixed(2)}%
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                CAGR (연평균 성장률)
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">샤프 지수</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {result.sharpe_ratio?.toFixed(2)}
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                소르티노: {result.sortino_ratio?.toFixed(2)}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">최대 낙폭</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-red-600">
                {result.max_drawdown?.toFixed(2)}%
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                기간: {result.max_drawdown_duration}일
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Trading Statistics */}
        <Card>
          <CardHeader>
            <CardTitle>거래 통계</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              <div className="border-r pr-4 last:border-0">
                <p className="text-sm text-muted-foreground mb-1">총 거래</p>
                <p className="text-2xl font-bold">{result.total_trades}</p>
              </div>
              <div className="border-r pr-4 last:border-0">
                <p className="text-sm text-muted-foreground mb-1">승률</p>
                <p className="text-2xl font-bold text-green-600">
                  {result.win_rate?.toFixed(1)}%
                </p>
              </div>
              <div className="border-r pr-4 last:border-0">
                <p className="text-sm text-muted-foreground mb-1">승/패</p>
                <p className="text-xl font-bold">
                  <span className="text-green-600">{result.winning_trades}</span>
                  {' / '}
                  <span className="text-red-600">{result.losing_trades}</span>
                </p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground mb-1">손익비</p>
                <p className="text-2xl font-bold">
                  {result.profit_factor?.toFixed(2)}
                </p>
              </div>
            </div>
            <div className="grid gap-4 md:grid-cols-2 mt-4 pt-4 border-t">
              <div>
                <p className="text-sm text-muted-foreground mb-1">
                  평균 수익 (승)
                </p>
                <p className="text-xl font-semibold text-green-600">
                  {formatCurrency(result.avg_win ?? 0)}
                </p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground mb-1">
                  평균 손실 (패)
                </p>
                <p className="text-xl font-semibold text-red-600">
                  {formatCurrency(result.avg_loss ?? 0)}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Equity Curve Placeholder */}
        <Card>
          <CardHeader>
            <CardTitle>자산 곡선 (Equity Curve)</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex h-80 items-center justify-center border-2 border-dashed rounded-lg">
              <p className="text-muted-foreground">
                차트 구현 예정 (Recharts 사용)
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Trade History */}
        <Card>
          <CardHeader>
            <CardTitle>거래 내역</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-3 px-2 text-sm font-medium text-muted-foreground">
                      일시
                    </th>
                    <th className="text-left py-3 px-2 text-sm font-medium text-muted-foreground">
                      종목
                    </th>
                    <th className="text-center py-3 px-2 text-sm font-medium text-muted-foreground">
                      구분
                    </th>
                    <th className="text-right py-3 px-2 text-sm font-medium text-muted-foreground">
                      수량
                    </th>
                    <th className="text-right py-3 px-2 text-sm font-medium text-muted-foreground">
                      가격
                    </th>
                    <th className="text-right py-3 px-2 text-sm font-medium text-muted-foreground">
                      손익
                    </th>
                    <th className="text-right py-3 px-2 text-sm font-medium text-muted-foreground">
                      수익률
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {trades.map((trade) => (
                    <tr key={trade.id} className="border-b last:border-0">
                      <td className="py-3 px-2 text-sm">
                        {formatDate(trade.executed_at)}
                      </td>
                      <td className="py-3 px-2 text-sm font-medium">
                        {trade.symbol}
                      </td>
                      <td className="py-3 px-2 text-center">
                        <span
                          className={`inline-flex items-center rounded px-2 py-0.5 text-xs font-semibold ${
                            trade.side === 'BUY'
                              ? 'bg-blue-100 text-blue-700'
                              : 'bg-red-100 text-red-700'
                          }`}
                        >
                          {trade.side === 'BUY' ? '매수' : '매도'}
                        </span>
                      </td>
                      <td className="py-3 px-2 text-sm text-right">
                        {trade.quantity}주
                      </td>
                      <td className="py-3 px-2 text-sm text-right">
                        {formatCurrency(trade.price)}
                      </td>
                      <td
                        className={`py-3 px-2 text-sm text-right font-semibold ${
                          trade.profit_loss
                            ? trade.profit_loss >= 0
                              ? 'text-green-600'
                              : 'text-red-600'
                            : ''
                        }`}
                      >
                        {trade.profit_loss
                          ? formatCurrency(trade.profit_loss)
                          : '-'}
                      </td>
                      <td
                        className={`py-3 px-2 text-sm text-right font-semibold ${
                          trade.profit_loss_percent
                            ? trade.profit_loss_percent >= 0
                              ? 'text-green-600'
                              : 'text-red-600'
                            : ''
                        }`}
                      >
                        {trade.profit_loss_percent
                          ? `${
                              trade.profit_loss_percent >= 0 ? '+' : ''
                            }${trade.profit_loss_percent.toFixed(2)}%`
                          : '-'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  )
}

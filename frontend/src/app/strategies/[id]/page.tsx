'use client'

import { useState } from 'react'
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
} from 'lucide-react'
import {
  Strategy,
  STRATEGY_TYPE_LABELS,
  STRATEGY_STATUS_LABELS,
  STRATEGY_STATUS_COLORS,
} from '@/types/strategy'

export default function StrategyDetailPage() {
  const router = useRouter()
  const params = useParams()
  const strategyId = params.id as string

  // TODO: Fetch strategy data from API
  const strategy: Strategy = {
    id: parseInt(strategyId),
    name: '모멘텀 전략 A',
    description: '20일 이동평균선을 활용한 모멘텀 전략',
    type: 'momentum',
    status: 'active',
    parameters: {
      period: 20,
      threshold: 0.02,
      max_position_size: 1000000,
      max_positions: 5,
      stop_loss_percent: 5.0,
      take_profit_percent: 10.0,
    },
    created_at: '2024-01-15T09:00:00Z',
    updated_at: '2024-01-20T14:30:00Z',
    user_id: 1,
    is_active: true,
    total_profit_loss: 234000,
    profit_loss_percent: 2.34,
    total_trades: 45,
    win_rate: 62.5,
    sharpe_ratio: 1.85,
    max_drawdown: -5.2,
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

  const handleStart = () => {
    // TODO: Call API to start strategy
    console.log('Starting strategy:', strategyId)
  }

  const handlePause = () => {
    // TODO: Call API to pause strategy
    console.log('Pausing strategy:', strategyId)
  }

  const handleStop = () => {
    // TODO: Call API to stop strategy
    console.log('Stopping strategy:', strategyId)
  }

  const handleEdit = () => {
    router.push(`/strategies/${strategyId}/edit`)
  }

  const handleDelete = () => {
    // TODO: Show confirmation dialog and delete strategy
    if (confirm('정말로 이 전략을 삭제하시겠습니까?')) {
      console.log('Deleting strategy:', strategyId)
      router.push('/strategies')
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
                  {STRATEGY_TYPE_LABELS[strategy.type]}
                </span>
              </div>
              <p className="text-muted-foreground">{strategy.description}</p>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-2">
            {strategy.status === 'active' && (
              <>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handlePause}
                  className="flex items-center gap-2"
                >
                  <Pause className="h-4 w-4" />
                  일시정지
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleStop}
                  className="flex items-center gap-2"
                >
                  <StopCircle className="h-4 w-4" />
                  중지
                </Button>
              </>
            )}
            {(strategy.status === 'paused' || strategy.status === 'stopped') && (
              <Button
                variant="default"
                size="sm"
                onClick={handleStart}
                className="flex items-center gap-2"
              >
                <Play className="h-4 w-4" />
                시작
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
                    {strategy.is_active ? '활성' : '비활성'}
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

'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { DashboardLayout } from '@/components/layout/DashboardLayout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import {
  Plus,
  Play,
  Pause,
  StopCircle,
  TrendingUp,
  TrendingDown,
  MoreVertical,
} from 'lucide-react'
import {
  Strategy,
  STRATEGY_TYPE_LABELS,
  STRATEGY_STATUS_LABELS,
  STRATEGY_STATUS_COLORS,
} from '@/types/strategy'

export default function StrategiesPage() {
  const router = useRouter()
  const [statusFilter, setStatusFilter] = useState<string>('all')

  // TODO: Replace with actual data from API
  const strategies: Strategy[] = [
    {
      id: 1,
      name: '모멘텀 전략 A',
      description: '20일 이동평균선을 활용한 모멘텀 전략',
      type: 'momentum',
      status: 'active',
      parameters: { period: 20, threshold: 0.02 },
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
    },
    {
      id: 2,
      name: '평균회귀 전략 B',
      description: 'RSI 기반 과매수/과매도 구간 매매 전략',
      type: 'mean_reversion',
      status: 'active',
      parameters: { rsi_period: 14, oversold: 30, overbought: 70 },
      created_at: '2024-01-10T10:00:00Z',
      updated_at: '2024-01-18T11:20:00Z',
      user_id: 1,
      is_active: true,
      total_profit_loss: 189000,
      profit_loss_percent: 1.89,
      total_trades: 38,
      win_rate: 58.3,
      sharpe_ratio: 1.62,
      max_drawdown: -4.8,
    },
    {
      id: 3,
      name: '변동성 돌파 전략 C',
      description: '전일 변동폭 기반 돌파 매매 전략',
      type: 'breakout',
      status: 'paused',
      parameters: { k: 0.5, stop_loss: 0.02 },
      created_at: '2024-01-05T08:30:00Z',
      updated_at: '2024-01-22T16:00:00Z',
      user_id: 1,
      is_active: false,
      total_profit_loss: 100000,
      profit_loss_percent: 1.0,
      total_trades: 25,
      win_rate: 55.0,
      sharpe_ratio: 1.45,
      max_drawdown: -6.1,
    },
    {
      id: 4,
      name: '차익거래 전략 D',
      description: '코스피-코스닥 지수 스프레드 전략',
      type: 'arbitrage',
      status: 'stopped',
      parameters: { threshold: 0.015 },
      created_at: '2023-12-20T15:00:00Z',
      updated_at: '2024-01-15T09:45:00Z',
      user_id: 1,
      is_active: false,
      total_profit_loss: -45000,
      profit_loss_percent: -0.45,
      total_trades: 18,
      win_rate: 44.4,
      sharpe_ratio: 0.82,
      max_drawdown: -8.3,
    },
  ]

  const filteredStrategies =
    statusFilter === 'all'
      ? strategies
      : strategies.filter((s) => s.status === statusFilter)

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('ko-KR', {
      style: 'currency',
      currency: 'KRW',
      maximumFractionDigits: 0,
    }).format(amount)
  }

  const handleStrategyClick = (id: number) => {
    router.push(`/strategies/${id}`)
  }

  const handleCreateStrategy = () => {
    router.push('/strategies/new')
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Page Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">전략 관리</h1>
            <p className="text-muted-foreground">
              트레이딩 전략을 생성하고 관리하세요
            </p>
          </div>
          <Button onClick={handleCreateStrategy} className="flex items-center gap-2">
            <Plus className="h-4 w-4" />
            새 전략 생성
          </Button>
        </div>

        {/* Filter Tabs */}
        <Card>
          <CardContent className="pt-6">
            <div className="flex flex-wrap gap-2">
              <Button
                variant={statusFilter === 'all' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setStatusFilter('all')}
              >
                전체
              </Button>
              <Button
                variant={statusFilter === 'active' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setStatusFilter('active')}
              >
                운영중
              </Button>
              <Button
                variant={statusFilter === 'paused' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setStatusFilter('paused')}
              >
                일시정지
              </Button>
              <Button
                variant={statusFilter === 'stopped' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setStatusFilter('stopped')}
              >
                중지됨
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Strategies List */}
        <div className="grid gap-4">
          {filteredStrategies.map((strategy) => (
            <Card
              key={strategy.id}
              className="cursor-pointer transition-shadow hover:shadow-md"
              onClick={() => handleStrategyClick(strategy.id)}
            >
              <CardContent className="pt-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1 space-y-3">
                    {/* Header */}
                    <div className="flex items-center gap-3">
                      <h3 className="text-lg font-semibold">{strategy.name}</h3>
                      <span
                        className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                          STRATEGY_STATUS_COLORS[strategy.status]
                        }`}
                      >
                        {STRATEGY_STATUS_LABELS[strategy.status]}
                      </span>
                      <span className="inline-flex items-center rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-700">
                        {STRATEGY_TYPE_LABELS[strategy.type]}
                      </span>
                    </div>

                    {/* Description */}
                    <p className="text-sm text-muted-foreground">
                      {strategy.description}
                    </p>

                    {/* Metrics */}
                    <div className="grid grid-cols-2 gap-4 md:grid-cols-4 lg:grid-cols-6">
                      <div>
                        <p className="text-xs text-muted-foreground">수익/손실</p>
                        <p
                          className={`text-sm font-semibold ${
                            (strategy.total_profit_loss ?? 0) >= 0
                              ? 'text-green-600'
                              : 'text-red-600'
                          }`}
                        >
                          {formatCurrency(strategy.total_profit_loss ?? 0)}
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-muted-foreground">수익률</p>
                        <p
                          className={`text-sm font-semibold ${
                            (strategy.profit_loss_percent ?? 0) >= 0
                              ? 'text-green-600'
                              : 'text-red-600'
                          }`}
                        >
                          {(strategy.profit_loss_percent ?? 0) >= 0 ? '+' : ''}
                          {strategy.profit_loss_percent?.toFixed(2)}%
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-muted-foreground">총 거래</p>
                        <p className="text-sm font-semibold">
                          {strategy.total_trades ?? 0}건
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-muted-foreground">승률</p>
                        <p className="text-sm font-semibold">
                          {strategy.win_rate?.toFixed(1)}%
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-muted-foreground">샤프지수</p>
                        <p className="text-sm font-semibold">
                          {strategy.sharpe_ratio?.toFixed(2)}
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-muted-foreground">최대 낙폭</p>
                        <p className="text-sm font-semibold text-red-600">
                          {strategy.max_drawdown?.toFixed(1)}%
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="ml-4 flex gap-2">
                    {strategy.status === 'active' && (
                      <Button
                        variant="outline"
                        size="icon"
                        onClick={(e) => {
                          e.stopPropagation()
                          // TODO: Pause strategy
                        }}
                      >
                        <Pause className="h-4 w-4" />
                      </Button>
                    )}
                    {(strategy.status === 'paused' ||
                      strategy.status === 'stopped') && (
                      <Button
                        variant="outline"
                        size="icon"
                        onClick={(e) => {
                          e.stopPropagation()
                          // TODO: Start strategy
                        }}
                      >
                        <Play className="h-4 w-4" />
                      </Button>
                    )}
                    {strategy.status === 'active' && (
                      <Button
                        variant="outline"
                        size="icon"
                        onClick={(e) => {
                          e.stopPropagation()
                          // TODO: Stop strategy
                        }}
                      >
                        <StopCircle className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Empty State */}
        {filteredStrategies.length === 0 && (
          <Card>
            <CardContent className="flex flex-col items-center justify-center py-12">
              <TrendingUp className="h-12 w-12 text-muted-foreground mb-4" />
              <p className="text-lg font-medium mb-2">전략이 없습니다</p>
              <p className="text-sm text-muted-foreground mb-4">
                새로운 트레이딩 전략을 생성해보세요
              </p>
              <Button onClick={handleCreateStrategy} className="flex items-center gap-2">
                <Plus className="h-4 w-4" />
                새 전략 생성
              </Button>
            </CardContent>
          </Card>
        )}
      </div>
    </DashboardLayout>
  )
}

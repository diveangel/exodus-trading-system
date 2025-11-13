'use client'

import { useState, useEffect } from 'react'
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
  Loader2,
  AlertCircle,
  RefreshCw,
} from 'lucide-react'
import {
  Strategy,
  StrategyStatus,
  STRATEGY_TYPE_LABELS,
  STRATEGY_STATUS_LABELS,
  STRATEGY_STATUS_COLORS,
} from '@/types/strategy'
import { strategyApi } from '@/lib/strategyApi'

export default function StrategiesPage() {
  const router = useRouter()
  const [statusFilter, setStatusFilter] = useState<StrategyStatus | 'all'>('all')
  const [strategies, setStrategies] = useState<Strategy[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isRefreshing, setIsRefreshing] = useState(false)

  const fetchStrategies = async () => {
    try {
      setError(null)
      const response = await strategyApi.listStrategies(
        1,
        100,
        statusFilter === 'all' ? undefined : statusFilter
      )
      setStrategies(response.strategies)
    } catch (err: any) {
      console.error('Failed to fetch strategies:', err)
      setError(err.response?.data?.detail || '전략 목록을 불러오는데 실패했습니다.')
    } finally {
      setIsLoading(false)
      setIsRefreshing(false)
    }
  }

  useEffect(() => {
    fetchStrategies()
  }, [statusFilter])

  const handleRefresh = async () => {
    setIsRefreshing(true)
    await fetchStrategies()
  }

  const handleActivate = async (strategyId: number, e: React.MouseEvent) => {
    e.stopPropagation()
    try {
      await strategyApi.activateStrategy(strategyId)
      await fetchStrategies()
    } catch (err: any) {
      console.error('Failed to activate strategy:', err)
      alert(err.response?.data?.detail || '전략 활성화에 실패했습니다.')
    }
  }

  const handleDeactivate = async (strategyId: number, e: React.MouseEvent) => {
    e.stopPropagation()
    try {
      await strategyApi.deactivateStrategy(strategyId)
      await fetchStrategies()
    } catch (err: any) {
      console.error('Failed to deactivate strategy:', err)
      alert(err.response?.data?.detail || '전략 비활성화에 실패했습니다.')
    }
  }

  const filteredStrategies = strategies

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

  if (isLoading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-96">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
        </div>
      </DashboardLayout>
    )
  }

  if (error) {
    return (
      <DashboardLayout>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">전략 관리</h1>
            <p className="text-muted-foreground">
              트레이딩 전략을 생성하고 관리하세요
            </p>
          </div>
          <Card>
            <CardContent className="pt-6">
              <div className="flex flex-col items-center justify-center py-12">
                <AlertCircle className="h-12 w-12 text-red-500 mb-4" />
                <p className="text-lg font-semibold mb-2">전략 목록을 불러올 수 없습니다</p>
                <p className="text-sm text-muted-foreground mb-4">{error}</p>
                <Button onClick={() => {
                  setError(null)
                  setIsLoading(true)
                  fetchStrategies()
                }}>
                  다시 시도
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </DashboardLayout>
    )
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
          <div className="flex gap-2">
            <Button
              variant="outline"
              onClick={handleRefresh}
              disabled={isRefreshing}
              className="flex items-center gap-2"
            >
              <RefreshCw className={`h-4 w-4 ${isRefreshing ? 'animate-spin' : ''}`} />
              새로고침
            </Button>
            <Button onClick={handleCreateStrategy} className="flex items-center gap-2">
              <Plus className="h-4 w-4" />
              새 전략 생성
            </Button>
          </div>
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
                variant={statusFilter === 'ACTIVE' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setStatusFilter('ACTIVE')}
              >
                운영중
              </Button>
              <Button
                variant={statusFilter === 'INACTIVE' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setStatusFilter('INACTIVE')}
              >
                비활성
              </Button>
              <Button
                variant={statusFilter === 'BACKTESTING' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setStatusFilter('BACKTESTING')}
              >
                백테스트중
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
                        {STRATEGY_TYPE_LABELS[strategy.strategy_type]}
                      </span>
                    </div>

                    {/* Description */}
                    {strategy.description && (
                      <p className="text-sm text-muted-foreground">
                        {strategy.description}
                      </p>
                    )}

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
                    {strategy.status === 'ACTIVE' && (
                      <Button
                        variant="outline"
                        size="icon"
                        onClick={(e) => handleDeactivate(strategy.id, e)}
                        title="비활성화"
                      >
                        <Pause className="h-4 w-4" />
                      </Button>
                    )}
                    {(strategy.status === 'INACTIVE' ||
                      strategy.status === 'BACKTESTING') && (
                      <Button
                        variant="outline"
                        size="icon"
                        onClick={(e) => handleActivate(strategy.id, e)}
                        title="활성화"
                      >
                        <Play className="h-4 w-4" />
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

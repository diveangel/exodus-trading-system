'use client'

import { useState, useEffect } from 'react'
import { DashboardLayout } from '@/components/layout/DashboardLayout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import {
  TrendingUp,
  TrendingDown,
  Wallet,
  Activity,
  BarChart3,
  Plus,
  PlayCircle,
  Loader2,
} from 'lucide-react'
import { dashboardApi } from '@/lib/dashboardApi'
import { DashboardData } from '@/types/dashboard'

export default function DashboardPage() {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        setIsLoading(true)
        console.log('🔄 Fetching dashboard data...')
        const data = await dashboardApi.getDashboard()
        console.log('✅ Dashboard data received:', data)
        setDashboardData(data)
      } catch (err: any) {
        console.error('❌ Dashboard API error:', err)
        setError(err.response?.data?.detail || '데이터를 불러오는데 실패했습니다.')
      } finally {
        setIsLoading(false)
      }
    }

    fetchDashboard()
  }, [])

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('ko-KR', {
      style: 'currency',
      currency: 'KRW',
    }).format(amount)
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

  if (error || !dashboardData) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-96">
          <p className="text-red-500">{error || '데이터를 불러오는데 실패했습니다.'}</p>
        </div>
      </DashboardLayout>
    )
  }

  const { stats, active_strategies, recent_activities } = dashboardData

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Page Header */}
        <div>
          <h1 className="text-3xl font-bold tracking-tight">대시보드</h1>
          <p className="text-muted-foreground">
            트레이딩 시스템 현황을 한눈에 확인하세요
          </p>
        </div>

        {/* Summary Cards */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">총 자산</CardTitle>
              <Wallet className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {formatCurrency(stats.total_balance)}
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                전체 보유 자산
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">수익/손실</CardTitle>
              {stats.profit_loss >= 0 ? (
                <TrendingUp className="h-4 w-4 text-green-600" />
              ) : (
                <TrendingDown className="h-4 w-4 text-red-600" />
              )}
            </CardHeader>
            <CardContent>
              <div
                className={`text-2xl font-bold ${
                  stats.profit_loss >= 0 ? 'text-green-600' : 'text-red-600'
                }`}
              >
                {formatCurrency(stats.profit_loss)}
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                <span
                  className={
                    stats.profit_loss_percent >= 0
                      ? 'text-green-600'
                      : 'text-red-600'
                  }
                >
                  {stats.profit_loss_percent >= 0 ? '+' : ''}
                  {stats.profit_loss_percent}%
                </span>{' '}
                총 수익률
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">활성 전략</CardTitle>
              <Activity className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.active_strategies}</div>
              <p className="text-xs text-muted-foreground mt-1">
                현재 운영 중인 전략
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">오늘의 거래</CardTitle>
              <BarChart3 className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.today_trades}</div>
              <p className="text-xs text-muted-foreground mt-1">
                금일 체결된 거래
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <CardTitle>빠른 실행</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-4">
              <Button className="flex items-center gap-2">
                <Plus className="h-4 w-4" />
                새 전략 생성
              </Button>
              <Button variant="outline" className="flex items-center gap-2">
                <PlayCircle className="h-4 w-4" />
                백테스트 실행
              </Button>
              <Button variant="outline" className="flex items-center gap-2">
                <BarChart3 className="h-4 w-4" />
                성과 분석
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Two Column Layout */}
        <div className="grid gap-6 md:grid-cols-2">
          {/* Active Strategies */}
          <Card>
            <CardHeader>
              <CardTitle>활성 전략</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {active_strategies.map((strategy) => (
                  <div
                    key={strategy.id}
                    className="flex items-center justify-between border-b pb-3 last:border-0 last:pb-0"
                  >
                    <div className="space-y-1">
                      <p className="font-medium">{strategy.name}</p>
                      <div className="flex items-center gap-2">
                        <span className="inline-flex items-center rounded-full bg-green-100 px-2 py-0.5 text-xs font-medium text-green-700">
                          운영중
                        </span>
                      </div>
                    </div>
                    <div className="text-right">
                      <p
                        className={`font-semibold ${
                          strategy.profit_loss >= 0
                            ? 'text-green-600'
                            : 'text-red-600'
                        }`}
                      >
                        {formatCurrency(strategy.profit_loss)}
                      </p>
                      <p
                        className={`text-xs ${
                          strategy.profit_loss_percent >= 0
                            ? 'text-green-600'
                            : 'text-red-600'
                        }`}
                      >
                        {strategy.profit_loss_percent >= 0 ? '+' : ''}
                        {strategy.profit_loss_percent}%
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Recent Activity */}
          <Card>
            <CardHeader>
              <CardTitle>최근 거래 내역</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recent_activities.map((activity) => (
                  <div
                    key={activity.id}
                    className="flex items-center justify-between border-b pb-3 last:border-0 last:pb-0"
                  >
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span
                          className={`inline-flex items-center rounded px-2 py-0.5 text-xs font-semibold ${
                            activity.type === 'BUY'
                              ? 'bg-blue-100 text-blue-700'
                              : 'bg-red-100 text-red-700'
                          }`}
                        >
                          {activity.type === 'BUY' ? '매수' : '매도'}
                        </span>
                        <p className="font-medium">{activity.symbol}</p>
                      </div>
                      <p className="text-xs text-muted-foreground">
                        {activity.quantity}주 @ {formatCurrency(activity.price)}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-xs text-muted-foreground">
                        {activity.time}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  )
}

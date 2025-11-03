'use client'

import { useState } from 'react'
import { DashboardLayout } from '@/components/layout/DashboardLayout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  History,
  Filter,
  Download,
  Search,
} from 'lucide-react'

type TradeStatus = 'completed' | 'pending' | 'cancelled' | 'failed'
type TradeSide = 'BUY' | 'SELL'

interface Trade {
  id: number
  strategy_name: string
  symbol: string
  side: TradeSide
  quantity: number
  order_price: number
  executed_price?: number
  status: TradeStatus
  order_time: string
  executed_time?: string
  profit_loss?: number
  profit_loss_percent?: number
  commission: number
  slippage?: number
}

const TRADE_STATUS_LABELS: Record<TradeStatus, string> = {
  completed: '체결완료',
  pending: '주문중',
  cancelled: '취소됨',
  failed: '실패',
}

const TRADE_STATUS_COLORS: Record<TradeStatus, string> = {
  completed: 'bg-green-100 text-green-700',
  pending: 'bg-blue-100 text-blue-700',
  cancelled: 'bg-gray-100 text-gray-700',
  failed: 'bg-red-100 text-red-700',
}

export default function TradesPage() {
  const [dateFrom, setDateFrom] = useState('2024-01-01')
  const [dateTo, setDateTo] = useState('2024-01-21')
  const [symbolFilter, setSymbolFilter] = useState('')
  const [statusFilter, setStatusFilter] = useState<string>('all')

  // TODO: Fetch trades from API
  const trades: Trade[] = [
    {
      id: 1,
      strategy_name: '모멘텀 전략 A',
      symbol: '삼성전자',
      side: 'BUY',
      quantity: 10,
      order_price: 71000,
      executed_price: 71000,
      status: 'completed',
      order_time: '2024-01-20T10:23:00Z',
      executed_time: '2024-01-20T10:23:15Z',
      commission: 106.5,
      slippage: 0,
    },
    {
      id: 2,
      strategy_name: '모멘텀 전략 A',
      symbol: 'SK하이닉스',
      side: 'SELL',
      quantity: 5,
      order_price: 132000,
      executed_price: 131900,
      status: 'completed',
      order_time: '2024-01-20T09:45:00Z',
      executed_time: '2024-01-20T09:45:32Z',
      profit_loss: 25000,
      profit_loss_percent: 3.94,
      commission: 98.925,
      slippage: -100,
    },
    {
      id: 3,
      strategy_name: '평균회귀 전략 B',
      symbol: 'NAVER',
      side: 'BUY',
      quantity: 8,
      order_price: 205000,
      executed_price: 205200,
      status: 'completed',
      order_time: '2024-01-19T14:12:00Z',
      executed_time: '2024-01-19T14:12:08Z',
      commission: 246.24,
      slippage: 200,
    },
    {
      id: 4,
      strategy_name: '변동성 돌파 전략 C',
      symbol: 'LG화학',
      side: 'SELL',
      quantity: 3,
      order_price: 420000,
      executed_price: 419500,
      status: 'completed',
      order_time: '2024-01-19T11:30:00Z',
      executed_time: '2024-01-19T11:30:45Z',
      profit_loss: -15000,
      profit_loss_percent: -1.19,
      commission: 188.325,
      slippage: -500,
    },
    {
      id: 5,
      strategy_name: '모멘텀 전략 A',
      symbol: 'KB금융',
      side: 'BUY',
      quantity: 20,
      order_price: 58000,
      status: 'pending',
      order_time: '2024-01-21T15:45:00Z',
      commission: 0,
    },
    {
      id: 6,
      strategy_name: '평균회귀 전략 B',
      symbol: '현대차',
      side: 'BUY',
      quantity: 15,
      order_price: 215000,
      status: 'cancelled',
      order_time: '2024-01-18T10:20:00Z',
      commission: 0,
    },
    {
      id: 7,
      strategy_name: '변동성 돌파 전략 C',
      symbol: '삼성바이오',
      side: 'SELL',
      quantity: 2,
      order_price: 850000,
      status: 'failed',
      order_time: '2024-01-17T16:30:00Z',
      commission: 0,
    },
  ]

  const filteredTrades = trades.filter((trade) => {
    const matchesStatus = statusFilter === 'all' || trade.status === statusFilter
    const matchesSymbol =
      !symbolFilter || trade.symbol.toLowerCase().includes(symbolFilter.toLowerCase())
    return matchesStatus && matchesSymbol
  })

  const totalStats = {
    total_trades: trades.filter((t) => t.status === 'completed').length,
    total_profit_loss: trades
      .filter((t) => t.status === 'completed' && t.profit_loss)
      .reduce((sum, t) => sum + (t.profit_loss ?? 0), 0),
    total_commission: trades
      .filter((t) => t.status === 'completed')
      .reduce((sum, t) => sum + t.commission, 0),
    win_rate:
      (trades.filter((t) => t.status === 'completed' && (t.profit_loss ?? 0) > 0)
        .length /
        trades.filter((t) => t.status === 'completed' && t.profit_loss !== undefined)
          .length) *
      100,
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
      second: '2-digit',
    })
  }

  const handleExport = () => {
    // TODO: Export to CSV
    console.log('Exporting trades to CSV...')
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Page Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">거래 내역</h1>
            <p className="text-muted-foreground">
              모든 매매 거래 내역을 확인하세요
            </p>
          </div>
          <Button
            variant="outline"
            onClick={handleExport}
            className="flex items-center gap-2"
          >
            <Download className="h-4 w-4" />
            내보내기
          </Button>
        </div>

        {/* Statistics */}
        <div className="grid gap-4 md:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">총 거래</CardTitle>
              <History className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{totalStats.total_trades}</div>
              <p className="text-xs text-muted-foreground mt-1">체결 완료</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">총 손익</CardTitle>
            </CardHeader>
            <CardContent>
              <div
                className={`text-2xl font-bold ${
                  totalStats.total_profit_loss >= 0
                    ? 'text-green-600'
                    : 'text-red-600'
                }`}
              >
                {totalStats.total_profit_loss >= 0 ? '+' : ''}
                {formatCurrency(totalStats.total_profit_loss)}
              </div>
              <p className="text-xs text-muted-foreground mt-1">실현 손익</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">승률</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {totalStats.win_rate.toFixed(1)}%
              </div>
              <p className="text-xs text-muted-foreground mt-1">수익 거래 비율</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">총 수수료</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-red-600">
                {formatCurrency(totalStats.total_commission)}
              </div>
              <p className="text-xs text-muted-foreground mt-1">거래 비용</p>
            </CardContent>
          </Card>
        </div>

        {/* Filters */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Filter className="h-5 w-5" />
              필터
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-4">
              <div className="space-y-2">
                <Label htmlFor="date_from">시작일</Label>
                <Input
                  id="date_from"
                  type="date"
                  value={dateFrom}
                  onChange={(e) => setDateFrom(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="date_to">종료일</Label>
                <Input
                  id="date_to"
                  type="date"
                  value={dateTo}
                  onChange={(e) => setDateTo(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="symbol">종목명</Label>
                <div className="relative">
                  <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="symbol"
                    placeholder="종목 검색..."
                    value={symbolFilter}
                    onChange={(e) => setSymbolFilter(e.target.value)}
                    className="pl-8"
                  />
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="status">상태</Label>
                <select
                  id="status"
                  className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                >
                  <option value="all">전체</option>
                  <option value="completed">체결완료</option>
                  <option value="pending">주문중</option>
                  <option value="cancelled">취소됨</option>
                  <option value="failed">실패</option>
                </select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Trades Table */}
        <Card>
          <CardHeader>
            <CardTitle>거래 목록 ({filteredTrades.length}건)</CardTitle>
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
                      전략
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
                      주문가
                    </th>
                    <th className="text-right py-3 px-2 text-sm font-medium text-muted-foreground">
                      체결가
                    </th>
                    <th className="text-center py-3 px-2 text-sm font-medium text-muted-foreground">
                      상태
                    </th>
                    <th className="text-right py-3 px-2 text-sm font-medium text-muted-foreground">
                      손익
                    </th>
                    <th className="text-right py-3 px-2 text-sm font-medium text-muted-foreground">
                      수수료
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {filteredTrades.map((trade) => (
                    <tr key={trade.id} className="border-b last:border-0 hover:bg-muted/50">
                      <td className="py-3 px-2 text-sm">
                        {formatDate(trade.order_time)}
                      </td>
                      <td className="py-3 px-2 text-sm">
                        {trade.strategy_name}
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
                        {formatCurrency(trade.order_price)}
                      </td>
                      <td className="py-3 px-2 text-sm text-right">
                        {trade.executed_price
                          ? formatCurrency(trade.executed_price)
                          : '-'}
                      </td>
                      <td className="py-3 px-2 text-center">
                        <span
                          className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                            TRADE_STATUS_COLORS[trade.status]
                          }`}
                        >
                          {TRADE_STATUS_LABELS[trade.status]}
                        </span>
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
                        {trade.profit_loss ? (
                          <div>
                            <div>
                              {trade.profit_loss >= 0 ? '+' : ''}
                              {formatCurrency(trade.profit_loss)}
                            </div>
                            <div className="text-xs">
                              {trade.profit_loss_percent! >= 0 ? '+' : ''}
                              {trade.profit_loss_percent?.toFixed(2)}%
                            </div>
                          </div>
                        ) : (
                          '-'
                        )}
                      </td>
                      <td className="py-3 px-2 text-sm text-right text-red-600">
                        {trade.commission > 0
                          ? formatCurrency(trade.commission)
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

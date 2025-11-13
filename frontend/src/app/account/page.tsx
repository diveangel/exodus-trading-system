'use client'

import { useState, useEffect } from 'react'
import { DashboardLayout } from '@/components/layout/DashboardLayout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import {
  Wallet,
  TrendingUp,
  TrendingDown,
  PieChart,
  RefreshCw,
  Eye,
  EyeOff,
  Settings,
  Loader2,
  AlertCircle,
} from 'lucide-react'
import { accountApi, AccountBalance } from '@/lib/accountApi'
import { useRouter } from 'next/navigation'

export default function AccountPage() {
  const router = useRouter()
  const [showBalance, setShowBalance] = useState(true)
  const [isRefreshing, setIsRefreshing] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [balanceData, setBalanceData] = useState<AccountBalance | null>(null)

  const fetchBalance = async () => {
    try {
      setError(null)
      const data = await accountApi.getBalance()
      setBalanceData(data)
    } catch (err: any) {
      console.error('Failed to fetch balance:', err)
      if (err.response?.status === 400) {
        setError('KIS API 인증 정보가 설정되지 않았습니다. 설정 페이지에서 먼저 설정해주세요.')
      } else {
        setError(err.response?.data?.detail || '계좌 정보를 불러오는데 실패했습니다.')
      }
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchBalance()
  }, [])

  const handleRefresh = async () => {
    setIsRefreshing(true)
    await fetchBalance()
    setIsRefreshing(false)
  }

  // Parse balance data
  // KIS API: output2[0] = 계좌 요약 정보, output1 = 보유 종목 리스트
  const accountSummary = balanceData && balanceData.output2 && balanceData.output2.length > 0 ? {
    total_balance: parseFloat(balanceData.output2[0].tot_evlu_amt || '0'),
    cash_balance: parseFloat(balanceData.output2[0].dnca_tot_amt || '0'),
    available_balance: parseFloat(balanceData.output2[0].prvs_rcdl_excc_amt || '0'),
    stock_value: parseFloat(balanceData.output2[0].evlu_amt_smtl_amt || '0'),
    total_profit_loss: parseFloat(balanceData.output2[0].evlu_pfls_smtl_amt || '0'),
    purchase_total: parseFloat(balanceData.output2[0].pchs_amt_smtl_amt || '0'),
  } : null

  // Parse holdings data
  const holdings = balanceData && balanceData.output1 ? balanceData.output1.map((holding, index) => ({
    id: index + 1,
    symbol: holding.prdt_name,
    code: holding.pdno,
    quantity: parseInt(holding.hldg_qty || '0'),
    avg_price: parseFloat(holding.pchs_avg_pric || '0'),
    current_price: parseFloat(holding.prpr || '0'),
    market_value: parseFloat(holding.evlu_amt || '0'),
    profit_loss: parseFloat(holding.evlu_pfls_amt || '0'),
    profit_loss_percent: parseFloat(holding.evlu_pfls_rt || '0'),
    weight: accountSummary ? (parseFloat(holding.evlu_amt || '0') / accountSummary.stock_value * 100) : 0,
  })) : []

  const formatCurrency = (amount: number) => {
    if (!showBalance) return '••••••••'
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
            <h1 className="text-3xl font-bold tracking-tight">계좌 정보</h1>
            <p className="text-muted-foreground">
              계좌 잔고 및 보유 종목을 확인하세요
            </p>
          </div>
          <Card>
            <CardContent className="pt-6">
              <div className="flex flex-col items-center justify-center py-12">
                <AlertCircle className="h-12 w-12 text-red-500 mb-4" />
                <p className="text-lg font-semibold mb-2">계좌 정보를 불러올 수 없습니다</p>
                <p className="text-sm text-muted-foreground mb-4">{error}</p>
                <div className="flex gap-2">
                  <Button onClick={() => router.push('/settings')}>
                    설정으로 이동
                  </Button>
                  <Button variant="outline" onClick={() => {
                    setError(null)
                    setIsLoading(true)
                    fetchBalance()
                  }}>
                    다시 시도
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </DashboardLayout>
    )
  }

  if (!accountSummary) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-96">
          <p className="text-muted-foreground">데이터를 불러오는 중...</p>
        </div>
      </DashboardLayout>
    )
  }

  const profit_loss_percent = accountSummary.purchase_total > 0
    ? (accountSummary.total_profit_loss / accountSummary.purchase_total * 100)
    : 0

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Page Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">계좌 정보</h1>
            <p className="text-muted-foreground">
              계좌 잔고 및 보유 종목을 확인하세요
            </p>
          </div>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="icon"
              onClick={() => setShowBalance(!showBalance)}
            >
              {showBalance ? (
                <Eye className="h-4 w-4" />
              ) : (
                <EyeOff className="h-4 w-4" />
              )}
            </Button>
            <Button
              variant="outline"
              onClick={handleRefresh}
              disabled={isRefreshing}
              className="flex items-center gap-2"
            >
              <RefreshCw
                className={`h-4 w-4 ${isRefreshing ? 'animate-spin' : ''}`}
              />
              새로고침
            </Button>
          </div>
        </div>

        {/* Account Summary */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">총 자산</CardTitle>
              <Wallet className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {formatCurrency(accountSummary.total_balance)}
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                현금 + 주식 평가액
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">총 손익</CardTitle>
              {accountSummary.total_profit_loss >= 0 ? (
                <TrendingUp className="h-4 w-4 text-green-600" />
              ) : (
                <TrendingDown className="h-4 w-4 text-red-600" />
              )}
            </CardHeader>
            <CardContent>
              <div
                className={`text-2xl font-bold ${
                  accountSummary.total_profit_loss >= 0
                    ? 'text-green-600'
                    : 'text-red-600'
                }`}
              >
                {formatCurrency(accountSummary.total_profit_loss)}
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                <span
                  className={
                    profit_loss_percent >= 0
                      ? 'text-green-600'
                      : 'text-red-600'
                  }
                >
                  {profit_loss_percent >= 0 ? '+' : ''}
                  {profit_loss_percent.toFixed(2)}%
                </span>{' '}
                수익률
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">가용 금액</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {formatCurrency(accountSummary.available_balance)}
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                출금 및 매수 가능 금액
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">주식 평가액</CardTitle>
              <PieChart className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {formatCurrency(accountSummary.stock_value)}
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                {((accountSummary.stock_value / accountSummary.total_balance) * 100).toFixed(1)}% 비중
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Holdings */}
        <Card>
          <CardHeader>
            <CardTitle>보유 종목</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-3 px-2 text-sm font-medium text-muted-foreground">
                      종목명
                    </th>
                    <th className="text-right py-3 px-2 text-sm font-medium text-muted-foreground">
                      보유수량
                    </th>
                    <th className="text-right py-3 px-2 text-sm font-medium text-muted-foreground">
                      평균단가
                    </th>
                    <th className="text-right py-3 px-2 text-sm font-medium text-muted-foreground">
                      현재가
                    </th>
                    <th className="text-right py-3 px-2 text-sm font-medium text-muted-foreground">
                      평가금액
                    </th>
                    <th className="text-right py-3 px-2 text-sm font-medium text-muted-foreground">
                      손익
                    </th>
                    <th className="text-right py-3 px-2 text-sm font-medium text-muted-foreground">
                      수익률
                    </th>
                    <th className="text-right py-3 px-2 text-sm font-medium text-muted-foreground">
                      비중
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {holdings.map((holding) => (
                    <tr key={holding.id} className="border-b last:border-0 hover:bg-muted/50">
                      <td className="py-3 px-2">
                        <div>
                          <p className="text-sm font-medium">{holding.symbol}</p>
                          <p className="text-xs text-muted-foreground">
                            {holding.code}
                          </p>
                        </div>
                      </td>
                      <td className="py-3 px-2 text-sm text-right">
                        {holding.quantity}주
                      </td>
                      <td className="py-3 px-2 text-sm text-right">
                        {formatCurrency(holding.avg_price)}
                      </td>
                      <td className="py-3 px-2 text-sm text-right">
                        {formatCurrency(holding.current_price)}
                      </td>
                      <td className="py-3 px-2 text-sm text-right font-medium">
                        {formatCurrency(holding.market_value)}
                      </td>
                      <td
                        className={`py-3 px-2 text-sm text-right font-semibold ${
                          holding.profit_loss >= 0
                            ? 'text-green-600'
                            : 'text-red-600'
                        }`}
                      >
                        {holding.profit_loss >= 0 ? '+' : ''}
                        {formatCurrency(holding.profit_loss)}
                      </td>
                      <td
                        className={`py-3 px-2 text-sm text-right font-semibold ${
                          holding.profit_loss_percent >= 0
                            ? 'text-green-600'
                            : 'text-red-600'
                        }`}
                      >
                        {holding.profit_loss_percent >= 0 ? '+' : ''}
                        {holding.profit_loss_percent.toFixed(2)}%
                      </td>
                      <td className="py-3 px-2 text-sm text-right">
                        {holding.weight.toFixed(2)}%
                      </td>
                    </tr>
                  ))}
                </tbody>
                <tfoot className="border-t bg-muted/50">
                  <tr>
                    <td className="py-3 px-2 text-sm font-semibold" colSpan={4}>
                      합계
                    </td>
                    <td className="py-3 px-2 text-sm text-right font-semibold">
                      {formatCurrency(accountSummary.stock_value)}
                    </td>
                    <td
                      className={`py-3 px-2 text-sm text-right font-semibold ${
                        holdings.reduce((sum, h) => sum + h.profit_loss, 0) >= 0
                          ? 'text-green-600'
                          : 'text-red-600'
                      }`}
                    >
                      {holdings.reduce((sum, h) => sum + h.profit_loss, 0) >= 0
                        ? '+'
                        : ''}
                      {formatCurrency(
                        holdings.reduce((sum, h) => sum + h.profit_loss, 0)
                      )}
                    </td>
                    <td className="py-3 px-2 text-sm text-right" colSpan={2}></td>
                  </tr>
                </tfoot>
              </table>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  )
}

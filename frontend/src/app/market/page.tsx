'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { MarketChart } from '@/components/market/MarketChart';
import { MarketDataTable } from '@/components/market/MarketDataTable';
import { useMarketData } from '@/hooks/useMarketData';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { StockSearchDialog } from '@/components/stocks/StockSearchDialog';
import { Loader2, TrendingUp, Download, Search } from 'lucide-react';
import type { Stock } from '@/types/stock';

type TimeInterval = '1m' | '5m' | '10m' | '30m' | '1h' | '1d';

export default function MarketPage() {
  const [symbol, setSymbol] = useState(''); // 초기값 비어있음
  const [selectedStock, setSelectedStock] = useState<Stock | null>(null);
  const [isStockSearchOpen, setIsStockSearchOpen] = useState(false);
  const [interval, setInterval] = useState<TimeInterval>('1d');
  const [days, setDays] = useState(30);

  const {
    chartData,
    currentPrice,
    isLoadingChart,
    isLoadingPrice,
    isCollecting,
    collectDailyData,
    collectMinuteData,
    refreshChartData,
    refreshCurrentPrice,
    error
  } = useMarketData(symbol, interval, days);

  const handleCollectData = async () => {
    if (interval === '1d') {
      await collectDailyData();
    } else {
      await collectMinuteData();
    }
    // Refresh chart data after collecting
    await refreshChartData();
  };

  const handleSearch = () => {
    refreshChartData();
    refreshCurrentPrice();
  };

  const handleStockSelect = (stock: Stock) => {
    setSymbol(stock.symbol);
    setSelectedStock(stock);
    // Auto-refresh data with new symbol
    setTimeout(() => {
      refreshChartData();
      refreshCurrentPrice();
    }, 100);
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Market Data</h1>
            <p className="text-muted-foreground">
              시장 데이터 수집 및 조회
            </p>
          </div>
        </div>

      {/* Search and Controls */}
      <Card>
        <CardHeader>
          <CardTitle>종목 조회</CardTitle>
          <CardDescription>
            종목 코드와 시간 간격을 선택하여 시장 데이터를 조회하세요
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {/* Symbol Input */}
            <div className="space-y-2">
              <Label htmlFor="symbol">종목 코드</Label>
              <div className="flex gap-2">
                <Input
                  id="symbol"
                  type="text"
                  placeholder="005930"
                  value={symbol}
                  onChange={(e) => setSymbol(e.target.value)}
                  className="flex-1"
                />
                <Button
                  variant="outline"
                  size="icon"
                  onClick={() => setIsStockSearchOpen(true)}
                  title="종목 검색"
                >
                  <Search className="h-4 w-4" />
                </Button>
              </div>
              {selectedStock && (
                <p className="text-xs text-muted-foreground">
                  {selectedStock.name} ({selectedStock.market_type})
                </p>
              )}
              {!selectedStock && !symbol && (
                <p className="text-xs text-muted-foreground">
                  검색 버튼을 클릭하거나 종목코드를 입력하세요
                </p>
              )}
              {!selectedStock && symbol && (
                <p className="text-xs text-muted-foreground">
                  예: 005930 (삼성전자)
                </p>
              )}
            </div>

            {/* Interval Select */}
            <div className="space-y-2">
              <Label htmlFor="interval">시간 간격</Label>
              <Select value={interval} onValueChange={(value) => setInterval(value as TimeInterval)}>
                <SelectTrigger id="interval">
                  <SelectValue placeholder="시간 간격 선택" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="1m">1분봉</SelectItem>
                  <SelectItem value="5m">5분봉</SelectItem>
                  <SelectItem value="10m">10분봉</SelectItem>
                  <SelectItem value="30m">30분봉</SelectItem>
                  <SelectItem value="1h">1시간봉</SelectItem>
                  <SelectItem value="1d">일봉</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Days Input */}
            <div className="space-y-2">
              <Label htmlFor="days">조회 기간 (일)</Label>
              <Input
                id="days"
                type="number"
                min="1"
                max="365"
                value={days}
                onChange={(e) => setDays(parseInt(e.target.value) || 30)}
              />
            </div>

            {/* Actions */}
            <div className="space-y-2">
              <Label>&nbsp;</Label>
              <div className="flex gap-2">
                <Button onClick={handleSearch} className="flex-1">
                  {isLoadingChart ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    '조회'
                  )}
                </Button>
                <Button
                  onClick={handleCollectData}
                  variant="outline"
                  disabled={isCollecting}
                  className="flex-1"
                >
                  {isCollecting ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      수집중
                    </>
                  ) : (
                    <>
                      <Download className="mr-2 h-4 w-4" />
                      수집
                    </>
                  )}
                </Button>
              </div>
            </div>
          </div>

          {error && (
            <div className="p-4 text-sm text-red-800 bg-red-50 rounded-md">
              {error}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Current Price Card */}
      {currentPrice && (
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                현재가 정보
              </CardTitle>
              <p className="text-sm text-muted-foreground">
                체결시각: {new Date(currentPrice.timestamp).toLocaleString('ko-KR', {
                  year: 'numeric',
                  month: '2-digit',
                  day: '2-digit',
                  hour: '2-digit',
                  minute: '2-digit',
                  second: '2-digit'
                })}
              </p>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <p className="text-sm text-muted-foreground">현재가</p>
                <p className="text-2xl font-bold">{(currentPrice.price || 0).toLocaleString()}원</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">전일대비</p>
                <p className={`text-2xl font-bold ${(currentPrice.change || 0) >= 0 ? 'text-red-600' : 'text-blue-600'}`}>
                  {(currentPrice.change || 0) >= 0 ? '+' : ''}{(currentPrice.change || 0).toLocaleString()}원
                </p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">등락률</p>
                <p className={`text-2xl font-bold ${(currentPrice.changePercent || 0) >= 0 ? 'text-red-600' : 'text-blue-600'}`}>
                  {(currentPrice.changePercent || 0) >= 0 ? '+' : ''}{(currentPrice.changePercent || 0).toFixed(2)}%
                </p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">거래량</p>
                <p className="text-2xl font-bold">{(currentPrice.volume || 0).toLocaleString()}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Chart */}
      <Card>
        <CardHeader>
          <CardTitle>가격 차트</CardTitle>
          <CardDescription>
            {symbol ? `${symbol} - ${interval} 차트 (${chartData?.data.length || 0}개 데이터)` : '종목을 선택하세요'}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {isLoadingChart ? (
            <div className="flex items-center justify-center h-96">
              <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
            </div>
          ) : !symbol ? (
            <div className="flex flex-col items-center justify-center h-96 text-muted-foreground">
              <Search className="h-16 w-16 mb-4 opacity-20" />
              <p className="text-lg font-medium">종목을 선택해주세요</p>
              <p className="text-sm mt-2">검색 버튼을 클릭하거나 종목코드를 직접 입력하세요</p>
            </div>
          ) : chartData && chartData.data.length > 0 ? (
            <MarketChart data={chartData.data} interval={interval} />
          ) : (
            <div className="flex flex-col items-center justify-center h-96 text-muted-foreground">
              <p>데이터가 없습니다</p>
              <p className="text-sm">&quot;수집&quot; 버튼을 눌러 데이터를 수집하세요</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Data Table */}
      {chartData && chartData.data.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>시세 데이터</CardTitle>
            <CardDescription>
              OHLCV 데이터 테이블
            </CardDescription>
          </CardHeader>
          <CardContent>
            <MarketDataTable data={chartData.data} />
          </CardContent>
        </Card>
      )}

      {/* Stock Search Dialog */}
      <StockSearchDialog
        open={isStockSearchOpen}
        onOpenChange={setIsStockSearchOpen}
        onSelect={handleStockSelect}
      />
      </div>
    </DashboardLayout>
  );
}

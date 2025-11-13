'use client'

import { useState, useEffect } from 'react'
import { X, Plus } from 'lucide-react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Stock } from '@/types/stock'
import { stockApi } from '@/lib/stockApi'
import { watchlistApi } from '@/lib/watchlistApi'
import { StockSearchInput } from './StockSearchInput'

interface MultiStockSelectorProps {
  selectedStocks: Stock[]
  onStocksChange: (stocks: Stock[]) => void
}

export function MultiStockSelector({ selectedStocks, onStocksChange }: MultiStockSelectorProps) {
  const [searchStock, setSearchStock] = useState<Stock | null>(null)
  const [watchlistStocks, setWatchlistStocks] = useState<Stock[]>([])
  const [isLoadingWatchlist, setIsLoadingWatchlist] = useState(false)

  // Load watchlist stocks
  useEffect(() => {
    loadWatchlist()
  }, [])

  const loadWatchlist = async () => {
    setIsLoadingWatchlist(true)
    try {
      // Get watchlist symbols
      const symbols = await watchlistApi.getWatchlistSymbols()

      // Load stock details for each symbol
      const stockPromises = symbols.map(symbol => stockApi.getStock(symbol))
      const stocks = await Promise.all(stockPromises)

      setWatchlistStocks(stocks)
    } catch (error) {
      console.error('Failed to load watchlist:', error)
      setWatchlistStocks([])
    } finally {
      setIsLoadingWatchlist(false)
    }
  }

  const addStock = (stock: Stock) => {
    if (!selectedStocks.find(s => s.symbol === stock.symbol)) {
      onStocksChange([...selectedStocks, stock])
    }
    setSearchStock(null)
  }

  const removeStock = (symbol: string) => {
    onStocksChange(selectedStocks.filter(s => s.symbol !== symbol))
  }

  const addFromWatchlist = (stock: Stock) => {
    addStock(stock)
  }

  return (
    <div className="space-y-4">
      {/* Selected Stocks Display */}
      {selectedStocks.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">선택된 종목 ({selectedStocks.length}개)</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2">
              {selectedStocks.map((stock) => (
                <Badge key={stock.symbol} variant="secondary" className="px-3 py-1.5">
                  <span className="mr-2">{stock.name} ({stock.symbol})</span>
                  <button
                    onClick={() => removeStock(stock.symbol)}
                    className="ml-1 hover:bg-muted-foreground/20 rounded-sm"
                  >
                    <X className="h-3 w-3" />
                  </button>
                </Badge>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Stock Selection Tabs */}
      <Tabs defaultValue="manual" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="manual">수동 선택</TabsTrigger>
          <TabsTrigger value="watchlist">즐겨찾기</TabsTrigger>
        </TabsList>

        {/* Manual Selection Tab */}
        <TabsContent value="manual" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">종목 검색</CardTitle>
              <CardDescription>종목명 또는 종목코드로 검색하세요</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <StockSearchInput
                selectedStock={searchStock}
                onSelect={(stock) => {
                  if (stock) {
                    addStock(stock)
                  } else {
                    setSearchStock(null)
                  }
                }}
                placeholder="종목명 또는 종목코드 입력"
              />
            </CardContent>
          </Card>
        </TabsContent>

        {/* Watchlist Tab */}
        <TabsContent value="watchlist" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">즐겨찾기 종목</CardTitle>
              <CardDescription>즐겨찾기에 등록된 종목을 선택하세요</CardDescription>
            </CardHeader>
            <CardContent>
              {isLoadingWatchlist ? (
                <p className="text-sm text-muted-foreground">로딩 중...</p>
              ) : watchlistStocks.length === 0 ? (
                <p className="text-sm text-muted-foreground">
                  즐겨찾기에 등록된 종목이 없습니다.
                </p>
              ) : (
                <div className="space-y-2">
                  {watchlistStocks.map((stock) => {
                    const isSelected = selectedStocks.find(s => s.symbol === stock.symbol)
                    return (
                      <div
                        key={stock.symbol}
                        className="flex items-center justify-between p-3 border rounded-md hover:bg-muted"
                      >
                        <div>
                          <p className="font-medium">{stock.name}</p>
                          <p className="text-sm text-muted-foreground">
                            {stock.symbol} · {stock.market_type}
                          </p>
                        </div>
                        <Button
                          size="sm"
                          variant={isSelected ? "secondary" : "outline"}
                          onClick={() => addFromWatchlist(stock)}
                          disabled={!!isSelected}
                        >
                          {isSelected ? '선택됨' : '추가'}
                        </Button>
                      </div>
                    )
                  })}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

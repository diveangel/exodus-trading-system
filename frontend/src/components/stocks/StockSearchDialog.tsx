'use client';

import { useState, useEffect } from 'react';
import { Search, Loader2 } from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { apiClient } from '@/lib/api';
import type { Stock, MarketType, StockListResponse } from '@/types/stock';

interface StockSearchDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSelect: (stock: Stock) => void;
}

export function StockSearchDialog({ open, onOpenChange, onSelect }: StockSearchDialogProps) {
  const [query, setQuery] = useState('');
  const [marketType, setMarketType] = useState<MarketType>('ALL');
  const [results, setResults] = useState<Stock[]>([]);
  const [total, setTotal] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Search on query change with debounce
  useEffect(() => {
    if (!query || query.length < 1) {
      setResults([]);
      setTotal(0);
      return;
    }

    const timeoutId = setTimeout(() => {
      searchStocks();
    }, 300);

    return () => clearTimeout(timeoutId);
  }, [query, marketType]);

  const searchStocks = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await apiClient.get<StockListResponse>('/stocks/search', {
        params: {
          query,
          market_type: marketType,
          limit: 20,
        },
      });

      setResults(response.data.stocks);
      setTotal(response.data.total);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || '종목 검색에 실패했습니다';
      setError(errorMessage);
      setResults([]);
      setTotal(0);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelect = (stock: Stock) => {
    onSelect(stock);
    onOpenChange(false);
    setQuery('');
    setResults([]);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[80vh] flex flex-col">
        <DialogHeader>
          <DialogTitle>종목 검색</DialogTitle>
          <DialogDescription>
            종목명 또는 종목코드를 입력하여 검색하세요
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4">
          {/* Search Input */}
          <div className="flex gap-2">
            <div className="flex-1">
              <Label htmlFor="stock-search" className="sr-only">
                종목 검색
              </Label>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  id="stock-search"
                  type="text"
                  placeholder="종목명 또는 코드 입력 (예: 삼성전자, 005930)"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  className="pl-9"
                  autoFocus
                />
              </div>
            </div>

            <Select value={marketType} onValueChange={(value) => setMarketType(value as MarketType)}>
              <SelectTrigger className="w-32">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="ALL">전체</SelectItem>
                <SelectItem value="KOSPI">KOSPI</SelectItem>
                <SelectItem value="KOSDAQ">KOSDAQ</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Error Message */}
          {error && (
            <div className="p-3 text-sm text-red-800 bg-red-50 rounded-md">
              {error}
            </div>
          )}

          {/* Loading State */}
          {isLoading && (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
            </div>
          )}

          {/* Search Results */}
          {!isLoading && query && results.length > 0 && (
            <div className="space-y-2">
              <div className="text-sm text-muted-foreground">
                {total}개의 종목 중 {results.length}개 표시
              </div>
              <div className="border rounded-md overflow-hidden max-h-96 overflow-y-auto">
                {results.map((stock) => (
                  <button
                    key={stock.id}
                    onClick={() => handleSelect(stock)}
                    className="w-full px-4 py-3 text-left hover:bg-muted/50 transition-colors border-b last:border-b-0 focus:outline-none focus:bg-muted"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="font-medium">{stock.name}</div>
                        <div className="text-sm text-muted-foreground">
                          {stock.symbol}
                        </div>
                      </div>
                      <div className="text-xs font-medium px-2 py-1 rounded bg-muted">
                        {stock.market_type}
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* No Results */}
          {!isLoading && query && results.length === 0 && (
            <div className="text-center py-8 text-muted-foreground">
              <p>검색 결과가 없습니다</p>
              <p className="text-sm mt-1">다른 검색어를 입력해보세요</p>
            </div>
          )}

          {/* Empty State */}
          {!query && (
            <div className="text-center py-8 text-muted-foreground">
              <Search className="h-12 w-12 mx-auto mb-2 opacity-20" />
              <p>종목명 또는 코드를 입력하세요</p>
              <p className="text-sm mt-1">예: 삼성전자, 005930</p>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}

'use client';

import { useState, useEffect } from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
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
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { stockApi, StockListParams, StockFiltersResponse } from '@/lib/stockApi';
import { watchlistApi } from '@/lib/watchlistApi';
import { Stock } from '@/types/stock';
import { Loader2, Filter, TrendingUp, ChevronLeft, ChevronRight, Search } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { WatchlistButton } from '@/components/ui/watchlist-button';

export default function StocksPage() {
  const router = useRouter();
  const [stocks, setStocks] = useState<Stock[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState<StockFiltersResponse | null>(null);
  const [watchlistSymbols, setWatchlistSymbols] = useState<Set<string>>(new Set());

  // Filter states
  const [marketType, setMarketType] = useState<'KOSPI' | 'KOSDAQ' | 'ALL'>('ALL');
  const [sector, setSector] = useState<string>('ALL');
  const [industry, setIndustry] = useState<string>('ALL');
  const [dept, setDept] = useState<string>('ALL');
  const [sortBy, setSortBy] = useState<'market_cap' | 'name' | 'symbol'>('market_cap');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [searchQuery, setSearchQuery] = useState('');

  // Pagination
  const [currentPage, setCurrentPage] = useState(1);
  const [limit] = useState(50);

  // Load filters and watchlist on mount
  useEffect(() => {
    loadFilters();
    loadWatchlist();
  }, []);

  // Load stocks when filters change
  useEffect(() => {
    loadStocks();
  }, [marketType, sector, industry, dept, sortBy, sortOrder, currentPage]);

  const loadFilters = async () => {
    try {
      const data = await stockApi.getFilters();
      setFilters(data);
    } catch (error) {
      console.error('Failed to load filters:', error);
    }
  };

  const loadWatchlist = async () => {
    try {
      const symbols = await watchlistApi.getWatchlistSymbols();
      setWatchlistSymbols(new Set(symbols));
    } catch (error) {
      console.error('Failed to load watchlist:', error);
    }
  };

  const loadStocks = async () => {
    setLoading(true);
    try {
      const params: StockListParams = {
        market_type: marketType,
        sector: sector === 'ALL' ? undefined : sector,
        industry: industry === 'ALL' ? undefined : industry,
        dept: dept === 'ALL' ? undefined : dept,
        sort_by: sortBy,
        sort_order: sortOrder,
        skip: (currentPage - 1) * limit,
        limit,
      };

      const data = await stockApi.listStocks(params);
      setStocks(data.stocks);
      setTotal(data.total);
    } catch (error) {
      console.error('Failed to load stocks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      loadStocks();
      return;
    }

    setLoading(true);
    try {
      const data = await stockApi.searchStocks({
        query: searchQuery,
        market_type: marketType,
        limit: 50,
      });
      setStocks(data.stocks);
      setTotal(data.total);
      setCurrentPage(1);
    } catch (error) {
      console.error('Failed to search stocks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleClearFilters = () => {
    setMarketType('ALL');
    setSector('ALL');
    setIndustry('ALL');
    setDept('ALL');
    setSearchQuery('');
    setCurrentPage(1);
  };

  const handleStockClick = (stock: Stock) => {
    router.push(`/market?symbol=${stock.symbol}`);
  };

  const handleWatchlistToggle = (symbol: string, isInWatchlist: boolean) => {
    setWatchlistSymbols(prev => {
      const newSet = new Set(prev);
      if (isInWatchlist) {
        newSet.add(symbol);
      } else {
        newSet.delete(symbol);
      }
      return newSet;
    });
  };

  const formatMarketCap = (marketCap: number | null | undefined): string => {
    if (!marketCap) return 'N/A';
    const trillion = marketCap / 1_000_000_000_000;
    if (trillion >= 1) return `${trillion.toFixed(2)}조`;
    const billion = marketCap / 100_000_000;
    return `${billion.toFixed(0)}억`;
  };

  const totalPages = Math.ceil(total / limit);

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold">종목 탐색</h1>
          <p className="text-muted-foreground">
            시가총액, 섹터, 산업별로 종목을 검색하고 필터링하세요
          </p>
        </div>

        {/* Filters */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Filter className="h-5 w-5" />
              필터
            </CardTitle>
            <CardDescription>종목을 필터링하고 정렬하세요</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Search Bar */}
            <div className="flex gap-2">
              <div className="flex-1">
                <Input
                  placeholder="종목명 또는 코드로 검색..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                />
              </div>
              <Button onClick={handleSearch} disabled={loading}>
                <Search className="h-4 w-4 mr-2" />
                검색
              </Button>
            </div>

            {/* Filter Controls */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {/* Market Type */}
              <div className="space-y-2">
                <Label>시장</Label>
                <Select value={marketType} onValueChange={(value: any) => {
                  setMarketType(value);
                  setCurrentPage(1);
                }}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="ALL">전체</SelectItem>
                    <SelectItem value="KOSPI">KOSPI</SelectItem>
                    <SelectItem value="KOSDAQ">KOSDAQ</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Sector */}
              <div className="space-y-2">
                <Label>섹터</Label>
                <Select value={sector} onValueChange={(value) => {
                  setSector(value);
                  setCurrentPage(1);
                }}>
                  <SelectTrigger>
                    <SelectValue placeholder="전체" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="ALL">전체</SelectItem>
                    {filters?.sectors.map((s) => (
                      <SelectItem key={s} value={s}>{s}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Industry */}
              <div className="space-y-2">
                <Label>산업</Label>
                <Select value={industry} onValueChange={(value) => {
                  setIndustry(value);
                  setCurrentPage(1);
                }}>
                  <SelectTrigger>
                    <SelectValue placeholder="전체" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="ALL">전체</SelectItem>
                    {filters?.industries.map((i) => (
                      <SelectItem key={i} value={i}>{i}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Dept */}
              <div className="space-y-2">
                <Label>부문</Label>
                <Select value={dept} onValueChange={(value) => {
                  setDept(value);
                  setCurrentPage(1);
                }}>
                  <SelectTrigger>
                    <SelectValue placeholder="전체" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="ALL">전체</SelectItem>
                    {filters?.depts.map((d) => (
                      <SelectItem key={d} value={d}>{d}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Sort By */}
              <div className="space-y-2">
                <Label>정렬 기준</Label>
                <Select value={sortBy} onValueChange={(value: any) => setSortBy(value)}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="market_cap">시가총액</SelectItem>
                    <SelectItem value="name">이름</SelectItem>
                    <SelectItem value="symbol">코드</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Sort Order */}
              <div className="space-y-2">
                <Label>정렬 순서</Label>
                <Select value={sortOrder} onValueChange={(value: any) => setSortOrder(value)}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="desc">내림차순</SelectItem>
                    <SelectItem value="asc">오름차순</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Clear Filters */}
              <div className="space-y-2 flex items-end">
                <Button variant="outline" onClick={handleClearFilters} className="w-full">
                  필터 초기화
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Results */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                종목 목록
              </span>
              <span className="text-sm font-normal text-muted-foreground">
                총 {total.toLocaleString()}개
              </span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="flex justify-center items-center py-12">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
              </div>
            ) : stocks.length === 0 ? (
              <div className="text-center py-12 text-muted-foreground">
                검색 결과가 없습니다
              </div>
            ) : (
              <>
                <div className="rounded-md border">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead className="w-[50px]"></TableHead>
                        <TableHead className="w-[100px]">코드</TableHead>
                        <TableHead>종목명</TableHead>
                        <TableHead>시장</TableHead>
                        <TableHead>섹터</TableHead>
                        <TableHead>산업</TableHead>
                        <TableHead>부문</TableHead>
                        <TableHead className="text-right">시가총액</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {stocks.map((stock) => (
                        <TableRow
                          key={stock.id}
                          className="cursor-pointer hover:bg-muted/50"
                          onClick={() => handleStockClick(stock)}
                        >
                          <TableCell>
                            <WatchlistButton
                              symbol={stock.symbol}
                              stockName={stock.name}
                              isInWatchlist={watchlistSymbols.has(stock.symbol)}
                              onToggle={(isInWatchlist) => handleWatchlistToggle(stock.symbol, isInWatchlist)}
                            />
                          </TableCell>
                          <TableCell className="font-mono">{stock.symbol}</TableCell>
                          <TableCell className="font-medium">{stock.name}</TableCell>
                          <TableCell>
                            <span className={`px-2 py-1 rounded text-xs ${
                              stock.market_type === 'KOSPI'
                                ? 'bg-blue-100 text-blue-700'
                                : 'bg-green-100 text-green-700'
                            }`}>
                              {stock.market_type}
                            </span>
                          </TableCell>
                          <TableCell>{stock.sector || '-'}</TableCell>
                          <TableCell>{stock.industry || '-'}</TableCell>
                          <TableCell>{stock.dept || '-'}</TableCell>
                          <TableCell className="text-right font-mono">
                            {formatMarketCap(stock.market_cap)}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>

                {/* Pagination */}
                {totalPages > 1 && (
                  <div className="flex items-center justify-between mt-4">
                    <div className="text-sm text-muted-foreground">
                      Page {currentPage} of {totalPages}
                    </div>
                    <div className="flex gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setCurrentPage(currentPage - 1)}
                        disabled={currentPage === 1}
                      >
                        <ChevronLeft className="h-4 w-4" />
                        이전
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setCurrentPage(currentPage + 1)}
                        disabled={currentPage === totalPages}
                      >
                        다음
                        <ChevronRight className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                )}
              </>
            )}
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}

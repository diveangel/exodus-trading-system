'use client';

import { useMemo, useState } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import type { ChartDataPoint } from '@/types/market';

interface MarketDataTableProps {
  data: ChartDataPoint[];
}

const ROWS_PER_PAGE = 10;

export function MarketDataTable({ data }: MarketDataTableProps) {
  const [currentPage, setCurrentPage] = useState(1);

  // Reverse data to show latest first
  const reversedData = useMemo(() => {
    return [...data].reverse();
  }, [data]);

  // Pagination
  const totalPages = Math.ceil(reversedData.length / ROWS_PER_PAGE);
  const startIndex = (currentPage - 1) * ROWS_PER_PAGE;
  const endIndex = startIndex + ROWS_PER_PAGE;
  const currentData = reversedData.slice(startIndex, endIndex);

  const handlePrevPage = () => {
    setCurrentPage(prev => Math.max(1, prev - 1));
  };

  const handleNextPage = () => {
    setCurrentPage(prev => Math.min(totalPages, prev + 1));
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('ko-KR', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getChangeColor = (open: number, close: number) => {
    if (close > open) return 'text-red-600';
    if (close < open) return 'text-blue-600';
    return '';
  };

  const getChangePercent = (open: number, close: number) => {
    if (open === 0) return 0;
    return ((close - open) / open * 100);
  };

  return (
    <div className="space-y-4">
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>시간</TableHead>
              <TableHead className="text-right">시가</TableHead>
              <TableHead className="text-right">고가</TableHead>
              <TableHead className="text-right">저가</TableHead>
              <TableHead className="text-right">종가</TableHead>
              <TableHead className="text-right">등락률</TableHead>
              <TableHead className="text-right">거래량</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {currentData.length === 0 ? (
              <TableRow>
                <TableCell colSpan={7} className="text-center text-muted-foreground">
                  데이터가 없습니다
                </TableCell>
              </TableRow>
            ) : (
              currentData.map((row, index) => {
                const changePercent = getChangePercent(row.open, row.close);
                const changeColor = getChangeColor(row.open, row.close);

                return (
                  <TableRow key={`${row.timestamp}-${index}`}>
                    <TableCell className="font-medium">
                      {formatDate(row.timestamp)}
                    </TableCell>
                    <TableCell className="text-right">
                      {row.open.toLocaleString()}
                    </TableCell>
                    <TableCell className="text-right text-red-600">
                      {row.high.toLocaleString()}
                    </TableCell>
                    <TableCell className="text-right text-blue-600">
                      {row.low.toLocaleString()}
                    </TableCell>
                    <TableCell className={`text-right font-semibold ${changeColor}`}>
                      {row.close.toLocaleString()}
                    </TableCell>
                    <TableCell className={`text-right font-semibold ${changeColor}`}>
                      {changePercent >= 0 ? '+' : ''}{changePercent.toFixed(2)}%
                    </TableCell>
                    <TableCell className="text-right">
                      {row.volume.toLocaleString()}
                    </TableCell>
                  </TableRow>
                );
              })
            )}
          </TableBody>
        </Table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between">
          <p className="text-sm text-muted-foreground">
            총 {reversedData.length}개 중 {startIndex + 1}-{Math.min(endIndex, reversedData.length)}개 표시
          </p>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={handlePrevPage}
              disabled={currentPage === 1}
            >
              <ChevronLeft className="h-4 w-4" />
              이전
            </Button>
            <span className="text-sm">
              {currentPage} / {totalPages}
            </span>
            <Button
              variant="outline"
              size="sm"
              onClick={handleNextPage}
              disabled={currentPage === totalPages}
            >
              다음
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}

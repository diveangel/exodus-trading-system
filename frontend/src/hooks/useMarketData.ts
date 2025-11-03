import { useState, useEffect, useCallback } from 'react';
import { apiClient } from '@/lib/api';
import type { ChartDataResponse, PriceResponse, MarketDataListResponse, TimeInterval } from '@/types/market';

export function useMarketData(symbol: string, interval: TimeInterval, days: number) {
  const [chartData, setChartData] = useState<ChartDataResponse | null>(null);
  const [currentPrice, setCurrentPrice] = useState<PriceResponse | null>(null);
  const [isLoadingChart, setIsLoadingChart] = useState(false);
  const [isLoadingPrice, setIsLoadingPrice] = useState(false);
  const [isCollecting, setIsCollecting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Get chart data from database
  const fetchChartData = useCallback(async () => {
    if (!symbol) return;

    setIsLoadingChart(true);
    setError(null);

    try {
      const response = await apiClient.get<ChartDataResponse>(
        `/market/chart/${symbol}`,
        {
          params: { interval, days }
        }
      );
      setChartData(response.data);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || '차트 데이터를 불러오는데 실패했습니다';
      setError(errorMessage);
      setChartData(null);
    } finally {
      setIsLoadingChart(false);
    }
  }, [symbol, interval, days]);

  // Get current price from KIS API
  const fetchCurrentPrice = useCallback(async () => {
    if (!symbol) return;

    setIsLoadingPrice(true);
    setError(null);

    try {
      const response = await apiClient.get<PriceResponse>(
        `/market/price/${symbol}`
      );
      setCurrentPrice(response.data);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || '현재가를 불러오는데 실패했습니다';
      console.error('Failed to fetch current price:', errorMessage);
      // Don't set error state for price fetch failures
    } finally {
      setIsLoadingPrice(false);
    }
  }, [symbol]);

  // Collect daily data from KIS API
  const collectDailyData = useCallback(async () => {
    if (!symbol) return;

    setIsCollecting(true);
    setError(null);

    try {
      const response = await apiClient.post<MarketDataListResponse>(
        `/market/collect/daily/${symbol}`,
        null,
        { params: { period: 'D' } }
      );

      return response.data;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || '데이터 수집에 실패했습니다';
      setError(errorMessage);
      throw err;
    } finally {
      setIsCollecting(false);
    }
  }, [symbol]);

  // Collect minute data from KIS API
  const collectMinuteData = useCallback(async () => {
    if (!symbol) return;

    setIsCollecting(true);
    setError(null);

    try {
      const response = await apiClient.post<MarketDataListResponse>(
        `/market/collect/minute/${symbol}`,
        null,
        { params: { interval } }
      );

      return response.data;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || '데이터 수집에 실패했습니다';
      setError(errorMessage);
      throw err;
    } finally {
      setIsCollecting(false);
    }
  }, [symbol, interval]);

  // Auto-fetch chart data on mount and when dependencies change
  useEffect(() => {
    fetchChartData();
  }, [fetchChartData]);

  // Auto-fetch current price on mount
  useEffect(() => {
    fetchCurrentPrice();
  }, [fetchCurrentPrice]);

  return {
    chartData,
    currentPrice,
    isLoadingChart,
    isLoadingPrice,
    isCollecting,
    collectDailyData,
    collectMinuteData,
    refreshChartData: fetchChartData,
    refreshCurrentPrice: fetchCurrentPrice,
    error
  };
}

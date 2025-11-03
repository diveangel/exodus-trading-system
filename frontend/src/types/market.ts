export type TimeInterval = '1m' | '5m' | '10m' | '30m' | '1h' | '1d';

export interface ChartDataPoint {
  timestamp: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface ChartDataResponse {
  symbol: string;
  interval: TimeInterval;
  data: ChartDataPoint[];
}

export interface PriceResponse {
  symbol: string;
  price: number;
  change: number;
  changePercent: number;
  volume: number;
  timestamp: string;
}

export interface MarketDataResponse {
  id: number;
  symbol: string;
  timestamp: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  interval: TimeInterval;
  created_at: string;
}

export interface MarketDataListResponse {
  data: MarketDataResponse[];
  symbol: string;
  interval: TimeInterval;
  start_date: string;
  end_date: string;
  total: number;
}

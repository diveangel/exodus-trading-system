export type MarketType = 'KOSPI' | 'KOSDAQ' | 'ALL';

export interface Stock {
  id: number;
  symbol: string;
  standard_code: string;
  name: string;
  market_type: 'KOSPI' | 'KOSDAQ';
  created_at: string;
  updated_at: string;
}

export interface StockSearchParams {
  query: string;
  market_type?: MarketType;
  limit?: number;
}

export interface StockListResponse {
  total: number;
  stocks: Stock[];
}

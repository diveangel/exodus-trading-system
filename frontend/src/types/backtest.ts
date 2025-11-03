export type BacktestStatus = 'pending' | 'running' | 'completed' | 'failed'

export interface BacktestConfig {
  strategy_id: number
  start_date: string
  end_date: string
  initial_capital: number
  commission_rate: number
  slippage_rate: number
  symbols?: string[]
}

export interface BacktestResult {
  id: number
  strategy_id: number
  strategy_name: string
  status: BacktestStatus
  config: BacktestConfig
  created_at: string
  started_at?: string
  completed_at?: string

  // Performance metrics
  total_return?: number
  total_return_percent?: number
  annualized_return?: number
  sharpe_ratio?: number
  sortino_ratio?: number
  max_drawdown?: number
  max_drawdown_duration?: number
  win_rate?: number
  profit_factor?: number
  total_trades?: number
  winning_trades?: number
  losing_trades?: number
  avg_win?: number
  avg_loss?: number

  // Additional info
  error_message?: string
  logs?: string
}

export interface BacktestTrade {
  id: number
  backtest_id: number
  symbol: string
  side: 'BUY' | 'SELL'
  quantity: number
  price: number
  executed_at: string
  profit_loss?: number
  profit_loss_percent?: number
  position_type: 'OPEN' | 'CLOSE'
}

export interface BacktestEquityCurve {
  date: string
  equity: number
  daily_return: number
  cumulative_return: number
}

export const BACKTEST_STATUS_LABELS: Record<BacktestStatus, string> = {
  pending: '대기중',
  running: '실행중',
  completed: '완료',
  failed: '실패',
}

export const BACKTEST_STATUS_COLORS: Record<BacktestStatus, string> = {
  pending: 'bg-gray-100 text-gray-700',
  running: 'bg-blue-100 text-blue-700',
  completed: 'bg-green-100 text-green-700',
  failed: 'bg-red-100 text-red-700',
}

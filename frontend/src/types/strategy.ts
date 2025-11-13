// Backend에서 사용하는 enum 값 (대문자)
export type StrategyType = 'MOMENTUM' | 'MEAN_REVERSION' | 'BREAKOUT' | 'CUSTOM'

export type StrategyStatus = 'ACTIVE' | 'INACTIVE' | 'BACKTESTING'

export interface Strategy {
  id: number
  name: string
  description?: string
  strategy_type: StrategyType  // Backend 필드명과 일치
  status: StrategyStatus
  parameters: Record<string, any>
  created_at: string
  updated_at: string
  user_id: number
  // Performance metrics (아직 구현 안됨)
  total_profit_loss?: number
  profit_loss_percent?: number
  total_trades?: number
  win_rate?: number
  sharpe_ratio?: number
  max_drawdown?: number
}

export interface CreateStrategyRequest {
  name: string
  description?: string
  strategy_type: StrategyType
  parameters: Record<string, any>
}

export interface UpdateStrategyRequest {
  name?: string
  description?: string
  strategy_type?: StrategyType
  parameters?: Record<string, any>
  status?: StrategyStatus
}

export const STRATEGY_TYPE_LABELS: Record<StrategyType, string> = {
  MOMENTUM: '모멘텀 전략',
  MEAN_REVERSION: '평균회귀 전략',
  BREAKOUT: '변동성 돌파 전략',
  CUSTOM: '커스텀 전략',
}

export const STRATEGY_STATUS_LABELS: Record<StrategyStatus, string> = {
  ACTIVE: '운영중',
  INACTIVE: '비활성',
  BACKTESTING: '백테스트중',
}

export const STRATEGY_STATUS_COLORS: Record<StrategyStatus, string> = {
  ACTIVE: 'bg-green-100 text-green-700',
  INACTIVE: 'bg-gray-100 text-gray-700',
  BACKTESTING: 'bg-blue-100 text-blue-700',
}

// API 응답 타입
export interface StrategyListResponse {
  strategies: Strategy[]
  total: number
  page: number
  page_size: number
}

export interface ExecuteStrategyResponse {
  strategy_id: number
  strategy_name: string
  symbols: string[]
  executed_at: string
  signals: Signal[]
  total_signals: number
  total_symbols: number
}

export interface Signal {
  timestamp: string
  symbol: string
  signal_type: 'BUY' | 'SELL' | 'HOLD'
  price: number
  quantity: number | null
  reason: string
  confidence: number
}

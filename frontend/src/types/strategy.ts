export type StrategyType = 'momentum' | 'mean_reversion' | 'breakout' | 'arbitrage' | 'custom'

export type StrategyStatus = 'active' | 'paused' | 'stopped' | 'error'

export interface Strategy {
  id: number
  name: string
  description: string
  type: StrategyType
  status: StrategyStatus
  parameters: Record<string, any>
  created_at: string
  updated_at: string
  user_id: number
  is_active: boolean
  // Performance metrics
  total_profit_loss?: number
  profit_loss_percent?: number
  total_trades?: number
  win_rate?: number
  sharpe_ratio?: number
  max_drawdown?: number
}

export interface CreateStrategyRequest {
  name: string
  description: string
  type: StrategyType
  parameters: Record<string, any>
}

export interface UpdateStrategyRequest {
  name?: string
  description?: string
  type?: StrategyType
  parameters?: Record<string, any>
  is_active?: boolean
}

export const STRATEGY_TYPE_LABELS: Record<StrategyType, string> = {
  momentum: '모멘텀 전략',
  mean_reversion: '평균회귀 전략',
  breakout: '변동성 돌파 전략',
  arbitrage: '차익거래 전략',
  custom: '커스텀 전략',
}

export const STRATEGY_STATUS_LABELS: Record<StrategyStatus, string> = {
  active: '운영중',
  paused: '일시정지',
  stopped: '중지됨',
  error: '오류',
}

export const STRATEGY_STATUS_COLORS: Record<StrategyStatus, string> = {
  active: 'bg-green-100 text-green-700',
  paused: 'bg-yellow-100 text-yellow-700',
  stopped: 'bg-gray-100 text-gray-700',
  error: 'bg-red-100 text-red-700',
}

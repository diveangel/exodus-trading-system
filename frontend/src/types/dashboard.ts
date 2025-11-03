/**
 * Dashboard types
 */

export interface DashboardStats {
  total_balance: number
  profit_loss: number
  profit_loss_percent: number
  active_strategies: number
  today_trades: number
}

export interface ActiveStrategy {
  id: number
  name: string
  status: string
  profit_loss: number
  profit_loss_percent: number
}

export interface RecentActivity {
  id: number
  type: 'BUY' | 'SELL'
  symbol: string
  quantity: number
  price: number
  time: string
  created_at?: string | null
}

export interface DashboardData {
  stats: DashboardStats
  active_strategies: ActiveStrategy[]
  recent_activities: RecentActivity[]
}

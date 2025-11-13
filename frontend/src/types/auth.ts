/**
 * Authentication related type definitions
 */

export interface User {
  id: number
  email: string
  full_name: string
  role: 'admin' | 'user' | 'viewer'
  is_active: boolean
  is_verified: boolean
  has_real_credentials: boolean
  has_mock_credentials: boolean
  kis_trading_mode: 'MOCK' | 'REAL'
  created_at: string
  updated_at: string
}

export interface LoginRequest {
  email: string
  password: string
  kis_trading_mode: 'MOCK' | 'REAL'
}

export interface RegisterRequest {
  email: string
  password: string
  full_name: string
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  token_type: string
  user: User
}

export interface AuthState {
  user: User | null
  accessToken: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  isLoading: boolean
}

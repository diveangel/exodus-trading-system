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
  has_kis_credentials: boolean
  created_at: string
  updated_at: string
}

export interface LoginRequest {
  email: string
  password: string
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
}

export interface AuthState {
  user: User | null
  accessToken: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  isLoading: boolean
}

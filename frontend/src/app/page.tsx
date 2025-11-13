'use client'

import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import { Button } from '@/components/ui/button'
import { useAuthStore } from '@/store/authStore'
import { TrendingUp, BarChart3, Activity, Shield } from 'lucide-react'

export default function Home() {
  const router = useRouter()
  const [mounted, setMounted] = useState(false)
  const { isAuthenticated } = useAuthStore()

  useEffect(() => {
    setMounted(true)
  }, [])

  useEffect(() => {
    if (mounted && isAuthenticated) {
      router.push('/dashboard')
    }
  }, [mounted, isAuthenticated, router])

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <div className="flex items-center justify-center mb-6">
            <div className="h-16 w-16 rounded-full bg-primary flex items-center justify-center">
              <TrendingUp className="h-8 w-8 text-primary-foreground" />
            </div>
          </div>
          <h1 className="text-5xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
            Exodus Trading System
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            데이터 기반 퀀트 투자 전략으로 체계적인 자동매매를 실현하세요
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/login">
              <Button size="lg" className="px-8">
                로그인
              </Button>
            </Link>
            <Link href="/register">
              <Button size="lg" variant="outline" className="px-8">
                회원가입
              </Button>
            </Link>
          </div>
        </div>

        {/* Features Section */}
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto mt-20">
          <div className="bg-white p-6 rounded-lg shadow-sm border hover:shadow-md transition">
            <div className="h-12 w-12 rounded-full bg-blue-100 flex items-center justify-center mb-4">
              <BarChart3 className="h-6 w-6 text-blue-600" />
            </div>
            <h3 className="text-lg font-semibold mb-2">전략 백테스트</h3>
            <p className="text-gray-600 text-sm">
              과거 데이터로 투자 전략을 검증하고 최적화하세요. 수익률, MDD, 샤프 지수 등 상세한 성과 지표를 제공합니다.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border hover:shadow-md transition">
            <div className="h-12 w-12 rounded-full bg-indigo-100 flex items-center justify-center mb-4">
              <Activity className="h-6 w-6 text-indigo-600" />
            </div>
            <h3 className="text-lg font-semibold mb-2">퀀트 전략</h3>
            <p className="text-gray-600 text-sm">
              모멘텀, 평균 회귀, 팩터 투자 등 다양한 퀀트 전략을 활용하여 감정을 배제한 체계적인 투자를 실행하세요.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border hover:shadow-md transition">
            <div className="h-12 w-12 rounded-full bg-purple-100 flex items-center justify-center mb-4">
              <Shield className="h-6 w-6 text-purple-600" />
            </div>
            <h3 className="text-lg font-semibold mb-2">안전한 연동</h3>
            <p className="text-gray-600 text-sm">
              한국투자증권 OpenAPI를 통한 안전한 계좌 연동과 실시간 시장 데이터를 제공합니다.
            </p>
          </div>
        </div>

        {/* Stats Section */}
        <div className="mt-20 text-center">
          <div className="grid md:grid-cols-3 gap-8 max-w-3xl mx-auto">
            <div>
              <div className="text-3xl font-bold text-primary mb-2">10+</div>
              <div className="text-sm text-gray-600">투자 전략</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary mb-2">100%</div>
              <div className="text-sm text-gray-600">자동화</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary mb-2">24/7</div>
              <div className="text-sm text-gray-600">모니터링</div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t mt-20 py-8">
        <div className="container mx-auto px-4 text-center text-sm text-gray-600">
          <p>&copy; 2025 Exodus Trading System. All rights reserved.</p>
        </div>
      </footer>
    </main>
  )
}

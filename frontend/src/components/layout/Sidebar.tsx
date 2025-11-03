'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'
import {
  LayoutDashboard,
  TrendingUp,
  BarChart3,
  Wallet,
  History,
  Settings,
  X,
  LineChart,
} from 'lucide-react'
import { Button } from '@/components/ui/button'

interface SidebarProps {
  isOpen?: boolean
  onClose?: () => void
}

const menuItems = [
  {
    title: '대시보드',
    href: '/dashboard',
    icon: LayoutDashboard,
  },
  {
    title: '시장 데이터',
    href: '/market',
    icon: LineChart,
  },
  {
    title: '전략 관리',
    href: '/strategies',
    icon: TrendingUp,
  },
  {
    title: '백테스트',
    href: '/backtest',
    icon: BarChart3,
  },
  {
    title: '계좌 정보',
    href: '/account',
    icon: Wallet,
  },
  {
    title: '거래 내역',
    href: '/trades',
    icon: History,
  },
  {
    title: '설정',
    href: '/settings',
    icon: Settings,
  },
]

export function Sidebar({ isOpen = true, onClose }: SidebarProps) {
  const pathname = usePathname()

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && onClose && (
        <div
          className="fixed inset-0 z-40 bg-black/50 md:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          'fixed left-0 top-16 z-40 h-[calc(100vh-4rem)] w-64 border-r bg-background transition-transform md:sticky md:translate-x-0',
          isOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        <div className="flex h-full flex-col gap-2">
          {/* Close button for mobile */}
          {onClose && (
            <div className="flex justify-end p-4 md:hidden">
              <Button
                variant="ghost"
                size="icon"
                onClick={onClose}
              >
                <X className="h-5 w-5" />
              </Button>
            </div>
          )}

          {/* Navigation */}
          <nav className="flex-1 space-y-1 px-3 py-4">
            {menuItems.map((item) => {
              const Icon = item.icon
              const isActive = pathname === item.href || pathname?.startsWith(item.href + '/')

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={onClose}
                  className={cn(
                    'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                    isActive
                      ? 'bg-primary text-primary-foreground'
                      : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
                  )}
                >
                  <Icon className="h-5 w-5" />
                  {item.title}
                </Link>
              )
            })}
          </nav>

          {/* Footer info */}
          <div className="border-t p-4">
            <div className="text-xs text-muted-foreground">
              <p className="font-medium">Exodus Trading System</p>
              <p className="mt-1">Version 0.1.0 MVP</p>
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}

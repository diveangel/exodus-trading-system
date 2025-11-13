'use client'

import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { DashboardLayout } from '@/components/layout/DashboardLayout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Settings as SettingsIcon,
  Key,
  Bell,
  Shield,
  Save,
  Eye,
  EyeOff,
  Loader2,
  Trash2,
} from 'lucide-react'
import { accountApi } from '@/lib/accountApi'
import { useAuthStore } from '@/store/authStore'

const realKisApiSchema = z.object({
  app_key: z.string().min(1, 'App Key를 입력해주세요'),
  app_secret: z.string().min(1, 'App Secret을 입력해주세요'),
  account_number: z.string().regex(/^\d{8}-\d{2}$/, '계좌번호 형식: 12345678-01'),
})

const mockKisApiSchema = z.object({
  app_key: z.string().min(1, 'App Key를 입력해주세요'),
  app_secret: z.string().min(1, 'App Secret을 입력해주세요'),
  account_number: z.string().regex(/^\d{8}-\d{2}$/, '계좌번호 형식: 12345678-01'),
})

type RealKisApiFormData = z.infer<typeof realKisApiSchema>
type MockKisApiFormData = z.infer<typeof mockKisApiSchema>

export default function SettingsPage() {
  const { user } = useAuthStore()
  const [showRealSecrets, setShowRealSecrets] = useState(false)
  const [showMockSecrets, setShowMockSecrets] = useState(false)
  const [isSaving, setIsSaving] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [hasRealCredentials, setHasRealCredentials] = useState(false)
  const [hasMockCredentials, setHasMockCredentials] = useState(false)

  // Notification settings
  const [emailNotifications, setEmailNotifications] = useState(true)
  const [tradeAlerts, setTradeAlerts] = useState(true)
  const [strategyAlerts, setStrategyAlerts] = useState(true)
  const [errorAlerts, setErrorAlerts] = useState(true)

  // Risk management settings
  const [dailyLossLimit, setDailyLossLimit] = useState(500000)
  const [maxPositionSize, setMaxPositionSize] = useState(1000000)
  const [maxPositions, setMaxPositions] = useState(5)

  const {
    register: registerReal,
    handleSubmit: handleSubmitReal,
    formState: { errors: errorsReal },
    reset: resetReal,
  } = useForm<RealKisApiFormData>({
    resolver: zodResolver(realKisApiSchema),
  })

  const {
    register: registerMock,
    handleSubmit: handleSubmitMock,
    formState: { errors: errorsMock },
    reset: resetMock,
  } = useForm<MockKisApiFormData>({
    resolver: zodResolver(mockKisApiSchema),
  })

  // Load KIS credentials on mount
  useEffect(() => {
    const loadKISCredentials = async () => {
      try {
        setIsLoading(true)
        const credentials = await accountApi.getKISCredentials()

        setHasRealCredentials(credentials.has_real_credentials)
        setHasMockCredentials(credentials.has_mock_credentials)

        // Format account numbers
        const realAccountNumber = credentials.real_account_number && credentials.real_account_code
          ? `${credentials.real_account_number}-${credentials.real_account_code}`
          : ''
        const mockAccountNumber = credentials.mock_account_number && credentials.mock_account_code
          ? `${credentials.mock_account_number}-${credentials.mock_account_code}`
          : ''

        resetReal({
          app_key: '', // Don't load actual keys for security
          app_secret: '',
          account_number: realAccountNumber,
        })

        resetMock({
          app_key: '', // Don't load actual keys for security
          app_secret: '',
          account_number: mockAccountNumber,
        })
      } catch (error) {
        console.error('Failed to load KIS credentials:', error)
      } finally {
        setIsLoading(false)
      }
    }

    loadKISCredentials()
  }, [resetReal, resetMock])

  const onSubmitRealKisApi = async (data: RealKisApiFormData) => {
    setIsSaving(true)
    try {
      // Parse account number and code
      const [accountNumber, accountCode] = data.account_number.split('-')

      await accountApi.updateRealKISCredentials({
        real_app_key: data.app_key,
        real_app_secret: data.app_secret,
        real_account_number: accountNumber,
        real_account_code: accountCode,
      })

      setHasRealCredentials(true)
      alert('실전투자 API 설정이 저장되었습니다.')
    } catch (error: any) {
      console.error('Failed to save Real KIS API credentials:', error)
      alert(error.response?.data?.detail || '저장에 실패했습니다.')
    } finally {
      setIsSaving(false)
    }
  }

  const onSubmitMockKisApi = async (data: MockKisApiFormData) => {
    setIsSaving(true)
    try {
      // Parse account number and code
      const [accountNumber, accountCode] = data.account_number.split('-')

      await accountApi.updateMockKISCredentials({
        mock_app_key: data.app_key,
        mock_app_secret: data.app_secret,
        mock_account_number: accountNumber,
        mock_account_code: accountCode,
      })

      setHasMockCredentials(true)
      alert('모의투자 API 설정이 저장되었습니다.')
    } catch (error: any) {
      console.error('Failed to save Mock KIS API credentials:', error)
      alert(error.response?.data?.detail || '저장에 실패했습니다.')
    } finally {
      setIsSaving(false)
    }
  }

  const handleDeleteRealCredentials = async () => {
    if (!confirm('실전투자 API 인증 정보를 삭제하시겠습니까?')) {
      return
    }

    setIsSaving(true)
    try {
      await accountApi.deleteRealKISCredentials()
      setHasRealCredentials(false)
      resetReal({
        app_key: '',
        app_secret: '',
        account_number: '',
      })
      alert('실전투자 API 인증 정보가 삭제되었습니다.')
    } catch (error: any) {
      console.error('Failed to delete Real KIS credentials:', error)
      alert(error.response?.data?.detail || '삭제에 실패했습니다.')
    } finally {
      setIsSaving(false)
    }
  }

  const handleDeleteMockCredentials = async () => {
    if (!confirm('모의투자 API 인증 정보를 삭제하시겠습니까?')) {
      return
    }

    setIsSaving(true)
    try {
      await accountApi.deleteMockKISCredentials()
      setHasMockCredentials(false)
      resetMock({
        app_key: '',
        app_secret: '',
        account_number: '',
      })
      alert('모의투자 API 인증 정보가 삭제되었습니다.')
    } catch (error: any) {
      console.error('Failed to delete Mock KIS credentials:', error)
      alert(error.response?.data?.detail || '삭제에 실패했습니다.')
    } finally {
      setIsSaving(false)
    }
  }

  const handleSaveNotifications = async () => {
    setIsSaving(true)
    try {
      // TODO: Call API to save notification settings
      console.log('Saving notification settings:', {
        emailNotifications,
        tradeAlerts,
        strategyAlerts,
        errorAlerts,
      })
      await new Promise((resolve) => setTimeout(resolve, 1000))
      alert('알림 설정이 저장되었습니다.')
    } catch (error) {
      console.error('Failed to save notification settings:', error)
      alert('저장에 실패했습니다.')
    } finally {
      setIsSaving(false)
    }
  }

  const handleSaveRiskManagement = async () => {
    setIsSaving(true)
    try {
      // TODO: Call API to save risk management settings
      console.log('Saving risk management settings:', {
        dailyLossLimit,
        maxPositionSize,
        maxPositions,
      })
      await new Promise((resolve) => setTimeout(resolve, 1000))
      alert('리스크 관리 설정이 저장되었습니다.')
    } catch (error) {
      console.error('Failed to save risk management settings:', error)
      alert('저장에 실패했습니다.')
    } finally {
      setIsSaving(false)
    }
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('ko-KR', {
      style: 'currency',
      currency: 'KRW',
      maximumFractionDigits: 0,
    }).format(amount)
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Page Header */}
        <div>
          <h1 className="text-3xl font-bold tracking-tight">설정</h1>
          <p className="text-muted-foreground">
            시스템 설정 및 API 연동을 관리하세요
          </p>
          {user && (
            <p className="text-sm text-muted-foreground mt-2">
              현재 거래 모드: <span className="font-semibold">{user.kis_trading_mode === 'REAL' ? '실전투자' : '모의투자'}</span>
            </p>
          )}
        </div>

        {/* KIS API Settings with Tabs */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Key className="h-5 w-5" />
              <CardTitle>한국투자증권 API 설정</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="flex items-center justify-center py-8">
                <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
              </div>
            ) : (
              <Tabs defaultValue="mock" className="w-full">
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="mock">모의투자</TabsTrigger>
                  <TabsTrigger value="real">실전투자</TabsTrigger>
                </TabsList>

                {/* Mock Trading Tab */}
                <TabsContent value="mock" className="space-y-4 mt-4">
                  <div className="bg-blue-50 border border-blue-200 rounded-md p-3 mb-4">
                    <p className="text-sm text-blue-800">
                      모의투자는 실제 자금 없이 거래를 테스트할 수 있습니다. 한국투자증권 모의투자 API 키가 필요합니다.
                    </p>
                  </div>

                  {hasMockCredentials && (
                    <div className="bg-green-50 border border-green-200 rounded-md p-3 flex items-center justify-between">
                      <p className="text-sm text-green-800">
                        모의투자 API 인증 정보가 등록되어 있습니다.
                      </p>
                      <Button
                        type="button"
                        variant="destructive"
                        size="sm"
                        onClick={handleDeleteMockCredentials}
                        disabled={isSaving}
                      >
                        <Trash2 className="h-4 w-4 mr-1" />
                        삭제
                      </Button>
                    </div>
                  )}

                  <form onSubmit={handleSubmitMock(onSubmitMockKisApi)} className="space-y-4">
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <Label htmlFor="mock_app_key">App Key *</Label>
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          onClick={() => setShowMockSecrets(!showMockSecrets)}
                        >
                          {showMockSecrets ? (
                            <EyeOff className="h-4 w-4" />
                          ) : (
                            <Eye className="h-4 w-4" />
                          )}
                        </Button>
                      </div>
                      <Input
                        id="mock_app_key"
                        type={showMockSecrets ? 'text' : 'password'}
                        placeholder="모의투자 App Key를 입력하세요"
                        {...registerMock('app_key')}
                      />
                      {errorsMock.app_key && (
                        <p className="text-sm text-red-600">
                          {errorsMock.app_key.message}
                        </p>
                      )}
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="mock_app_secret">App Secret *</Label>
                      <Input
                        id="mock_app_secret"
                        type={showMockSecrets ? 'text' : 'password'}
                        placeholder="모의투자 App Secret을 입력하세요"
                        {...registerMock('app_secret')}
                      />
                      {errorsMock.app_secret && (
                        <p className="text-sm text-red-600">
                          {errorsMock.app_secret.message}
                        </p>
                      )}
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="mock_account_number">계좌번호 *</Label>
                      <Input
                        id="mock_account_number"
                        type="text"
                        placeholder="12345678-01"
                        {...registerMock('account_number')}
                      />
                      {errorsMock.account_number && (
                        <p className="text-sm text-red-600">
                          {errorsMock.account_number.message}
                        </p>
                      )}
                      <p className="text-xs text-muted-foreground">
                        형식: 계좌번호-계좌상품코드 (예: 12345678-01)
                      </p>
                    </div>

                    <div className="flex justify-between items-center pt-4 border-t">
                      <div className="text-sm text-muted-foreground">
                        <p>모의투자 API 키는 한국투자증권 홈페이지에서 발급받을 수 있습니다.</p>
                        <a
                          href="https://apiportal.koreainvestment.com/"
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-primary hover:underline"
                        >
                          API 포털 바로가기 →
                        </a>
                      </div>
                      <Button
                        type="submit"
                        disabled={isSaving}
                        className="flex items-center gap-2"
                      >
                        <Save className="h-4 w-4" />
                        {isSaving ? '저장 중...' : '저장'}
                      </Button>
                    </div>
                  </form>
                </TabsContent>

                {/* Real Trading Tab */}
                <TabsContent value="real" className="space-y-4 mt-4">
                  <div className="bg-red-50 border border-red-200 rounded-md p-3 mb-4">
                    <p className="text-sm text-red-800 font-semibold">
                      ⚠️ 주의: 실전투자는 실제 계좌로 거래가 실행됩니다. 신중하게 설정하세요.
                    </p>
                  </div>

                  {hasRealCredentials && (
                    <div className="bg-green-50 border border-green-200 rounded-md p-3 flex items-center justify-between">
                      <p className="text-sm text-green-800">
                        실전투자 API 인증 정보가 등록되어 있습니다.
                      </p>
                      <Button
                        type="button"
                        variant="destructive"
                        size="sm"
                        onClick={handleDeleteRealCredentials}
                        disabled={isSaving}
                      >
                        <Trash2 className="h-4 w-4 mr-1" />
                        삭제
                      </Button>
                    </div>
                  )}

                  <form onSubmit={handleSubmitReal(onSubmitRealKisApi)} className="space-y-4">
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <Label htmlFor="real_app_key">App Key *</Label>
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          onClick={() => setShowRealSecrets(!showRealSecrets)}
                        >
                          {showRealSecrets ? (
                            <EyeOff className="h-4 w-4" />
                          ) : (
                            <Eye className="h-4 w-4" />
                          )}
                        </Button>
                      </div>
                      <Input
                        id="real_app_key"
                        type={showRealSecrets ? 'text' : 'password'}
                        placeholder="실전투자 App Key를 입력하세요"
                        {...registerReal('app_key')}
                      />
                      {errorsReal.app_key && (
                        <p className="text-sm text-red-600">
                          {errorsReal.app_key.message}
                        </p>
                      )}
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="real_app_secret">App Secret *</Label>
                      <Input
                        id="real_app_secret"
                        type={showRealSecrets ? 'text' : 'password'}
                        placeholder="실전투자 App Secret을 입력하세요"
                        {...registerReal('app_secret')}
                      />
                      {errorsReal.app_secret && (
                        <p className="text-sm text-red-600">
                          {errorsReal.app_secret.message}
                        </p>
                      )}
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="real_account_number">계좌번호 *</Label>
                      <Input
                        id="real_account_number"
                        type="text"
                        placeholder="12345678-01"
                        {...registerReal('account_number')}
                      />
                      {errorsReal.account_number && (
                        <p className="text-sm text-red-600">
                          {errorsReal.account_number.message}
                        </p>
                      )}
                      <p className="text-xs text-muted-foreground">
                        형식: 계좌번호-계좌상품코드 (예: 12345678-01)
                      </p>
                    </div>

                    <div className="flex justify-between items-center pt-4 border-t">
                      <div className="text-sm text-muted-foreground">
                        <p>실전투자 API 키는 한국투자증권 홈페이지에서 발급받을 수 있습니다.</p>
                        <a
                          href="https://apiportal.koreainvestment.com/"
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-primary hover:underline"
                        >
                          API 포털 바로가기 →
                        </a>
                      </div>
                      <Button
                        type="submit"
                        disabled={isSaving}
                        className="flex items-center gap-2"
                      >
                        <Save className="h-4 w-4" />
                        {isSaving ? '저장 중...' : '저장'}
                      </Button>
                    </div>
                  </form>
                </TabsContent>
              </Tabs>
            )}
          </CardContent>
        </Card>

        {/* Notification Settings */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Bell className="h-5 w-5" />
              <CardTitle>알림 설정</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">이메일 알림</p>
                  <p className="text-sm text-muted-foreground">
                    중요한 이벤트를 이메일로 받습니다
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => setEmailNotifications(!emailNotifications)}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    emailNotifications ? 'bg-primary' : 'bg-gray-200'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      emailNotifications ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>

              <div className="flex items-center justify-between border-t pt-4">
                <div>
                  <p className="font-medium">거래 체결 알림</p>
                  <p className="text-sm text-muted-foreground">
                    매매 주문이 체결되면 알림을 받습니다
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => setTradeAlerts(!tradeAlerts)}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    tradeAlerts ? 'bg-primary' : 'bg-gray-200'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      tradeAlerts ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>

              <div className="flex items-center justify-between border-t pt-4">
                <div>
                  <p className="font-medium">전략 상태 알림</p>
                  <p className="text-sm text-muted-foreground">
                    전략이 시작/중지되면 알림을 받습니다
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => setStrategyAlerts(!strategyAlerts)}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    strategyAlerts ? 'bg-primary' : 'bg-gray-200'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      strategyAlerts ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>

              <div className="flex items-center justify-between border-t pt-4">
                <div>
                  <p className="font-medium">오류 알림</p>
                  <p className="text-sm text-muted-foreground">
                    시스템 오류 발생 시 즉시 알림을 받습니다
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => setErrorAlerts(!errorAlerts)}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    errorAlerts ? 'bg-primary' : 'bg-gray-200'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      errorAlerts ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>

              <div className="flex justify-end pt-4 border-t">
                <Button
                  onClick={handleSaveNotifications}
                  disabled={isSaving}
                  className="flex items-center gap-2"
                >
                  <Save className="h-4 w-4" />
                  {isSaving ? '저장 중...' : '저장'}
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Risk Management Settings */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Shield className="h-5 w-5" />
              <CardTitle>리스크 관리</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="daily_loss_limit">일일 손실 한도 (원)</Label>
                <Input
                  id="daily_loss_limit"
                  type="number"
                  step="10000"
                  value={dailyLossLimit}
                  onChange={(e) => setDailyLossLimit(Number(e.target.value))}
                />
                <p className="text-xs text-muted-foreground">
                  현재 설정: {formatCurrency(dailyLossLimit)} (하루 최대 손실 금액)
                </p>
              </div>

              <div className="space-y-2">
                <Label htmlFor="max_position_size">
                  최대 포지션 크기 (원)
                </Label>
                <Input
                  id="max_position_size"
                  type="number"
                  step="100000"
                  value={maxPositionSize}
                  onChange={(e) => setMaxPositionSize(Number(e.target.value))}
                />
                <p className="text-xs text-muted-foreground">
                  현재 설정: {formatCurrency(maxPositionSize)} (단일 종목당 최대 투자 금액)
                </p>
              </div>

              <div className="space-y-2">
                <Label htmlFor="max_positions">최대 보유 종목 수</Label>
                <Input
                  id="max_positions"
                  type="number"
                  min="1"
                  max="20"
                  value={maxPositions}
                  onChange={(e) => setMaxPositions(Number(e.target.value))}
                />
                <p className="text-xs text-muted-foreground">
                  현재 설정: {maxPositions}개 (동시에 보유 가능한 종목 수)
                </p>
              </div>

              <div className="flex justify-end pt-4 border-t">
                <Button
                  onClick={handleSaveRiskManagement}
                  disabled={isSaving}
                  className="flex items-center gap-2"
                >
                  <Save className="h-4 w-4" />
                  {isSaving ? '저장 중...' : '저장'}
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* System Info */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <SettingsIcon className="h-5 w-5" />
              <CardTitle>시스템 정보</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex justify-between border-b pb-2">
                <span className="text-sm text-muted-foreground">버전</span>
                <span className="text-sm font-medium">0.1.0 MVP</span>
              </div>
              <div className="flex justify-between border-b pb-2">
                <span className="text-sm text-muted-foreground">
                  마지막 업데이트
                </span>
                <span className="text-sm font-medium">2024-01-21</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">환경</span>
                <span className="text-sm font-medium">개발 (Development)</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  )
}

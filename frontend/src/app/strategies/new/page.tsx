'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { DashboardLayout } from '@/components/layout/DashboardLayout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { ArrowLeft, Save } from 'lucide-react'
import { StrategyType, STRATEGY_TYPE_LABELS } from '@/types/strategy'

const strategySchema = z.object({
  name: z.string().min(1, '전략 이름을 입력해주세요'),
  description: z.string().min(1, '전략 설명을 입력해주세요'),
  type: z.enum(['momentum', 'mean_reversion', 'breakout', 'arbitrage', 'custom']),
  parameters: z.record(z.any()),
})

type StrategyFormData = z.infer<typeof strategySchema>

export default function NewStrategyPage() {
  const router = useRouter()
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [selectedType, setSelectedType] = useState<StrategyType>('momentum')

  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
  } = useForm<StrategyFormData>({
    resolver: zodResolver(strategySchema),
    defaultValues: {
      type: 'momentum',
      parameters: {},
    },
  })

  const onSubmit = async (data: StrategyFormData) => {
    setIsSubmitting(true)
    try {
      // TODO: Call API to create strategy
      console.log('Creating strategy:', data)

      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 1000))

      // Redirect to strategies list
      router.push('/strategies')
    } catch (error) {
      console.error('Failed to create strategy:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleTypeChange = (type: StrategyType) => {
    setSelectedType(type)
    setValue('type', type)
  }

  // Dynamic parameter fields based on strategy type
  const renderParameterFields = () => {
    switch (selectedType) {
      case 'momentum':
        return (
          <>
            <div className="space-y-2">
              <Label htmlFor="period">기간 (일)</Label>
              <Input
                id="period"
                type="number"
                placeholder="20"
                defaultValue="20"
                {...register('parameters.period')}
              />
              <p className="text-xs text-muted-foreground">
                이동평균선 계산 기간
              </p>
            </div>
            <div className="space-y-2">
              <Label htmlFor="threshold">임계값 (%)</Label>
              <Input
                id="threshold"
                type="number"
                step="0.01"
                placeholder="2.0"
                defaultValue="2.0"
                {...register('parameters.threshold')}
              />
              <p className="text-xs text-muted-foreground">
                매수/매도 신호 발생 임계값
              </p>
            </div>
          </>
        )
      case 'mean_reversion':
        return (
          <>
            <div className="space-y-2">
              <Label htmlFor="rsi_period">RSI 기간 (일)</Label>
              <Input
                id="rsi_period"
                type="number"
                placeholder="14"
                defaultValue="14"
                {...register('parameters.rsi_period')}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="oversold">과매도 기준</Label>
              <Input
                id="oversold"
                type="number"
                placeholder="30"
                defaultValue="30"
                {...register('parameters.oversold')}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="overbought">과매수 기준</Label>
              <Input
                id="overbought"
                type="number"
                placeholder="70"
                defaultValue="70"
                {...register('parameters.overbought')}
              />
            </div>
          </>
        )
      case 'breakout':
        return (
          <>
            <div className="space-y-2">
              <Label htmlFor="k">K 계수</Label>
              <Input
                id="k"
                type="number"
                step="0.1"
                placeholder="0.5"
                defaultValue="0.5"
                {...register('parameters.k')}
              />
              <p className="text-xs text-muted-foreground">
                변동성 돌파 계수 (0.3 ~ 0.7 권장)
              </p>
            </div>
            <div className="space-y-2">
              <Label htmlFor="stop_loss">손절 비율 (%)</Label>
              <Input
                id="stop_loss"
                type="number"
                step="0.01"
                placeholder="2.0"
                defaultValue="2.0"
                {...register('parameters.stop_loss')}
              />
            </div>
          </>
        )
      case 'arbitrage':
        return (
          <>
            <div className="space-y-2">
              <Label htmlFor="threshold">스프레드 임계값 (%)</Label>
              <Input
                id="threshold"
                type="number"
                step="0.001"
                placeholder="1.5"
                defaultValue="1.5"
                {...register('parameters.threshold')}
              />
              <p className="text-xs text-muted-foreground">
                차익거래 진입 기준
              </p>
            </div>
          </>
        )
      case 'custom':
        return (
          <div className="space-y-2">
            <Label htmlFor="custom_params">커스텀 파라미터 (JSON)</Label>
            <textarea
              id="custom_params"
              className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
              rows={5}
              placeholder='{"param1": "value1", "param2": 123}'
              {...register('parameters')}
            />
            <p className="text-xs text-muted-foreground">
              JSON 형식으로 입력해주세요
            </p>
          </div>
        )
      default:
        return null
    }
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Page Header */}
        <div className="flex items-center gap-4">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => router.back()}
          >
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">새 전략 생성</h1>
            <p className="text-muted-foreground">
              새로운 트레이딩 전략을 설정하세요
            </p>
          </div>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          {/* Basic Information */}
          <Card>
            <CardHeader>
              <CardTitle>기본 정보</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="name">전략 이름 *</Label>
                <Input
                  id="name"
                  placeholder="예: 모멘텀 전략 A"
                  {...register('name')}
                />
                {errors.name && (
                  <p className="text-sm text-red-600">{errors.name.message}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="description">전략 설명 *</Label>
                <textarea
                  id="description"
                  className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  rows={3}
                  placeholder="전략에 대한 설명을 입력하세요"
                  {...register('description')}
                />
                {errors.description && (
                  <p className="text-sm text-red-600">
                    {errors.description.message}
                  </p>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Strategy Type */}
          <Card>
            <CardHeader>
              <CardTitle>전략 유형 *</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-3 md:grid-cols-3 lg:grid-cols-5">
                {(Object.keys(STRATEGY_TYPE_LABELS) as StrategyType[]).map(
                  (type) => (
                    <button
                      key={type}
                      type="button"
                      onClick={() => handleTypeChange(type)}
                      className={`rounded-lg border-2 p-4 text-center transition-colors ${
                        selectedType === type
                          ? 'border-primary bg-primary/10'
                          : 'border-border hover:border-primary/50'
                      }`}
                    >
                      <p className="font-medium">{STRATEGY_TYPE_LABELS[type]}</p>
                    </button>
                  )
                )}
              </div>
            </CardContent>
          </Card>

          {/* Strategy Parameters */}
          <Card>
            <CardHeader>
              <CardTitle>전략 파라미터</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {renderParameterFields()}
            </CardContent>
          </Card>

          {/* Risk Management */}
          <Card>
            <CardHeader>
              <CardTitle>리스크 관리</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="max_position_size">최대 포지션 크기 (원)</Label>
                <Input
                  id="max_position_size"
                  type="number"
                  placeholder="1000000"
                  defaultValue="1000000"
                  {...register('parameters.max_position_size')}
                />
                <p className="text-xs text-muted-foreground">
                  단일 종목당 최대 투자 금액
                </p>
              </div>

              <div className="space-y-2">
                <Label htmlFor="max_positions">최대 보유 종목 수</Label>
                <Input
                  id="max_positions"
                  type="number"
                  placeholder="5"
                  defaultValue="5"
                  {...register('parameters.max_positions')}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="stop_loss_percent">손절 비율 (%)</Label>
                <Input
                  id="stop_loss_percent"
                  type="number"
                  step="0.1"
                  placeholder="5.0"
                  defaultValue="5.0"
                  {...register('parameters.stop_loss_percent')}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="take_profit_percent">익절 비율 (%)</Label>
                <Input
                  id="take_profit_percent"
                  type="number"
                  step="0.1"
                  placeholder="10.0"
                  defaultValue="10.0"
                  {...register('parameters.take_profit_percent')}
                />
              </div>
            </CardContent>
          </Card>

          {/* Actions */}
          <div className="flex justify-end gap-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => router.back()}
              disabled={isSubmitting}
            >
              취소
            </Button>
            <Button type="submit" disabled={isSubmitting} className="flex items-center gap-2">
              {isSubmitting ? (
                <>처리중...</>
              ) : (
                <>
                  <Save className="h-4 w-4" />
                  전략 생성
                </>
              )}
            </Button>
          </div>
        </form>
      </div>
    </DashboardLayout>
  )
}

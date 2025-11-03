'use client';

import { useMemo } from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ComposedChart,
  Area
} from 'recharts';
import type { ChartDataPoint, TimeInterval } from '@/types/market';

interface MarketChartProps {
  data: ChartDataPoint[];
  interval: TimeInterval;
}

export function MarketChart({ data, interval }: MarketChartProps) {
  // Transform data for chart
  const chartData = useMemo(() => {
    return data.map(point => ({
      ...point,
      time: new Date(point.timestamp).toLocaleString('ko-KR', {
        month: '2-digit',
        day: '2-digit',
        hour: interval !== '1d' ? '2-digit' : undefined,
        minute: interval !== '1d' ? '2-digit' : undefined
      })
    }));
  }, [data, interval]);

  // Calculate price range for Y-axis
  const priceRange = useMemo(() => {
    if (chartData.length === 0) return { min: 0, max: 100 };

    const prices = chartData.flatMap(d => [d.low, d.high]);
    const min = Math.min(...prices);
    const max = Math.max(...prices);
    const padding = (max - min) * 0.1;

    return {
      min: Math.floor(min - padding),
      max: Math.ceil(max + padding)
    };
  }, [chartData]);

  // Custom tooltip
  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-background border rounded-lg shadow-lg p-3 space-y-1">
          <p className="font-semibold text-sm">{new Date(data.timestamp).toLocaleString('ko-KR')}</p>
          <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-xs">
            <span className="text-muted-foreground">시가:</span>
            <span className="font-medium text-right">{data.open.toLocaleString()}원</span>

            <span className="text-muted-foreground">고가:</span>
            <span className="font-medium text-right text-red-600">{data.high.toLocaleString()}원</span>

            <span className="text-muted-foreground">저가:</span>
            <span className="font-medium text-right text-blue-600">{data.low.toLocaleString()}원</span>

            <span className="text-muted-foreground">종가:</span>
            <span className="font-medium text-right">{data.close.toLocaleString()}원</span>

            <span className="text-muted-foreground">거래량:</span>
            <span className="font-medium text-right">{data.volume.toLocaleString()}</span>
          </div>
        </div>
      );
    }
    return null;
  };

  if (chartData.length === 0) {
    return (
      <div className="flex items-center justify-center h-96 text-muted-foreground">
        데이터가 없습니다
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Price Chart (Line + Area) */}
      <div>
        <h3 className="text-sm font-semibold mb-2">가격 차트</h3>
        <ResponsiveContainer width="100%" height={400}>
          <ComposedChart
            data={chartData}
            margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
          >
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis
              dataKey="time"
              tick={{ fontSize: 12 }}
              tickMargin={10}
            />
            <YAxis
              domain={[priceRange.min, priceRange.max]}
              tick={{ fontSize: 12 }}
              tickMargin={10}
              tickFormatter={(value) => `${(value / 1000).toFixed(0)}k`}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend />

            {/* Area for price range */}
            <Area
              type="monotone"
              dataKey="high"
              stroke="none"
              fill="hsl(var(--primary))"
              fillOpacity={0.1}
              name="고가"
            />
            <Area
              type="monotone"
              dataKey="low"
              stroke="none"
              fill="hsl(var(--primary))"
              fillOpacity={0.1}
              name="저가"
            />

            {/* Lines for OHLC */}
            <Line
              type="monotone"
              dataKey="close"
              stroke="hsl(var(--primary))"
              strokeWidth={2}
              dot={false}
              name="종가"
            />
            <Line
              type="monotone"
              dataKey="open"
              stroke="hsl(var(--muted-foreground))"
              strokeWidth={1}
              dot={false}
              name="시가"
              strokeDasharray="5 5"
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>

      {/* Volume Chart */}
      <div>
        <h3 className="text-sm font-semibold mb-2">거래량</h3>
        <ResponsiveContainer width="100%" height={150}>
          <BarChart
            data={chartData}
            margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
          >
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis
              dataKey="time"
              tick={{ fontSize: 12 }}
              tickMargin={10}
            />
            <YAxis
              tick={{ fontSize: 12 }}
              tickMargin={10}
              tickFormatter={(value) => {
                if (value >= 1000000) {
                  return `${(value / 1000000).toFixed(1)}M`;
                } else if (value >= 1000) {
                  return `${(value / 1000).toFixed(0)}K`;
                }
                return value.toString();
              }}
            />
            <Tooltip
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  return (
                    <div className="bg-background border rounded-lg shadow-lg p-2">
                      <p className="text-xs font-medium">
                        거래량: {payload[0].value?.toLocaleString()}
                      </p>
                    </div>
                  );
                }
                return null;
              }}
            />
            <Bar
              dataKey="volume"
              fill="hsl(var(--primary))"
              opacity={0.6}
              name="거래량"
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

'use client';

import { useState } from 'react';
import { Star } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { watchlistApi } from '@/lib/watchlistApi';

interface WatchlistButtonProps {
  symbol: string;
  stockName?: string;
  isInWatchlist: boolean;
  onToggle?: (isInWatchlist: boolean) => void;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'default' | 'ghost' | 'outline';
}

export function WatchlistButton({
  symbol,
  stockName,
  isInWatchlist: initialIsInWatchlist,
  onToggle,
  size = 'sm',
  variant = 'ghost',
}: WatchlistButtonProps) {
  const [isInWatchlist, setIsInWatchlist] = useState(initialIsInWatchlist);
  const [isLoading, setIsLoading] = useState(false);

  const handleToggle = async (e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent row click event

    setIsLoading(true);
    try {
      if (isInWatchlist) {
        // Need to get the watchlist entry ID first
        const watchlist = await watchlistApi.getWatchlist();
        const entry = watchlist.watchlists.find(w => w.symbol === symbol);

        if (entry) {
          await watchlistApi.removeFromWatchlist(entry.id);
          setIsInWatchlist(false);
          onToggle?.(false);
          console.log(`Removed ${stockName || symbol} from watchlist`);
        }
      } else {
        await watchlistApi.addToWatchlist({
          symbol,
          name: 'default',
        });
        setIsInWatchlist(true);
        onToggle?.(true);
        console.log(`Added ${stockName || symbol} to watchlist`);
      }
    } catch (error: any) {
      console.error('Failed to toggle watchlist:', error);
      alert(error.response?.data?.detail || '관심종목 처리 중 오류가 발생했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Button
      variant={variant}
      size={size === 'sm' ? 'sm' : size === 'lg' ? 'lg' : 'default'}
      onClick={handleToggle}
      disabled={isLoading}
      className="group"
    >
      <Star
        className={`h-4 w-4 transition-all ${
          isInWatchlist
            ? 'fill-yellow-400 text-yellow-400'
            : 'text-muted-foreground group-hover:text-yellow-400'
        }`}
      />
    </Button>
  );
}

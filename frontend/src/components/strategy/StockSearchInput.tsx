'use client'

import { useState, useEffect, useRef } from 'react'
import { Search, X, Loader2 } from 'lucide-react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Stock } from '@/types/stock'
import { stockApi } from '@/lib/stockApi'

interface StockSearchInputProps {
  onSelect: (stock: Stock) => void
  selectedStock: Stock | null
  placeholder?: string
}

export function StockSearchInput({
  onSelect,
  selectedStock,
  placeholder = 'Search stock',
}: StockSearchInputProps) {
  const [query, setQuery] = useState('')
  const [searchResults, setSearchResults] = useState<Stock[]>([])
  const [isSearching, setIsSearching] = useState(false)
  const [showDropdown, setShowDropdown] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const dropdownRef = useRef<HTMLDivElement>(null)
  const searchTimeoutRef = useRef<NodeJS.Timeout>()

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowDropdown(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  useEffect(() => {
    if (!query || query.length < 1) {
      setSearchResults([])
      setShowDropdown(false)
      return
    }

    if (searchTimeoutRef.current) clearTimeout(searchTimeoutRef.current)

    searchTimeoutRef.current = setTimeout(async () => {
      setIsSearching(true)
      setError(null)
      try {
        const response = await stockApi.searchStocks({ query, market_type: 'ALL', limit: 10 })
        setSearchResults(response.stocks)
        setShowDropdown(true)
      } catch (err: any) {
        console.error('Search error:', err)
        setError('Search error')
        setSearchResults([])
      } finally {
        setIsSearching(false)
      }
    }, 300)

    return () => {
      if (searchTimeoutRef.current) clearTimeout(searchTimeoutRef.current)
    }
  }, [query])

  const handleSelect = (stock: Stock) => {
    onSelect(stock)
    setQuery('')
    setSearchResults([])
    setShowDropdown(false)
  }

  const handleClear = () => {
    onSelect(null as any)
    setQuery('')
    setSearchResults([])
    setShowDropdown(false)
  }

  if (selectedStock) {
    return (
      <div className="flex items-center gap-2 p-3 border rounded-md bg-muted">
        <div className="flex-1">
          <p className="font-medium">{selectedStock.name}</p>
          <p className="text-sm text-muted-foreground">{selectedStock.symbol} · {selectedStock.market_type}</p>
        </div>
        <Button variant="ghost" size="icon" onClick={handleClear} className="h-8 w-8">
          <X className="h-4 w-4" />
        </Button>
      </div>
    )
  }

  return (
    <div className="relative" ref={dropdownRef}>
      <div className="relative">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <Input type="text" value={query} onChange={(e) => setQuery(e.target.value)} placeholder={placeholder} className="pl-10 pr-10" />
        {isSearching && <Loader2 className="absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 animate-spin text-muted-foreground" />}
      </div>

      {showDropdown && (searchResults.length > 0 || error) && (
        <div className="absolute z-50 mt-1 w-full rounded-md border bg-popover shadow-md">
          {error ? (
            <div className="p-3 text-sm text-red-600">{error}</div>
          ) : (
            <div className="max-h-60 overflow-y-auto">
              {searchResults.map((stock) => (
                <button key={stock.id} onClick={() => handleSelect(stock)} className="flex w-full items-center justify-between px-3 py-2 text-left hover:bg-accent">
                  <div>
                    <p className="font-medium">{stock.name}</p>
                    <p className="text-sm text-muted-foreground">{stock.symbol}</p>
                  </div>
                  <span className="text-xs text-muted-foreground">{stock.market_type}</span>
                </button>
              ))}
            </div>
          )}
        </div>
      )}

      {showDropdown && !isSearching && !error && searchResults.length === 0 && query.length > 0 && (
        <div className="absolute z-50 mt-1 w-full rounded-md border bg-popover p-3 shadow-md">
          <p className="text-sm text-muted-foreground">No results</p>
        </div>
      )}
    </div>
  )
}

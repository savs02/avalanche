
import React, { useState, useEffect } from 'react';
import { DollarSign, TrendingUp, TrendingDown } from 'lucide-react';
import { fetchGlobalData, MarketData } from '../services/cryptoService';
import LoadingSpinner from './LoadingSpinner';

const MarketStats: React.FC = () => {
  const [marketData, setMarketData] = useState<MarketData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const loadMarketData = async () => {
      setLoading(true);
      const data = await fetchGlobalData();
      setMarketData(data);
      setLoading(false);
    };
    
    loadMarketData();
  }, []);

  if (loading) {
    return (
      <div className="glass-card p-5 h-full animate-fade-in">
        <h3 className="text-lg font-medium mb-5">Market Overview</h3>
        <div className="h-32 flex items-center justify-center">
          <LoadingSpinner />
        </div>
      </div>
    );
  }

  if (!marketData) {
    return (
      <div className="glass-card p-5 h-full animate-fade-in">
        <h3 className="text-lg font-medium mb-5">Market Overview</h3>
        <div className="text-center text-muted-foreground">
          Unable to load market data
        </div>
      </div>
    );
  }

  const formatLargeNumber = (value: number) => {
    if (value >= 1000000000000) {
      return `$${(value / 1000000000000).toFixed(2)}T`;
    }
    if (value >= 1000000000) {
      return `$${(value / 1000000000).toFixed(2)}B`;
    }
    if (value >= 1000000) {
      return `$${(value / 1000000).toFixed(2)}M`;
    }
    return `$${value.toFixed(2)}`;
  };

  const isMarketUp = marketData.market_cap_change_percentage_24h_usd >= 0;

  return (
    <div className="glass-card p-5 h-full animate-fade-in">
      <h3 className="text-lg font-medium mb-5">Market Overview</h3>
      
      <div className="space-y-6">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <DollarSign className="h-4 w-4 text-primary" />
            <span className="text-sm text-muted-foreground">Total Market Cap</span>
          </div>
          <p className="text-xl font-medium">{formatLargeNumber(marketData.total_market_cap)}</p>
        </div>
        
        <div>
          <div className="flex items-center gap-2 mb-2">
            {isMarketUp ? (
              <TrendingUp className="h-4 w-4 text-green-500" />
            ) : (
              <TrendingDown className="h-4 w-4 text-red-500" />
            )}
            <span className="text-sm text-muted-foreground">24h Market Change</span>
          </div>
          <p className={`text-xl font-medium ${isMarketUp ? 'text-green-500' : 'text-red-500'}`}>
            {marketData.market_cap_change_percentage_24h_usd.toFixed(2)}%
          </p>
        </div>
        
        <div>
          <div className="flex items-center gap-2 mb-2">
            <DollarSign className="h-4 w-4 text-primary" />
            <span className="text-sm text-muted-foreground">24h Trading Volume</span>
          </div>
          <p className="text-xl font-medium">{formatLargeNumber(marketData.total_volume)}</p>
        </div>
      </div>
    </div>
  );
};

export default MarketStats;

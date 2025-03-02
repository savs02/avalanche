
import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

interface MarketSummaryProps {
  coins: {
    name: string;
    price: number;
    change24h: number;
    isPositive: boolean;
  }[];
}

const MarketSummary: React.FC<MarketSummaryProps> = ({ coins }) => {
  const overallMarketTrend = coins.reduce((sum, coin) => sum + coin.change24h, 0) / coins.length;
  const isMarketUp = overallMarketTrend >= 0;

  return (
    <div className="glass-card p-5 animate-fade-in">
      <h3 className="text-lg font-medium mb-4">Market Summary</h3>
      
      <div className="mb-4">
        <div className="flex items-center gap-2 mb-2">
          {isMarketUp ? (
            <TrendingUp className="h-4 w-4 text-green-500" />
          ) : (
            <TrendingDown className="h-4 w-4 text-red-500" />
          )}
          <span className="text-sm">Overall market trend in the past 24h</span>
        </div>
        <p className={`text-lg font-medium ${isMarketUp ? 'text-green-500' : 'text-red-500'}`}>
          {Math.abs(overallMarketTrend).toFixed(2)}% {isMarketUp ? 'Up' : 'Down'}
        </p>
      </div>
      
      <div className="prose prose-sm">
        <p>
          The crypto market is currently showing {isMarketUp ? 'positive' : 'negative'} momentum, with
          an average change of {Math.abs(overallMarketTrend).toFixed(2)}% in the past 24 hours.
          {overallMarketTrend > 5 ? ' Strong bullish sentiment is evident across major cryptocurrencies.' : 
            overallMarketTrend > 2 ? ' Moderate upward movement indicates growing investor confidence.' :
            overallMarketTrend > 0 ? ' Slight upward momentum suggests cautious market optimism.' :
            overallMarketTrend > -2 ? ' Minor correction reflects normal market volatility.' :
            ' Significant downward pressure may signal a broader market adjustment.'}
        </p>
      </div>
    </div>
  );
};

export default MarketSummary;

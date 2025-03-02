
import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';
import { Coin } from '../services/cryptoService';

interface PriceCardProps {
  coin: Coin;
  index: number;
  isSelected?: boolean;
}

const PriceCard: React.FC<PriceCardProps> = ({ coin, index, isSelected = false }) => {
  const isPositive = coin.price_change_percentage_24h >= 0;
  
  return (
    <div 
      className={`glass-card p-5 hover:shadow-md w-full animate-enter ${
        isSelected ? 'ring-2 ring-primary ring-opacity-70' : ''
      }`}
      style={{ animationDelay: `${index * 75}ms` }}
    >
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
          <img 
            src={coin.image} 
            alt={coin.name} 
            className="w-10 h-10 object-contain"
            loading="lazy" 
          />
          <div className="flex flex-col">
            <h3 className="font-medium">{coin.name}</h3>
            <span className="text-xs text-muted-foreground uppercase">{coin.symbol}</span>
          </div>
        </div>
        <div className="text-xs px-2 py-1 rounded-full bg-secondary">
          Rank #{coin.market_cap_rank}
        </div>
      </div>
      
      <div className="flex items-end justify-between mt-2">
        <div className="flex flex-col">
          <span className="text-2xl font-semibold">${coin.current_price.toLocaleString()}</span>
          <div className={`flex items-center gap-1 ${isPositive ? 'text-green-500' : 'text-red-500'}`}>
            {isPositive ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
            <span className="text-sm font-medium">
              {Math.abs(coin.price_change_percentage_24h).toFixed(2)}%
            </span>
          </div>
        </div>
        <div className="text-xs text-muted-foreground">
          Volume: ${(coin.total_volume / 1000000).toFixed(1)}M
        </div>
      </div>
    </div>
  );
};

export default PriceCard;

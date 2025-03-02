
import React from 'react';
import { ArrowUpCircle, ArrowDownCircle } from 'lucide-react';
import { Trade } from '../services/cryptoService';
import { formatDistanceToNow } from 'date-fns';

interface TradesListProps {
  trades: Trade[];
}

const TradesList: React.FC<TradesListProps> = ({ trades }) => {
  if (!trades.length) {
    return (
      <div className="glass-card p-5 h-full animate-fade-in">
        <h3 className="text-lg font-medium mb-5">Previous Trades</h3>
        <div className="text-center text-muted-foreground py-8">
          No trades found
        </div>
      </div>
    );
  }

  return (
    <div className="glass-card p-5 h-full animate-fade-in">
      <h3 className="text-lg font-medium mb-5">Previous Trades</h3>
      
      <div className="space-y-4 max-h-[400px] overflow-y-auto subtle-scroll pr-2">
        {trades.map((trade) => (
          <div 
            key={trade.id} 
            className="flex items-center justify-between p-3 rounded-lg bg-secondary/10 hover:bg-secondary/20 transition-colors"
          >
            <div className="flex items-center gap-3">
              {trade.type === 'buy' ? (
                <ArrowUpCircle className="h-5 w-5 text-green-500" />
              ) : (
                <ArrowDownCircle className="h-5 w-5 text-red-500" />
              )}
              <div>
                <p className="font-medium capitalize">
                  {trade.type} {trade.coinId}
                </p>
                <p className="text-xs text-muted-foreground">
                  {formatDistanceToNow(new Date(trade.date), { addSuffix: true })}
                </p>
              </div>
            </div>
            
            <div className="text-right">
              <p className="font-medium">${trade.price.toLocaleString()}</p>
              <p className="text-sm">
                {trade.amount.toLocaleString()} {trade.coinId.substring(0, 3).toUpperCase()}
              </p>
              {trade.profit !== undefined && (
                <p className={`text-xs ${trade.profit >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                  {trade.profit >= 0 ? '+' : ''}{trade.profit.toLocaleString()} USD
                </p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TradesList;

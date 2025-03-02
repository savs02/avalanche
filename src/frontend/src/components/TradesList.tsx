import React, { useEffect, useState } from 'react';
import { Trade, fetchUserTrades } from '../services/cryptoService';
import LoadingSpinner from './LoadingSpinner';

const TradesList: React.FC = () => {
  const [trades, setTrades] = useState<Trade[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const loadTrades = async () => {
      setLoading(true);
      const tradesData = await fetchUserTrades();
      setTrades(tradesData);
      setLoading(false);
    };
    
    loadTrades();
  }, []);

  if (loading) {
    return (
      <div className="glass-card p-5 h-full animate-fade-in">
        <h3 className="text-lg font-medium mb-5">Previous Trades</h3>
        <div className="text-center text-muted-foreground py-8">
          <LoadingSpinner />
        </div>
      </div>
    );
  }

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
  
      {Array.isArray(trades) && trades.length === 0 ? (
        <div className="text-center text-muted-foreground py-8">No trades found</div>
      ) : (
        <div className="space-y-4 max-h-[400px] overflow-y-auto subtle-scroll pr-2">
          {trades.map((trade) => (
            <div
              key={trade.id}
              className="flex items-center justify-between p-3 rounded-lg bg-secondary/10 hover:bg-secondary/20 transition-colors"
            >
              <div className="flex items-center gap-3">
                {/* {trade.type === 'buy' ? (
                  <ArrowUpCircle className="h-5 w-5 text-green-500" />
                ) : (
                  <ArrowDownCircle className="h-5 w-5 text-red-500" />
                )} */}
                <div>
                  {trade.type === 'buy' ? (
                    <span className="text-green-500">↑</span>
                  ) : (
                    <span className="text-red-500">↓</span>
                  )}
                </div>

                <div>
                  <p className="font-medium capitalize">
                    {trade.type} {trade.coinId}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {new Date(trade.date).toLocaleDateString()}
                  </p>
                  {/* <p className="text-xs text-muted-foreground">
                    {formatDistanceToNow(new Date(trade.date), { addSuffix: true })}
                  </p> */}
                </div>
              </div>
  
              <div className="text-right">
                <p className="font-medium">
                  ${trade.price ? trade.price.toLocaleString() : 'Unknown'}
                </p>
                <p className="text-sm">
                  {trade.amount ? trade.amount.toLocaleString() : 'Unknown'}{' '}
                  {trade.coinId.substring(0, 3).toUpperCase()}
                </p>
                {trade.profit != null && (
                  <p
                    className={`text-xs ${
                      trade.profit >= 0 ? 'text-green-500' : 'text-red-500'
                    }`}
                  >
                    {trade.profit >= 0 ? '+' : ''}
                    {trade.profit.toLocaleString()} USD
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
// return (
//   <div className="glass-card p-5 h-full overflow-hidden animate-fade-in">
//     <h3 className="text-lg font-medium mb-5">User Trades</h3>

//     {trades.length === 0 ? (
//       <div className="text-center text-muted-foreground py-8">No trades found</div>
//     ) : (
//       <div className="space-y-5 max-h-[500px] overflow-y-auto subtle-scroll pr-2">
//         {trades.map((trade) => (
//           <div key={trade.id} className="flex gap-4 pb-4 animate-scale-in border-b last:border-0">
//             <div>
//               <span className="font-medium">{trade.coinId}</span>
//               <div className="flex items-center gap-2 mt-2 text-xs text-muted-foreground">
//                 <span>{new Date(trade.date).toLocaleDateString()}</span>
//               </div>
//               <div className="text-sm">{trade.type}</div>
//             </div>
//           </div>
//         ))}
//       </div>
//     )}
//   </div>
//   );
// };

export default TradesList;

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

  // if (!trades.length) {
  //   return (
  //     <div className="glass-card p-5 h-full animate-fade-in">
  //       <h3 className="text-lg font-medium mb-5">Previous Trades</h3>
  //       <div className="text-center text-muted-foreground py-8">
  //         No trades found
  //       </div>
  //     </div>
  //   );
  // }


//   return (
//     <div className="glass-card p-5 h-full overflow-hidden animate-fade-in">
//       <h3 className="text-lg font-medium mb-5">Latest News</h3>
      
//       <div className="space-y-5 max-h-[500px] overflow-y-auto subtle-scroll pr-2">
//         {news.map((item, index) => (
//           <div 
//             key={index} 
//             className="flex gap-4 pb-4 animate-scale-in border-b last:border-0"
//             style={{ animationDelay: `${index * 100}ms` }}
//           >
//             <div className="rounded-lg overflow-hidden w-20 h-20 min-w-20 bg-accent">
//               <img 
//                 src={item.urlToImage} 
//                 alt={item.title} 
//                 className="w-full h-full object-cover animate-blur-in"
//                 loading="lazy"
//               />
//             </div>
//             <div>
//               <a 
//                 href={item.url} 
//                 target="_blank" 
//                 rel="noopener noreferrer"
//                 className="font-medium hover:text-primary transition-colors line-clamp-2"
//               >
//                 {item.title}
//               </a>
//               <div className="flex items-center gap-2 mt-2 text-xs text-muted-foreground">
//                 <span>{item.source}</span>
//                 <div className="w-1 h-1 rounded-full bg-muted-foreground" />
//                 <span>{new Date(item.publishedAt).toLocaleDateString()}</span>
//               </div>
//             </div>
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// };

return (
  <div className="glass-card p-5 h-full overflow-hidden animate-fade-in">
    <h3 className="text-lg font-medium mb-5">User Trades</h3>

    {trades.length === 0 ? (
      <div className="text-center text-muted-foreground py-8">No trades found</div>
    ) : (
      <div className="space-y-5 max-h-[500px] overflow-y-auto subtle-scroll pr-2">
        {trades.map((trade) => (
          <div key={trade.id} className="flex gap-4 pb-4 animate-scale-in border-b last:border-0">
            <div>
              <span className="font-medium">{trade.coinId}</span>
              <div className="flex items-center gap-2 mt-2 text-xs text-muted-foreground">
                <span>{new Date(trade.date).toLocaleDateString()}</span>
              </div>
              <div className="text-sm">{trade.type}</div>
            </div>
          </div>
        ))}
      </div>
    )}
  </div>
  );
};

export default TradesList;

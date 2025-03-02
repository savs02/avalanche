
import React, { useState, useEffect } from 'react';
import { fetchTopCoins, fetchUserTrades, Coin, Trade } from '../services/cryptoService';
import Header from '../components/Header';
import PriceCard from '../components/PriceCard';
import TrendChart from '../components/TrendChart';
import NewsSection from '../components/NewsSection';
import LoadingSpinner from '../components/LoadingSpinner';
import TradesList from '../components/TradesList';
import MarketSummary from '../components/MarketSummary';

const Index: React.FC = () => {
  const [coins, setCoins] = useState<Coin[]>([]);
  const [trades, setTrades] = useState<Trade[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedCoin, setSelectedCoin] = useState<string>('bitcoin');

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      const [coinsData, tradesData] = await Promise.all([
        fetchTopCoins(),
        fetchUserTrades()
      ]);
      
      setCoins(coinsData);
      setTrades(tradesData);
      setLoading(false);
    };
    
    loadData();
    
    // Refresh data every 60 seconds
    const interval = setInterval(loadData, 60000);
    return () => clearInterval(interval);
  }, []);

  // Calculate market summary data for the top 4 coins
  const summaryCoins = coins.slice(0, 4).map(coin => ({
    name: coin.name,
    price: coin.current_price,
    change24h: coin.price_change_percentage_24h,
    isPositive: coin.price_change_percentage_24h >= 0
  }));

  return (
    <div className="min-h-screen max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
      <Header />
      
      <main className="space-y-8">
        {loading && coins.length === 0 ? (
          <div className="flex justify-center items-center h-60">
            <LoadingSpinner size="lg" className="opacity-70" />
          </div>
        ) : (
          <>
            {/* Market Summary */}
            {summaryCoins.length > 0 && (
              <MarketSummary coins={summaryCoins} />
            )}
            
            {/* Price Cards */}
            <section>
              <h2 className="text-xl font-medium mb-4 animate-slide-in">Top Cryptocurrencies</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                {coins.slice(0, 4).map((coin, index) => (
                  <button 
                    key={coin.id}
                    className="text-left focus:outline-none focus:ring-2 focus:ring-primary focus:ring-opacity-50 rounded-xl"
                    onClick={() => setSelectedCoin(coin.id)}
                  >
                    <PriceCard coin={coin} index={index} isSelected={coin.id === selectedCoin} />
                  </button>
                ))}
              </div>
            </section>
            
            {/* Chart */}
            <section>
              <TrendChart coinId={selectedCoin} />
            </section>
            
            {/* Trades and News */}
            <section className="grid grid-cols-1 lg:grid-cols-2 gap-5">
              <TradesList trades={trades} />
              <NewsSection />
            </section>
          </>
        )}
      </main>
    </div>
  );
};

export default Index;

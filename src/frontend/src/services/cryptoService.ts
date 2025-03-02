
// Constants
const COINS = ['bitcoin', 'ethereum', 'ripple', 'litecoin', 'cardano', 'polkadot'];
const API_BASE_URL = 'https://api.coingecko.com/api/v3';

// Types
export interface Coin {
  id: string;
  symbol: string;
  name: string;
  image: string;
  current_price: number;
  market_cap: number;
  market_cap_rank: number;
  price_change_percentage_24h: number;
  price_change_percentage_7d_in_currency: number;
  total_volume: number;
  circulating_supply: number;
}

export interface MarketData {
  total_market_cap: number;
  total_volume: number;
  market_cap_percentage: {
    [key: string]: number;
  };
  market_cap_change_percentage_24h_usd: number;
}

export interface ChartData {
  prices: [number, number][];
  market_caps: [number, number][];
  total_volumes: [number, number][];
}

export interface NewsItem {
  title: string;
  url: string;
  source: string;
  publishedAt: string;
  urlToImage: string;
}

export interface Trade {
  id: string;
  coinId: string;
  type: 'buy' | 'sell';
  amount: number;
  price: number;
  date: string;
  profit?: number;
}

// API methods
export const fetchTopCoins = async (): Promise<Coin[]> => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/coins/markets?vs_currency=usd&ids=${COINS.join(',')}&order=market_cap_desc&per_page=10&page=1&sparkline=false&price_change_percentage=24h,7d`
    );
    
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching coins:', error);
    return [];
  }
};

export const fetchGlobalData = async (): Promise<MarketData> => {
  try {
    const response = await fetch(`${API_BASE_URL}/global`);
    
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    
    const data = await response.json();
    // Extract only the needed data and flatten the structure
    return {
      total_market_cap: data.data.total_market_cap.usd,
      total_volume: data.data.total_volume.usd,
      market_cap_percentage: data.data.market_cap_percentage,
      market_cap_change_percentage_24h_usd: data.data.market_cap_change_percentage_24h_usd
    };
  } catch (error) {
    console.error('Error fetching global data:', error);
    return {
      total_market_cap: 0,
      total_volume: 0,
      market_cap_percentage: {},
      market_cap_change_percentage_24h_usd: 0
    };
  }
};

export const fetchCoinChartData = async (coinId: string, days: number = 7): Promise<ChartData> => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/coins/${coinId}/market_chart?vs_currency=usd&days=${days}`
    );
    
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    
    return await response.json();
  } catch (error) {
    console.error(`Error fetching chart data for ${coinId}:`, error);
    return {
      prices: [],
      market_caps: [],
      total_volumes: []
    };
  }
};

// Mock trades data (in a real app, this would come from a backend)
export const fetchUserTrades = async (): Promise<Trade[]> => {
  // Simulating an API call
  return [
    {
      id: '1',
      coinId: 'bitcoin',
      type: 'buy',
      amount: 0.05,
      price: 87500,
      date: '2025-02-25T10:30:00Z',
      profit: 0
    },
    {
      id: '2',
      coinId: 'ethereum',
      type: 'buy',
      amount: 1.2,
      price: 2400,
      date: '2025-02-20T14:15:00Z',
      profit: -212.4
    },
    {
      id: '3',
      coinId: 'bitcoin',
      type: 'sell',
      amount: 0.02,
      price: 92000,
      date: '2025-02-15T09:45:00Z',
      profit: 850
    },
    {
      id: '4',
      coinId: 'ripple',
      type: 'buy',
      amount: 1000,
      price: 2.15,
      date: '2025-02-10T16:20:00Z',
      profit: 50
    }
  ];
};

// Mock news data (since CoinGecko doesn't provide news)
export const fetchCryptoNews = async (): Promise<NewsItem[]> => {
  // In a real app, we would fetch from a news API
  return [
    {
      title: "Bitcoin Surges to New Highs as Institutional Interest Grows",
      url: "#",
      source: "CryptoNews",
      publishedAt: new Date().toISOString(),
      urlToImage: "https://images.unsplash.com/photo-1518546305927-5a555bb7020d?ixlib=rb-1.2.1&auto=format&fit=crop&w=1400&q=80"
    },
    {
      title: "Ethereum 2.0 Upgrade: What You Need to Know",
      url: "#",
      source: "BlockchainInsider",
      publishedAt: new Date().toISOString(),
      urlToImage: "https://images.unsplash.com/photo-1622630998477-20aa696ecb05?ixlib=rb-1.2.1&auto=format&fit=crop&w=1400&q=80"
    },
    {
      title: "Regulators Set New Framework for Cryptocurrency Exchanges",
      url: "#",
      source: "CryptoDaily",
      publishedAt: new Date().toISOString(),
      urlToImage: "https://images.unsplash.com/photo-1621761331887-35f4c9619667?ixlib=rb-1.2.1&auto=format&fit=crop&w=1400&q=80"
    },
    {
      title: "NFT Market Continues to Expand Despite Price Fluctuations",
      url: "#",
      source: "DigitalAssetNews",
      publishedAt: new Date().toISOString(),
      urlToImage: "https://images.unsplash.com/photo-1658237759206-3efe941e4ddc?ixlib=rb-1.2.1&auto=format&fit=crop&w=1400&q=80"
    }
  ];
};

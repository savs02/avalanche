
import React, { useState, useEffect } from 'react';
import { fetchCryptoNews, NewsItem } from '../services/cryptoService';
import LoadingSpinner from './LoadingSpinner';

const NewsSection: React.FC = () => {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const loadNews = async () => {
      setLoading(true);
      const newsData = await fetchCryptoNews();
      setNews(newsData);
      setLoading(false);
    };
    
    loadNews();
  }, []);

  if (loading) {
    return (
      <div className="glass-card p-5 h-full animate-fade-in">
        <h3 className="text-lg font-medium mb-5">Latest News</h3>
        <div className="h-32 flex items-center justify-center">
          <LoadingSpinner />
        </div>
      </div>
    );
  }

  return (
    <div className="glass-card p-5 h-full overflow-hidden animate-fade-in">
      <h3 className="text-lg font-medium mb-5">Latest News</h3>
      
      <div className="space-y-5 max-h-[500px] overflow-y-auto subtle-scroll pr-2">
        {news.map((item, index) => (
          <div 
            key={index} 
            className="flex gap-4 pb-4 animate-scale-in border-b last:border-0"
            style={{ animationDelay: `${index * 100}ms` }}
          >
            <div className="rounded-lg overflow-hidden w-20 h-20 min-w-20 bg-accent">
              <img 
                src={item.urlToImage} 
                alt={item.title} 
                className="w-full h-full object-cover animate-blur-in"
                loading="lazy"
              />
            </div>
            <div>
              <a 
                href={item.url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="font-medium hover:text-primary transition-colors line-clamp-2"
              >
                {item.title}
              </a>
              <div className="flex items-center gap-2 mt-2 text-xs text-muted-foreground">
                <span>{item.source}</span>
                <div className="w-1 h-1 rounded-full bg-muted-foreground" />
                <span>{new Date(item.publishedAt).toLocaleDateString()}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default NewsSection;

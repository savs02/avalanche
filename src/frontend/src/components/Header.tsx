
import React from 'react';
import { ChartBar } from 'lucide-react';

const Header: React.FC = () => {
  return (
    <header className="py-6 animate-fade-in">
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-2">
          <ChartBar className="h-7 w-7 text-primary" />
          <h1 className="text-2xl font-medium">
            <span className="text-gradient font-semibold">Crypto</span>Board
          </h1>
        </div>
        
        <div className="flex items-center gap-1 px-3 py-1.5 glass-card bg-secondary/50">
          <span className="text-sm font-medium">Last updated:</span>
          <span className="text-sm text-muted-foreground">
            {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
        </div>
      </div>
    </header>
  );
};

export default Header;

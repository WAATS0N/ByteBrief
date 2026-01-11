import React from 'react';
import { Zap } from 'lucide-react';

const BreakingNewsBanner = ({ breakingNews, newsIndex }) => (
  <div className="bg-gradient-to-r from-red-600 via-purple-600 to-blue-600 p-3 mt-16">
    <div className="flex items-center space-x-4 max-w-7xl mx-auto px-4">
      <div className="flex items-center space-x-2">
        <Zap className="h-4 w-4 text-white animate-pulse" />
        <span className="text-white font-semibold text-sm">BREAKING NEWS </span>
      </div>
      <div className="flex-1 overflow-hidden">
        <p className="text-white text-sm animate-pulse">
          {breakingNews[newsIndex]}
        </p>
      </div>
    </div>
  </div>
);

export default BreakingNewsBanner;
import React from 'react';
import { getIcon } from '../../utils/iconMap';

const StatsSection = ({ stats }) => (
  <div className="py-20 bg-gradient-to-r from-purple-900/20 to-cyan-900/20">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8">
        {stats.map((stat, index) => {
          const Icon = getIcon(stat.icon);
          return (
            <div key={index} className="text-center">
              <div className="bg-gray-800/50 backdrop-blur-xl p-6 rounded-xl border border-purple-500/20">
                <Icon className="h-8 w-8 text-purple-400 mx-auto mb-3" />
                <div className="text-2xl font-bold text-white mb-1">{stat.value}</div>
                <div className="text-sm text-gray-400">{stat.label}</div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  </div>
);

export default StatsSection;
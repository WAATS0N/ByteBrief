import React from 'react';
import { getIcon } from '../../utils/iconMap';

const HeroSection = ({ heroData, animatedText }) => {
  const { title, animatedText: staticAnimatedText, features } = heroData;

  return (
    <div className="relative min-h-screen overflow-hidden">

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-20">
        <div className="text-center">
          <h1 className="text-5xl md:text-7xl font-bold mb-6">
            <span className="bg-gradient-to-r from-purple-400 via-pink-400 to-cyan-400 bg-clip-text text-transparent">
              {title}
            </span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 mb-8 min-h-[2rem]">
            {animatedText || staticAnimatedText}
            <span className="animate-pulse">|</span>
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            {features.map((feature, index) => {
              const Icon = getIcon(feature.icon);
              const borderColor = index === 0 ? 'border-purple-500/20' : index === 1 ? 'border-cyan-500/20' : 'border-pink-500/20';
              const iconColor = index === 0 ? 'text-purple-400' : index === 1 ? 'text-cyan-400' : 'text-pink-400';

              return (
                <div key={index} className={`bg-gray-800/50 backdrop-blur-xl p-6 rounded-xl border ${borderColor}`}>
                  <Icon className={`h-8 w-8 ${iconColor} mb-3`} />
                  <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
                  <p className="text-gray-400 text-sm">{feature.description}</p>
                </div>
              );
            })}
          </div>
          <button className="bg-gradient-to-r from-purple-500 to-cyan-500 hover:from-purple-600 hover:to-cyan-600 text-white px-8 py-4 rounded-xl font-semibold transition-all duration-300 transform hover:scale-105">
            Start Your Free Digest
          </button>
        </div>
      </div>
    </div>
  );
};

export default HeroSection;
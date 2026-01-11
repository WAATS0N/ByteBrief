import React from 'react';
import { Bot, Zap, Sparkles } from 'lucide-react';

const HeroSection = ({ animatedText }) => (
  <div className="relative min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-black overflow-hidden">
    <div className="absolute inset-0 opacity-20">
      <div className="w-full h-full bg-gradient-to-r from-purple-500/10 to-cyan-500/10"></div>
    </div>
    
    <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-20">
      <div className="text-center">
        <h1 className="text-5xl md:text-7xl font-bold mb-6">
          <span className="bg-gradient-to-r from-purple-400 via-pink-400 to-cyan-400 bg-clip-text text-transparent">
            ByteBrief
          </span>
        </h1>
        <p className="text-xl md:text-2xl text-gray-300 mb-8 min-h-[2rem]">
          {animatedText}
          <span className="animate-pulse">|</span>
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div className="bg-gray-800/50 backdrop-blur-xl p-6 rounded-xl border border-purple-500/20">
            <Bot className="h-8 w-8 text-purple-400 mb-3" />
            <h3 className="text-lg font-semibold text-white mb-2">AI-Powered</h3>
            <p className="text-gray-400 text-sm">Advanced algorithms analyze and summarize news from hundreds of sources</p>
          </div>
          <div className="bg-gray-800/50 backdrop-blur-xl p-6 rounded-xl border border-cyan-500/20">
            <Zap className="h-8 w-8 text-cyan-400 mb-3" />
            <h3 className="text-lg font-semibold text-white mb-2">Real-Time</h3>
            <p className="text-gray-400 text-sm">Get breaking news and updates as they happen, 24/7 monitoring</p>
          </div>
          <div className="bg-gray-800/50 backdrop-blur-xl p-6 rounded-xl border border-pink-500/20">
            <Sparkles className="h-8 w-8 text-pink-400 mb-3" />
            <h3 className="text-lg font-semibold text-white mb-2">Personalized</h3>
            <p className="text-gray-400 text-sm">Customized digests based on your interests and reading preferences</p>
          </div>
        </div>
        <button className="bg-gradient-to-r from-purple-500 to-cyan-500 hover:from-purple-600 hover:to-cyan-600 text-white px-8 py-4 rounded-xl font-semibold transition-all duration-300 transform hover:scale-105">
          Start Your Free Digest
        </button>
      </div>
    </div>
  </div>
);

export default HeroSection;
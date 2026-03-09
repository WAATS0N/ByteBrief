import React from 'react';
import { Brain } from 'lucide-react';

const Footer = () => (
  <footer className="relative z-10 bg-gray-900 py-12 border-t border-gray-800">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
      <div className="flex items-center justify-center space-x-2 mb-4">
        <Brain className="h-6 w-6 text-purple-400" />
        <span className="text-xl font-bold bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">
          ByteBrief
        </span>
      </div>
      <p className="text-gray-400 mb-4">Making news consumption efficient, intelligent, and accessible for everyone.</p>
      <div className="flex justify-center space-x-6 text-sm text-gray-500">
        <a href="#" className="hover:text-purple-400 transition-colors">Privacy Policy</a>
        <a href="#" className="hover:text-purple-400 transition-colors">Terms of Service</a>
        <a href="#" className="hover:text-purple-400 transition-colors">API Documentation</a>
        <a href="#" className="hover:text-purple-400 transition-colors">Contact</a>
      </div>
    </div>
  </footer>
);

export default Footer;
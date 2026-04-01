import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Brain, Lock, Bookmark, Zap, X } from 'lucide-react';

const SmartSignupTrigger = () => {
    const [isVisible, setIsVisible] = useState(false);
    const [hasDismissed, setHasDismissed] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            if (hasDismissed) return;
            // Approx 5-6 scrolls could be ~2000px on desktop, adjust as needed
            if (window.scrollY > 1800 && !isVisible) {
                setIsVisible(true);
            }
        };

        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, [hasDismissed, isVisible]);

    if (!isVisible) return null;

    return (
        <div className="fixed bottom-4 right-4 z-50 md:bottom-8 md:right-8 animate-fade-in-up">
            <div className="bg-gray-900 border border-purple-500/50 rounded-2xl p-6 shadow-2xl max-w-sm relative overflow-hidden group">
                <div className="absolute inset-0 bg-gradient-to-br from-purple-600/10 to-transparent"></div>
                <button 
                    onClick={() => {
                        setIsVisible(false);
                        setHasDismissed(true);
                    }}
                    className="absolute top-3 right-3 text-gray-500 hover:text-white"
                >
                    <X className="w-5 h-5" />
                </button>
                
                <h3 className="text-xl font-bold text-white mb-2 flex items-center">
                    Enjoying ByteBrief? <Zap className="w-5 h-5 text-yellow-400 ml-2" />
                </h3>
                <p className="text-gray-400 text-sm mb-4">
                    Create an account to personalize your feed, save articles, and access AI-driven insights.
                </p>
                
                <ul className="space-y-2 mb-6">
                    <li className="flex items-center text-sm text-gray-300">
                        <Brain className="w-4 h-4 mr-2 text-cyan-400" /> Personalized AI Feed
                    </li>
                    <li className="flex items-center text-sm text-gray-300">
                        <Bookmark className="w-4 h-4 mr-2 text-pink-400" /> Save & Bookmark
                    </li>
                    <li className="flex items-center text-sm text-gray-300">
                        <Lock className="w-4 h-4 mr-2 text-purple-400" /> Unlock Analytics
                    </li>
                </ul>

                <Link
                    to="/login"
                    className="w-full py-3 bg-gradient-to-r from-purple-600 to-cyan-600 hover:from-purple-500 hover:to-cyan-500 text-white rounded-xl font-bold text-sm transition-all duration-300 flex items-center justify-center shadow-lg"
                >
                    Sign Up for Free
                </Link>
            </div>
        </div>
    );
};

export default SmartSignupTrigger;

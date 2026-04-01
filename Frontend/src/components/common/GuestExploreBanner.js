import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, Brain, Bookmark } from 'lucide-react';

const GuestExploreBanner = () => {
    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6">
            <div className="bg-gradient-to-r from-gray-900 to-gray-800 border border-gray-700 hover:border-purple-500/50 transition-colors rounded-2xl p-4 sm:p-6 flex flex-col md:flex-row items-center justify-between">
                <div className="flex items-center mb-4 md:mb-0">
                    <div className="bg-purple-500/20 p-3 rounded-full mr-4">
                        <Sparkles className="w-6 h-6 text-purple-400" />
                    </div>
                    <div>
                        <h3 className="text-white font-bold text-lg">Login to unlock the full potential</h3>
                        <p className="text-gray-400 text-sm flex items-center gap-4 mt-1">
                            <span className="flex items-center"><Brain className="w-3 h-3 mr-1"/> Personalized feed</span>
                            <span className="flex items-center"><Bookmark className="w-3 h-3 mr-1"/> Save articles</span>
                        </p>
                    </div>
                </div>
                <Link to="/login" className="px-6 py-2 bg-purple-600 hover:bg-purple-500 text-white font-medium rounded-full transition-colors whitespace-nowrap text-sm">
                    Log In / Sign Up
                </Link>
            </div>
        </div>
    );
};

export default GuestExploreBanner;

import React from 'react';
import { Link } from 'react-router-dom';
import { Brain, ArrowRight, Zap, Shield, Globe } from 'lucide-react';
import { authService } from '../services/authService';
import BrandSeal from '../components/common/BrandSeal';

const LandingPage = () => {
    const isAuthenticated = authService.isAuthenticated();

    return (
        <div className="min-h-screen bg-black overflow-hidden selection:bg-purple-500/30">
            {/* Background Effects matching the theme */}
            <div className="fixed inset-0 z-0">
                <div className="absolute top-0 -left-1/4 w-full h-full bg-gradient-to-br from-purple-900/10 to-transparent rounded-full blur-[120px]" />
                <div className="absolute bottom-0 -right-1/4 w-full h-full bg-gradient-to-bl from-cyan-900/10 to-transparent rounded-full blur-[120px]" />
                <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_50%,#000_70%,transparent_100%)]" />
            </div>

            {/* Hero Content */}
            <main className="relative z-10 pt-8 pb-32 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto text-center flex flex-col items-center">
                <BrandSeal scale={0.4} className="mb-8" rotating={true} />

                <h1 className="text-5xl md:text-7xl font-extrabold text-white tracking-tight mb-6">
                    Smart News Digest for <br />
                    <span className="bg-gradient-to-r from-purple-400 via-cyan-400 to-blue-500 bg-clip-text text-transparent">
                        Busy Humans
                    </span>
                </h1>

                <p className="mt-6 text-xl text-gray-400 max-w-3xl mx-auto mb-10">
                    ByteBrief automatically collects, analyzes, and summarizes the world's top news in real-time.
                    Get personalized insights without the noise.
                </p>

                <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
                    <Link
                        to={isAuthenticated ? "/home" : "/login"}
                        className="w-full sm:w-auto px-8 py-4 bg-gradient-to-r from-purple-600 to-cyan-600 hover:from-purple-500 hover:to-cyan-500 text-white rounded-full font-bold text-lg transition-all duration-300 transform hover:scale-105 flex items-center justify-center shadow-[0_0_40px_-10px_rgba(168,85,247,0.5)]"
                    >
                        {isAuthenticated ? 'Open Your Digest' : 'Start Your Free Digest'}
                        <ArrowRight className="ml-2 h-5 w-5" />
                    </Link>
                    {!isAuthenticated && (
                        <Link
                            to="/home"
                            className="w-full sm:w-auto px-8 py-4 bg-gray-900/50 border border-gray-700 hover:border-gray-500 text-white rounded-full font-bold text-lg transition-all duration-300 flex items-center justify-center"
                        >
                            Explore as Guest
                        </Link>
                    )}
                </div>

                {/* Features Grid */}
                <div className="mt-32 grid grid-cols-1 md:grid-cols-3 gap-8 text-left">
                    <div className="bg-gray-900/40 p-8 rounded-3xl border border-gray-800 backdrop-blur-sm">
                        <div className="bg-purple-500/20 p-3 rounded-2xl w-fit mb-6">
                            <Zap className="h-6 w-6 text-purple-400" />
                        </div>
                        <h3 className="text-xl font-bold text-white mb-3">Real-Time Scraping</h3>
                        <p className="text-gray-400">Our agents constantly monitor trusted global sources to bring you breaking updates the second they happen.</p>
                    </div>
                    <div className="bg-gray-900/40 p-8 rounded-3xl border border-gray-800 backdrop-blur-sm">
                        <div className="bg-cyan-500/20 p-3 rounded-2xl w-fit mb-6">
                            <Brain className="h-6 w-6 text-cyan-400" />
                        </div>
                        <h3 className="text-xl font-bold text-white mb-3">AI Summarization</h3>
                        <p className="text-gray-400">Long articles are condensed into powerful, 3-minute reads keeping you informed faster than ever.</p>
                    </div>
                    <div className="bg-gray-900/40 p-8 rounded-3xl border border-gray-800 backdrop-blur-sm">
                        <div className="bg-blue-500/20 p-3 rounded-2xl w-fit mb-6">
                            <Shield className="h-6 w-6 text-blue-400" />
                        </div>
                        <h3 className="text-xl font-bold text-white mb-3">Personalized Curation</h3>
                        <p className="text-gray-400">The more you read, the smarter it gets. Your feed adapts to your unique interests and industry.</p>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default LandingPage;

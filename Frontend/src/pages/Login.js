import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Mail, Lock, Eye, EyeOff, Github, ArrowRight, Brain } from 'lucide-react';

const Login = () => {
    const [isLogin, setIsLogin] = useState(true);
    const [showPassword, setShowPassword] = useState(false);
    const navigate = useNavigate();

    const handleAuth = (e) => {
        e.preventDefault();
        navigate('/home'); // Mock logic: simply route to authenticated view
    };

    return (
        <div className="min-h-screen bg-black pt-24 pb-12 px-4 sm:px-6 flex items-center justify-center relative overflow-hidden">
            {/* Background Glow */}
            <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-600/20 rounded-full blur-[120px] pointer-events-none" />
            <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-cyan-600/20 rounded-full blur-[120px] pointer-events-none" />

            <div className="max-w-md w-full relative z-10">
                <div className="text-center mb-8 bg-gray-900/40 p-10 rounded-3xl border border-gray-800 backdrop-blur-xl">
                    <Link to="/" className="inline-flex items-center justify-center space-x-2 mb-8 mx-auto">
                        <div className="bg-gradient-to-r from-purple-500 to-cyan-500 p-2 rounded-xl">
                            <Brain className="h-8 w-8 text-white" />
                        </div>
                        <span className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">
                            ByteBrief
                        </span>
                    </Link>

                    <h2 className="text-3xl font-bold text-white mb-2">
                        {isLogin ? 'Welcome back' : 'Create an account'}
                    </h2>
                    <p className="text-gray-400 mb-8">
                        {isLogin ? 'Enter your details to access your digest.' : 'Sign up to get personalized AI news.'}
                    </p>

                    <form onSubmit={handleAuth} className="space-y-4">
                        {!isLogin && (
                            <div className="relative">
                                <input
                                    type="text"
                                    placeholder="Full Name"
                                    className="w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 transition-colors"
                                    required
                                />
                            </div>
                        )}
                        <div className="relative">
                            <Mail className="absolute left-3 top-3.5 h-5 w-5 text-gray-500" />
                            <input
                                type="email"
                                placeholder="Email address"
                                className="w-full bg-gray-950 border border-gray-800 rounded-xl pl-10 pr-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 transition-colors"
                                required
                            />
                        </div>

                        <div className="relative">
                            <Lock className="absolute left-3 top-3.5 h-5 w-5 text-gray-500" />
                            <input
                                type={showPassword ? 'text' : 'password'}
                                placeholder="Password"
                                className="w-full bg-gray-950 border border-gray-800 rounded-xl pl-10 pr-12 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 transition-colors"
                                required
                            />
                            <button
                                type="button"
                                onClick={() => setShowPassword(!showPassword)}
                                className="absolute right-3 top-3.5 text-gray-500 hover:text-gray-300 transition-colors"
                            >
                                {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                            </button>
                        </div>

                        {isLogin && (
                            <div className="flex justify-end">
                                <button type="button" className="text-sm text-purple-400 hover:text-purple-300">
                                    Forgot password?
                                </button>
                            </div>
                        )}

                        <button
                            type="submit"
                            className="w-full bg-gradient-to-r from-purple-600 to-cyan-600 hover:from-purple-500 hover:to-cyan-500 text-white font-semibold rounded-xl py-3 px-4 flex items-center justify-center transition-all duration-300 transform hover:scale-[1.02]"
                        >
                            {isLogin ? 'Sign In' : 'Create Account'}
                            <ArrowRight className="ml-2 h-5 w-5" />
                        </button>
                    </form>

                    <div className="mt-6 flex items-center justify-center space-x-4">
                        <div className="h-px bg-gray-800 flex-1"></div>
                        <span className="text-gray-500 text-sm">Or continue with</span>
                        <div className="h-px bg-gray-800 flex-1"></div>
                    </div>

                    <div className="mt-6">
                        <button className="w-full bg-gray-950 border border-gray-800 hover:border-gray-600 text-white font-medium rounded-xl py-3 px-4 flex items-center justify-center transition-colors">
                            <svg className="h-5 w-5 mr-2" viewBox="0 0 24 24">
                                <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4" />
                                <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
                                <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05" />
                                <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
                            </svg>
                            Google
                        </button>
                    </div>

                    <p className="mt-8 text-gray-400 text-sm">
                        {isLogin ? "Don't have an account? " : "Already have an account? "}
                        <button
                            onClick={() => setIsLogin(!isLogin)}
                            className="text-cyan-400 hover:text-cyan-300 font-medium transition-colors"
                        >
                            {isLogin ? 'Sign up' : 'Log in'}
                        </button>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Login;

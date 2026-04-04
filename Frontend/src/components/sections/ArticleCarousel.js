import React, { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight, Clock } from 'lucide-react';
import { Link } from 'react-router-dom';
import ArticleImage from '../common/ArticleImage';

const ArticleCarousel = ({ articles }) => {
    const [currentIndex, setCurrentIndex] = useState(0);

    useEffect(() => {
        if (!articles || articles.length === 0) return;
        const timer = setInterval(() => {
            setCurrentIndex((prevIndex) => (prevIndex + 1) % articles.length);
        }, 5000);
        return () => clearInterval(timer);
    }, [articles]);

    if (!articles || articles.length === 0) return null;

    const nextSlide = () => {
        setCurrentIndex((prevIndex) => (prevIndex + 1) % articles.length);
    };

    const prevSlide = () => {
        setCurrentIndex((prevIndex) => (prevIndex - 1 + articles.length) % articles.length);
    };

    return (
        <div className="w-full bg-transparent py-4 sm:py-8">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="relative group w-full h-[300px] sm:h-[400px] md:h-[500px] rounded-2xl overflow-hidden shadow-2xl border border-gray-800">

                    {articles.map((article, index) => (
                        <div
                            key={article.id}
                            className={`absolute inset-0 w-full h-full transition-opacity duration-700 ease-in-out ${index === currentIndex ? 'opacity-100 z-10' : 'opacity-0 z-0'
                                }`}
                        >
                            {/* Background Image using robust ArticleImage */}
                            <div className="absolute inset-0">
                                <ArticleImage src={article.image_url} category={article.category} className="w-full h-full object-cover" />
                            </div>

                            {/* Dark Gradient Overlay */}
                            <div className="absolute inset-0 bg-gradient-to-t from-black/95 via-black/40 to-transparent"></div>

                            {/* Content Overlay */}
                            <div className="absolute bottom-0 left-0 w-full p-6 md:p-12 pb-14 md:pb-16 flex flex-col justify-end">
                                <div className="flex items-center space-x-3 mb-3 md:mb-4">
                                    {article.source && (
                                        <span className="flex items-center justify-center w-6 h-6 md:w-8 md:h-8 text-xs md:text-sm font-extrabold text-white bg-red-600/90 backdrop-blur-sm rounded-full border border-red-500/50 shadow-lg">
                                            {article.source.charAt(0).toUpperCase()}
                                        </span>
                                    )}
                                    <span className="text-xs md:text-sm font-semibold text-gray-200 drop-shadow-md">
                                        {article.source || "ByteBrief"}
                                    </span>
                                    <span className="text-gray-400 text-xs md:text-sm drop-shadow-md flex items-center">
                                        <span className="mx-2">•</span>
                                        {article.readTime || "3m read"}
                                    </span>
                                </div>

                                <Link to={`/article/${article.id}`} state={{ article }}>
                                    <h2 className="text-xl sm:text-3xl md:text-4xl lg:text-5xl font-extrabold text-white leading-tight drop-shadow-2xl max-w-4xl hover:text-cyan-400 transition-colors mb-2">
                                        {article.title}
                                    </h2>
                                </Link>


                            </div>
                        </div>
                    ))}

                    {/* Left/Right Navigation Arrows */}
                    <button
                        onClick={prevSlide}
                        className="absolute left-2 sm:left-4 top-1/2 -translate-y-1/2 z-20 p-2 sm:p-3 rounded-full bg-black/20 hover:bg-black/80 text-white backdrop-blur-md transition-all opacity-0 group-hover:opacity-100 focus:opacity-100 border border-white/10 shadow-xl"
                    >
                        <ChevronLeft className="w-5 h-5 md:w-8 md:h-8" />
                    </button>

                    <button
                        onClick={nextSlide}
                        className="absolute right-2 sm:right-4 top-1/2 -translate-y-1/2 z-20 p-2 sm:p-3 rounded-full bg-black/20 hover:bg-black/80 text-white backdrop-blur-md transition-all opacity-0 group-hover:opacity-100 focus:opacity-100 border border-white/10 shadow-xl"
                    >
                        <ChevronRight className="w-5 h-5 md:w-8 md:h-8" />
                    </button>

                    {/* Dots Indicator */}
                    <div className="absolute bottom-4 left-0 right-0 z-20 flex justify-center space-x-2">
                        {articles.map((_, index) => (
                            <button
                                key={index}
                                onClick={() => setCurrentIndex(index)}
                                className={`transition-all duration-300 rounded-full ${index === currentIndex
                                    ? 'w-6 h-2 bg-white shadow-lg'
                                    : 'w-2 h-2 bg-white/30 hover:bg-white/70'
                                    }`}
                                aria-label={`Go to slide ${index + 1}`}
                            />
                        ))}
                    </div>

                </div>
            </div>
        </div>
    );
};

export default ArticleCarousel;

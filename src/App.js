import React, { useState, useEffect } from 'react';
import Layout from './components/layout/Layout';
import BreakingNewsBanner from './components/sections/BreakingNewsBanner';
import HeroSection from './components/sections/HeroSection';
import CategoriesGrid from './components/sections/CategoriesGrid';
import FeaturedNews from './components/sections/FeaturedNews';
import StatsSection from './components/sections/StatsSection';
import { useRealTime } from './hooks/useRealTime';
import { categories } from './data/categories';
import { breakingNews, featuredArticles } from './data/sampleData';

const ByteBriefWebsite = () => {
  const [currentPage, setCurrentPage] = useState('home');
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [animatedText, setAnimatedText] = useState('');
  const { currentTime, updateIndex } = useRealTime();
  
  const newsIndex = updateIndex % breakingNews.length;

  useEffect(() => {
    const text = "Smart News Digest Generator";
    let index = 0;
    const timer = setInterval(() => {
      if (index <= text.length) {
        setAnimatedText(text.slice(0, index));
        index++;
      } else {
        clearInterval(timer);
      }
    }, 100);
    return () => clearInterval(timer);
  }, []);

  return (
    <Layout
      currentPage={currentPage}
      setCurrentPage={setCurrentPage}
      currentTime={currentTime}
      isMenuOpen={isMenuOpen}
      setIsMenuOpen={setIsMenuOpen}
    >
      <BreakingNewsBanner breakingNews={breakingNews} newsIndex={newsIndex} />
      
      {currentPage === 'home' && (
        <>
          <HeroSection animatedText={animatedText} />
          <CategoriesGrid categories={categories} />
          <FeaturedNews featuredArticles={featuredArticles} />
          <StatsSection />
        </>
      )}

      {currentPage === 'categories' && (
        <div className="pt-32 pb-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h1 className="text-4xl font-bold text-white text-center mb-12">News Categories</h1>
            <CategoriesGrid categories={categories} />
          </div>
        </div>
      )}
    </Layout>
  );
};

export default ByteBriefWebsite;
import React, { useState, useEffect } from 'react';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import BreakingNewsBanner from './components/sections/BreakingNewsBanner';
import HeroSection from './components/sections/HeroSection';
import CategoriesGrid from './components/sections/CategoriesGrid';
import FeaturedNews from './components/sections/FeaturedNews';
import StatsSection from './components/sections/StatsSection';
import { useRealTime } from './hooks/useRealTime';
import { generateDigest, fetchMetadata } from './services/api';
import CategoryPage from './pages/CategoryPage';
import SearchPage from './pages/SearchPage';
import ArticleDigestPage from './pages/ArticleDigestPage';
import Categories from './pages/Categories';
import LandingPage from './pages/LandingPage';
import Login from './pages/Login';
import Analytics from './pages/Analytics';
import AccountSettings from './pages/AccountSettings';
import SavedNews from './pages/SavedNews';
import GuestExploreBanner from './components/common/GuestExploreBanner';
import SmartSignupTrigger from './components/common/SmartSignupTrigger';

const Home = ({ breakingNewsData, heroData, categoriesData, featuredNewsData, statsData, isLoading, animatedText, newsIndex, isAuthenticated }) => {
  const getRecommendedNews = (allNews) => {
    if (!isAuthenticated) return allNews;
    const prefs = JSON.parse(localStorage.getItem("user_category_prefs") || "{}");
    let topCategory = null;
    let max = 0;
    for (const key in prefs) {
      if (prefs[key] > max) {
        max = prefs[key];
        topCategory = key;
      }
    }
    if (!topCategory) return allNews;
    
    const filtered = allNews.filter(news => news.category === topCategory);
    if (filtered.length > 0) {
      // Return filtered news + pad with others to ensure feed isn't too short
      const others = allNews.filter(news => news.category !== topCategory);
      return [...filtered, ...others];
    }
    return allNews;
  };

  const displayNews = getRecommendedNews(featuredNewsData);

  return (
  <>
    {!isAuthenticated && (
      <div className="bg-gradient-to-r from-purple-900/30 to-cyan-900/30 border-b border-gray-800 text-center py-2">
        <span className="text-gray-300 text-sm font-medium flex justify-center items-center">
          🤖 <span className="ml-2 font-bold text-white">Powered by AI summaries</span> <span className="mx-2">—</span> read smarter, not longer.
        </span>
      </div>
    )}
    {breakingNewsData.length > 0 && (
      <BreakingNewsBanner breakingNews={breakingNewsData} newsIndex={newsIndex} />
    )}
    {heroData && <HeroSection heroData={heroData} animatedText={animatedText} />}
    {categoriesData.length > 0 && <CategoriesGrid categories={categoriesData} />}
    
    {!isAuthenticated && <GuestExploreBanner />}
    {isLoading ? (
      <div className="text-center py-20 text-white">Generating your personalized digest...</div>
    ) : (
      <>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-16 mb-4">
          <h2 className="text-2xl font-bold text-white flex items-center">
            {isAuthenticated ? (
              <>
                <span className="bg-purple-500/20 p-2 rounded-lg mr-3">
                  <svg className="w-5 h-5 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                  </svg>
                </span>
                Recommended for You
              </>
            ) : (
              <>
                <span className="bg-orange-500/20 p-2 rounded-lg mr-3">
                  <svg className="w-5 h-5 text-orange-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                  </svg>
                </span>
                Trending Now
              </>
            )}
          </h2>
          <p className="text-gray-400 mt-1">
            {isAuthenticated 
              ? "Based on your recent viewing history and selected categories."
              : "Discover the most viewed and shared news globally right now."}
          </p>
        </div>
        <FeaturedNews featuredArticles={displayNews} />
      </>
    )}
    {statsData.length > 0 && <StatsSection stats={statsData} />}
    {!isAuthenticated && <SmartSignupTrigger />}
  </>
  );
};

const ByteBriefWebsite = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [animatedText, setAnimatedText] = useState('');
  // Initialize with empty arrays/objects to prevent crashes before fetch
  const [breakingNewsData, setBreakingNewsData] = useState([]);
  const [featuredNewsData, setFeaturedNewsData] = useState([]);
  const [categoriesData, setCategoriesData] = useState([]);
  const [statsData, setStatsData] = useState([]);
  const [heroData, setHeroData] = useState(null);
  
  const isAuthenticated = !!localStorage.getItem('access_token');

  const [isLoading, setIsLoading] = useState(false);
  const { currentTime, updateIndex } = useRealTime();

  const newsIndex = breakingNewsData.length > 0 ? updateIndex % breakingNewsData.length : 0;

  useEffect(() => {
    // Initial Animation for text (will be replaced by metadata if available)
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

    // Fetch Metadata
    const loadMetadata = async () => {
      const meta = await fetchMetadata();
      if (meta) {
        setCategoriesData(meta.categories);
        setStatsData(meta.stats);
        setHeroData(meta.hero);
      }
    };
    loadMetadata();

    // Fetch news from all sources on mount
    const fetchNews = async () => {
      setIsLoading(true);
      try {
        // Retrieve token if user is logged in
        const token = localStorage.getItem('access_token');
        let userCategories = [];

        if (token) {
          const { fetchPreferences } = await import('./services/api');
          const prefs = await fetchPreferences(token);
          if (prefs && prefs.categories) {
            userCategories = prefs.categories;
          }
        }

        // Fetch customized topics! (Or all, if none selected)
        const data = await generateDigest([], userCategories);

        if (data.articles && data.articles.length > 0) {
          const mappedFeatured = data.articles.slice(0, 8).map((article, idx) => ({
            id: idx + 100,
            title: article.title,
            summary: article.summary || article.content?.slice(0, 150) + "..." || "No summary available.",
            category: article.category || "Global",
            readTime: "3 min read",
            sentiment: article.sentiment || "neutral",
            importance: 8.5,
            url: article.url,
            source: article.source,
            image_url: article.image_url,
          }));
          setFeaturedNewsData(mappedFeatured);

          const mappedBreaking = data.articles.map((a, idx) => ({
            title: a.title,
            id: idx + 200,
            summary: a.summary || a.content,
            category: a.category || "Breaking",
            source: a.source,
          }));
          setBreakingNewsData(mappedBreaking);
        }
      } catch (error) {
        console.error("Error loading news:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchNews();

    return () => clearInterval(timer);
  }, []);

  const clientId = process.env.REACT_APP_GOOGLE_CLIENT_ID || "434057962464-k3k9o8d3n2b2l8r7m9t6v5w4c1x0z2y1.apps.googleusercontent.com";

  return (
    <GoogleOAuthProvider clientId={clientId}>
      <Router>
        <Layout
          currentTime={currentTime}
          isMenuOpen={isMenuOpen}
          setIsMenuOpen={setIsMenuOpen}
        >
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<Login />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/home" element={
              <Home
                breakingNewsData={breakingNewsData}
                heroData={heroData}
                categoriesData={categoriesData}
                featuredNewsData={featuredNewsData}
                statsData={statsData}
                isLoading={isLoading}
                animatedText={animatedText}
                newsIndex={newsIndex}
                isAuthenticated={isAuthenticated}
              />
            } />
            <Route path="/search" element={<SearchPage />} />
            <Route path="/category/:categoryName" element={<CategoryPage />} />
            <Route path="/categories" element={<Categories />} />
            <Route path="/article/:id" element={<ArticleDigestPage />} />
            <Route path="/saved" element={<SavedNews />} />
            <Route path="/settings" element={<AccountSettings />} />
          </Routes>
        </Layout>
      </Router>
    </GoogleOAuthProvider>
  );
};

export default ByteBriefWebsite;
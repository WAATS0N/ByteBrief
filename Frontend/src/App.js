import React, { useState, useEffect } from 'react';
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
import ArticleDigestPage from './pages/ArticleDigestPage';
import Categories from './pages/Categories';

const Home = ({ breakingNewsData, heroData, categoriesData, featuredNewsData, statsData, isLoading, animatedText, newsIndex }) => (
  <>
    {breakingNewsData.length > 0 && (
      <BreakingNewsBanner breakingNews={breakingNewsData} newsIndex={newsIndex} />
    )}
    {heroData && <HeroSection heroData={heroData} animatedText={animatedText} />}
    {categoriesData.length > 0 && <CategoriesGrid categories={categoriesData} />}
    {isLoading ? (
      <div className="text-center py-20 text-white">Generating your personalized digest...</div>
    ) : (
      <FeaturedNews featuredArticles={featuredNewsData} />
    )}
    {statsData.length > 0 && <StatsSection stats={statsData} />}
  </>
);

const ByteBriefWebsite = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [animatedText, setAnimatedText] = useState('');
  // Initialize with empty arrays/objects to prevent crashes before fetch
  const [breakingNewsData, setBreakingNewsData] = useState([]);
  const [featuredNewsData, setFeaturedNewsData] = useState([]);
  const [categoriesData, setCategoriesData] = useState([]);
  const [statsData, setStatsData] = useState([]);
  const [heroData, setHeroData] = useState(null);

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

    // Fetch news from API on mount
    const fetchNews = async () => {
      setIsLoading(true);
      try {
        const defaultCategories = ['Technology', 'Business', 'Global', 'Health'];
        const data = await generateDigest([], defaultCategories);

        if (data.articles && data.articles.length > 0) {
          const mappedFeatured = data.articles.slice(0, 4).map((article, idx) => ({
            id: idx + 100,
            title: article.title,
            summary: article.summary || article.content?.slice(0, 150) + "..." || "No summary available.",
            category: article.category || "General",
            readTime: "3 min read",
            sentiment: article.sentiment || "neutral",
            importance: 8.5
          }));
          setFeaturedNewsData(mappedFeatured);

          const mappedBreaking = data.articles.map((a, idx) => ({
            title: a.title,
            id: idx + 200, // Distinct ID range
            summary: a.summary || a.content,
            category: a.category || "Breaking",
            source: a.source
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

  return (
    <Router>
      <Layout
        currentTime={currentTime}
        isMenuOpen={isMenuOpen}
        setIsMenuOpen={setIsMenuOpen}
      >
        <Routes>
          <Route path="/" element={
            <Home
              breakingNewsData={breakingNewsData}
              heroData={heroData}
              categoriesData={categoriesData}
              featuredNewsData={featuredNewsData}
              statsData={statsData}
              isLoading={isLoading}
              animatedText={animatedText}
              newsIndex={newsIndex}
            />
          } />
          <Route path="/category/:categoryName" element={<CategoryPage />} />
          <Route path="/categories" element={<Categories />} />
          <Route path="/article/:id" element={<ArticleDigestPage />} />
        </Routes>
      </Layout>
    </Router>
  );
};

export default ByteBriefWebsite;
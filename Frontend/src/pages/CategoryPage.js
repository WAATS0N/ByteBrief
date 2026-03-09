import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { generateDigest } from '../services/api';
import FeaturedNews from '../components/sections/FeaturedNews';

const CategoryPage = () => {
    const { categoryName } = useParams();
    const [articles, setArticles] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchCategoryNews = async () => {
            setIsLoading(true);
            try {
                // Pass the category as both a keyword and a category filter
                const data = await generateDigest([], [categoryName]);

                if (data.articles) {
                    const mappedArticles = data.articles.map((article, idx) => ({
                        id: `cat-${idx}`, // Ensure unique ID for routing
                        title: article.title,
                        summary: article.summary || article.content?.slice(0, 150) + "..." || "No summary available.",
                        category: article.category || categoryName,
                        readTime: "3 min read", // Mocked
                        sentiment: article.sentiment || "neutral",
                        importance: article.importance || 7
                    }));
                    setArticles(mappedArticles);
                }
            } catch (error) {
                console.error("Error loading category news:", error);
            } finally {
                setIsLoading(false);
            }
        };

        if (categoryName) {
            fetchCategoryNews();
        }
    }, [categoryName]);

    return (
        <div className="min-h-screen bg-black pt-8 pb-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto">
                <div className="mb-8">
                    <Link to="/" className="inline-flex items-center text-gray-400 hover:text-white transition-colors mb-4">
                        <ArrowLeft className="h-4 w-4 mr-2" />
                        Back to Home
                    </Link>
                    <h1 className="text-4xl font-bold text-white capitalize">
                        {categoryName} News
                    </h1>
                    <p className="text-gray-400 mt-2">Latest AI-curated updates in {categoryName}</p>
                </div>

                {isLoading ? (
                    <div className="flex justify-center items-center h-64">
                        <div className="text-purple-400 text-xl animate-pulse">Generating digest for {categoryName}...</div>
                    </div>
                ) : (
                    articles.length > 0 ? (
                        <FeaturedNews featuredArticles={articles} />
                    ) : (
                        <div className="text-center text-gray-500 py-12">
                            No articles found for this category. Try again later.
                        </div>
                    )
                )}
            </div>
        </div>
    );
};

export default CategoryPage;

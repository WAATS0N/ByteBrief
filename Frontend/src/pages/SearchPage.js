import React, { useState, useEffect } from 'react';
import { useSearchParams, Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, Search } from 'lucide-react';
import { generateDigest } from '../services/api';
import FeaturedNews from '../components/sections/FeaturedNews';

const SearchPage = () => {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const query = searchParams.get('q') || '';
    const [articles, setArticles] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchSearchResults = async () => {
            if (!query) {
                setArticles([]);
                setIsLoading(false);
                return;
            }
            
            setIsLoading(true);
            try {
                // Pass the query as a keyword
                const data = await generateDigest([query], []);

                if (data.articles) {
                    const mappedArticles = data.articles.map((article, idx) => ({
                        id: `search-${idx}`,
                        title: article.title,
                        summary: article.summary || article.content?.slice(0, 150) + "..." || "No summary available.",
                        category: article.category || "Global",
                        image_url: article.image_url || null,   // ← pass image through
                        url: article.url,
                        readTime: "3 min read",
                        sentiment: article.sentiment || "neutral",
                        importance: article.importance || 7
                    }));
                    setArticles(mappedArticles);
                }
            } catch (error) {
                console.error("Error loading search results:", error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchSearchResults();
    }, [query]);

    return (
        <div className="min-h-screen bg-black pt-8 pb-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto">
                <div className="mb-8">
                    <button
                        onClick={() => {
                            if (window.history.state && window.history.state.idx > 0) {
                                navigate(-1);
                            } else {
                                navigate('/home');
                            }
                        }}
                        className="inline-flex items-center text-gray-400 hover:text-white transition-colors mb-4 group"
                    >
                        <ArrowLeft className="h-4 w-4 mr-2 group-hover:-translate-x-1 transition-transform" />
                        Back
                    </button>
                    <h1 className="text-4xl font-bold text-white flex items-center">
                        <Search className="h-8 w-8 mr-3 text-cyan-400" />
                        Search Results
                    </h1>
                    <p className="text-gray-400 mt-2">
                        {query ? `Showing results for "${query}"` : "Enter a search term in the navigation bar."}
                    </p>
                </div>

                {isLoading ? (
                    <div className="flex justify-center items-center h-64">
                        <div className="text-cyan-400 text-xl animate-pulse">Searching for "{query}"...</div>
                    </div>
                ) : (
                    query ? (
                        articles.length > 0 ? (
                            <FeaturedNews featuredArticles={articles} />
                        ) : (
                            <div className="text-center text-gray-500 py-12">
                                No articles found for "{query}". Try a different keyword.
                            </div>
                        )
                    ) : null
                )}
            </div>
        </div>
    );
};

export default SearchPage;

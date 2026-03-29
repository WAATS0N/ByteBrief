import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, Bookmark } from 'lucide-react';
import { fetchBookmarks } from '../services/api';
import FeaturedNews from '../components/sections/FeaturedNews';

const SavedNews = () => {
    const [articles, setArticles] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const loadBookmarks = async () => {
            setIsLoading(true);
            try {
                const token = localStorage.getItem('access_token');
                if (token) {
                    const res = await fetchBookmarks(token);
                    if (res.status === 'success' && res.bookmarks) {
                        // Reshape bookmark structure to match FeaturedNews expectations
                        const mappedArticles = res.bookmarks.map((b) => ({
                            id: b.id,
                            title: b.title,
                            summary: b.content?.slice(0, 150) + "..." || "No summary available.",
                            category: b.category || "Saved",
                            readTime: "3 min read",
                            url: b.url,
                            source: b.source,
                            image_url: b.image_url,
                            sentiment: "neutral",
                            importance: 8
                        }));
                        setArticles(mappedArticles);
                    }
                }
            } catch (error) {
                console.error("Error loading bookmarks:", error);
            } finally {
                setIsLoading(false);
            }
        };

        loadBookmarks();
    }, []);

    return (
        <div className="min-h-screen bg-black pt-8 pb-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto">
                <div className="mb-8">
                    <Link to="/" className="inline-flex items-center text-gray-400 hover:text-white transition-colors mb-4">
                        <ArrowLeft className="h-4 w-4 mr-2" />
                        Back to Home
                    </Link>
                    <h1 className="text-4xl font-bold text-white flex items-center">
                        <Bookmark className="h-8 w-8 mr-3 text-purple-400 fill-current" />
                        Saved Articles
                    </h1>
                    <p className="text-gray-400 mt-2">Your personal reading list.</p>
                </div>

                {isLoading ? (
                    <div className="flex justify-center items-center h-64">
                        <div className="text-purple-400 text-xl animate-pulse">Loading saved articles...</div>
                    </div>
                ) : (
                    articles.length > 0 ? (
                        <FeaturedNews featuredArticles={articles} />
                    ) : (
                        <div className="text-center py-20 bg-gray-900/30 rounded-3xl border border-dashed border-gray-800">
                            <Bookmark className="h-12 w-12 text-gray-500 mx-auto mb-4" />
                            <p className="text-white text-xl font-medium mb-2">No saved articles yet</p>
                            <p className="text-gray-500">Click the bookmark icon on any article to read it later.</p>
                        </div>
                    )
                )}
            </div>
        </div>
    );
};

export default SavedNews;

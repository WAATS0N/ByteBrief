import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { fetchMetadata } from '../services/api';
import { getIcon } from '../utils/iconMap';

const Categories = () => {
    const [categories, setCategories] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const loadCategories = async () => {
            setIsLoading(true);
            try {
                const meta = await fetchMetadata();
                if (meta && meta.categories) {
                    setCategories(meta.categories);
                }
            } catch (error) {
                console.error("Error fetching categories:", error);
            } finally {
                setIsLoading(false);
            }
        };
        loadCategories();
    }, []);

    return (
        <div className="min-h-screen bg-black pt-24 pb-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto">
                <div className="text-center mb-16">
                    <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent mb-4">
                        News Categories
                    </h1>
                    <p className="text-gray-400 text-lg max-w-2xl mx-auto">
                        Explore personalized news digests across various sectors. Each category is powered by AI to bring you the most relevant updates.
                    </p>
                </div>

                {isLoading ? (
                    <div className="flex justify-center items-center h-64">
                        <div className="w-12 h-12 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
                        {categories.map((category) => {
                            const Icon = getIcon(category.icon);
                            return (
                                <Link
                                    key={category.name}
                                    to={`/category/${category.name.toLowerCase()}`}
                                    className="group relative bg-gray-900/50 border border-gray-800 rounded-2xl p-8 hover:border-purple-500/50 transition-all duration-300 hover:transform hover:-translate-y-2 overflow-hidden"
                                >
                                    <div className={`absolute inset-0 bg-gradient-to-br ${category.color} opacity-0 group-hover:opacity-10 transition-opacity duration-300`} />

                                    <div className="relative z-10">
                                        <div className="bg-gray-800 rounded-xl p-4 w-16 h-16 flex items-center justify-center mb-6 group-hover:bg-purple-500/20 transition-colors">
                                            <Icon className="h-8 w-8 text-gray-400 group-hover:text-purple-400 transition-colors" />
                                        </div>

                                        <h3 className="text-2xl font-bold text-white mb-2 group-hover:text-purple-400 transition-colors">
                                            {category.name}
                                        </h3>

                                        <div className="flex items-center text-gray-400 text-sm">
                                            <span className="font-medium text-purple-400/80 mr-2">{category.count}</span>
                                            updates available
                                        </div>

                                        <div className="mt-8 flex items-center text-purple-400 font-semibold opacity-0 group-hover:opacity-100 transition-opacity">
                                            View Digest
                                            <svg className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                                            </svg>
                                        </div>
                                    </div>
                                </Link>
                            );
                        })}
                    </div>
                )}

                {!isLoading && categories.length === 0 && (
                    <div className="text-center py-20 bg-gray-900/30 rounded-3xl border border-dashed border-gray-800">
                        <p className="text-gray-500 text-xl">No categories found at the moment.</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Categories;

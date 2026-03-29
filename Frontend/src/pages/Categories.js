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
        <div className="min-h-screen bg-black pt-8 pb-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto">
                <div className="text-center mb-16">
                    <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent mb-4 pb-2">
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
                    <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 sm:gap-8">
                        {categories.map((category) => {
                            const Icon = getIcon(category.icon);
                            return (
                                <Link
                                    key={category.name}
                                    to={`/category/${category.name.toLowerCase()}`}
                                    className="group relative bg-gray-900/50 border border-gray-800 rounded-2xl p-4 sm:p-8 hover:border-purple-500/50 transition-all duration-300 hover:transform hover:-translate-y-2 overflow-hidden flex flex-col justify-between"
                                >
                                    <div className={`absolute inset-0 bg-gradient-to-br ${category.color} opacity-0 group-hover:opacity-10 transition-opacity duration-300`} />

                                    <div className="relative z-10">
                                        <div className="bg-gray-800 rounded-xl p-3 sm:p-4 w-12 h-12 sm:w-16 sm:h-16 flex items-center justify-center mb-4 sm:mb-6 group-hover:bg-purple-500/20 transition-colors">
                                            <Icon className="h-6 w-6 sm:h-8 sm:w-8 text-gray-400 group-hover:text-purple-400 transition-colors" />
                                        </div>

                                        <h3 className="text-lg sm:text-2xl font-bold text-white mb-2 group-hover:text-purple-400 transition-colors">
                                            {category.name}
                                        </h3>

                                        <div className="flex flex-col sm:flex-row sm:items-center text-gray-400 text-xs sm:text-sm">
                                            <span className="font-medium text-purple-400/80 sm:mr-2">{category.count} updates available</span>
                                        </div>

                                        <div className="mt-4 sm:mt-8 flex items-center text-[10px] sm:text-sm text-purple-400 font-semibold opacity-100 sm:opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                                            View Digest
                                            <svg className="w-3 h-3 sm:w-4 sm:h-4 ml-1 sm:ml-2 sm:group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
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

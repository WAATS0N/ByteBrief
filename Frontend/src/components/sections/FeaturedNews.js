import React from 'react';
import { Clock, ArrowRight, Share2, Bookmark } from 'lucide-react';
import { Link } from 'react-router-dom';

const FeaturedNews = ({ featuredArticles }) => {
  return (
    <div className="py-20 bg-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-bold text-white mb-12 flex items-center">
          <span className="bg-purple-500 w-2 h-8 mr-4 rounded-full"></span>
          Featured Digest
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-8">
          {featuredArticles.map((article) => {
            const importanceColor = article.importance > 8 ? 'text-red-400' : 'text-purple-400';

            return (
              <div key={article.id} className="group relative bg-gray-900/50 rounded-2xl border border-gray-800 overflow-hidden hover:border-purple-500/50 transition-all duration-300">
                <div className="absolute top-0 left-0 w-1 h-full bg-gradient-to-b from-purple-500 to-cyan-500 opacity-0 group-hover:opacity-100 transition-opacity"></div>

                <div className="p-8">
                  <div className="flex items-center justify-between mb-6">
                    <span className="px-3 py-1 rounded-full text-xs font-semibold bg-gray-800 text-gray-300 border border-gray-700">
                      {article.category}
                    </span>
                    <div className="flex items-center space-x-3">
                      <span className={`text-xs font-bold ${importanceColor}`}>
                        {article.sentiment === 'positive' ? 'High Impact' : 'Trending'}
                      </span>
                      <Bookmark className="h-4 w-4 text-gray-500 hover:text-white cursor-pointer transition-colors" />
                    </div>
                  </div>

                  <h3 className="text-2xl font-bold text-white mb-4 leading-tight group-hover:text-purple-400 transition-colors">
                    <Link to={`/article/${article.id}`} state={{ article }}>
                      {article.title}
                    </Link>
                  </h3>

                  <p className="text-gray-400 mb-6 line-clamp-3">
                    {article.summary}
                  </p>

                  <div className="flex items-center justify-between pt-6 border-t border-gray-800">
                    <div className="flex items-center text-sm text-gray-500">
                      <Clock className="h-4 w-4 mr-2" />
                      {article.readTime}
                    </div>

                    <div className="flex items-center space-x-4">
                      <button className="text-gray-500 hover:text-white transition-colors">
                        <Share2 className="h-4 w-4" />
                      </button>
                      <Link
                        to={`/article/${article.id}`}
                        state={{ article }}
                        className="flex items-center text-purple-400 font-semibold group-hover:translate-x-1 transition-transform"
                      >
                        Read Digest <ArrowRight className="h-4 w-4 ml-2" />
                      </Link>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default FeaturedNews;
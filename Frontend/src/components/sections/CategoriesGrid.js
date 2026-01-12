import React from 'react';
import { Link } from 'react-router-dom';
import { getIcon } from '../../utils/iconMap';

const CategoriesGrid = ({ categories }) => {
  return (
    <div className="py-20 bg-black/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-bold text-white mb-12 text-center">Explore Categories</h2>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-6">
          {categories.map((category) => {
            const Icon = getIcon(category.icon);
            return (
              <Link
                key={category.name}
                to={`/category/${category.name.toLowerCase()}`}
                className={`block p-6 rounded-xl bg-gray-800/50 border border-gray-700 hover:border-purple-500 transition-all duration-300 hover:scale-105 group relative overflow-hidden text-center`}
              >
                <div className={`absolute inset-0 bg-gradient-to-br ${category.color} opacity-0 group-hover:opacity-10 transition-opacity duration-300`} />
                <Icon className="h-8 w-8 text-gray-400 group-hover:text-purple-400 mb-3 mx-auto transition-colors" />
                <div className="text-white font-semibold text-lg">{category.name}</div>
                <div className="text-gray-500 text-sm">{category.count} updates</div>
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default CategoriesGrid;
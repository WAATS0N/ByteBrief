import React from 'react';
import { ChevronRight } from 'lucide-react';

const CategoriesGrid = ({ categories }) => (
  <div className="py-20 bg-gray-900">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h2 className="text-3xl font-bold text-white text-center mb-12">
        News Categories
      </h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
        {categories.map((category, index) => (
          <div
            key={category.name}
            className="group relative bg-gray-800 rounded-xl p-6 hover:bg-gray-700 transition-all duration-300 cursor-pointer transform hover:scale-105"
          >
            <div className={`bg-gradient-to-r ${category.color} p-3 rounded-lg mb-4 w-fit`}>
              <category.icon className="h-6 w-6 text-white" />
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">{category.name}</h3>
            <p className="text-gray-400 text-sm">{category.count} articles today</p>
            <ChevronRight className="absolute top-6 right-6 h-5 w-5 text-gray-600 group-hover:text-purple-400 transition-colors" />
          </div>
        ))}
      </div>
    </div>
  </div>
);

export default CategoriesGrid;
import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { ArrowLeft, Clock, Share2, BookOpen, CheckCircle, Brain } from 'lucide-react';

const ArticleDigestPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [digestPoints, setDigestPoints] = useState([]);
  
  // Get article from navigation state
  const article = location.state?.article;

  useEffect(() => {
    if (!article) {
      // If accessed directly without state, redirect to home
      // In a real app, we would fetch by ID here
      navigate('/');
      return;
    }

    // Heuristic: Transform summary/content into point-by-point digest
    const textToProcess = article.summary || article.content || "";
    
    // Split by period, question mark, or exclamation mark followed by a space
    // Filter out short segments to keep meaningful points
    const points = textToProcess
      .split(/(?<=[.?!])\s+/)
      .filter(p => p.length > 20)
      .map(p => p.trim());

    if (points.length === 0) {
        setDigestPoints([textToProcess]);
    } else {
        setDigestPoints(points);
    }
    
  }, [article, navigate]);

  if (!article) return null;

  return (
    <div className="min-h-screen bg-black pt-24 pb-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <Link 
          to="/" 
          className="inline-flex items-center text-gray-400 hover:text-white transition-colors mb-8 group"
        >
          <ArrowLeft className="h-4 w-4 mr-2 group-hover:-translate-x-1 transition-transform" />
          Back to Digest
        </Link>
        
        {/* Transformed Container */}
        <div className="relative bg-gray-900/50 rounded-2xl border border-purple-500/20 overflow-hidden shadow-2xl backdrop-blur-sm">
           {/* Decorative Top Gradient */}
          <div className="absolute top-0 left-0 right-0 h-2 bg-gradient-to-r from-purple-500 via-cyan-500 to-purple-500" />
          
          <div className="p-8 md:p-12">
            {/* Header */}
            <div className="mb-8">
              <div className="flex items-center space-x-3 mb-4">
                <span className="px-3 py-1 rounded-full text-xs font-semibold bg-purple-500/10 text-purple-400 border border-purple-500/20">
                  {article.category || "News"}
                </span>
                <span className="flex items-center text-xs text-gray-400">
                  <Clock className="h-3 w-3 mr-1" />
                  {article.readTime || "3 min read"}
                </span>
                 <span className="flex items-center text-xs text-gray-400">
                  <Brain className="h-3 w-3 mr-1" />
                  AI Summarized
                </span>
              </div>
              
              <h1 className="text-3xl md:text-5xl font-bold text-white mb-6 leading-tight">
                {article.title}
              </h1>
              
              {/* Meta actions */}
              <div className="flex items-center justify-between border-b border-gray-800 pb-8 mb-8">
                <div className="text-gray-400 text-sm">
                   Source: <span className="text-white font-medium">{article.source || "ByteBrief Intelligence"}</span>
                </div>
                <div className="flex space-x-4">
                   <button className="p-2 rounded-full hover:bg-gray-800 text-gray-400 hover:text-white transition-colors" title="Read Full">
                      <BookOpen className="h-5 w-5" />
                   </button>
                   <button className="p-2 rounded-full hover:bg-gray-800 text-gray-400 hover:text-white transition-colors" title="Share">
                      <Share2 className="h-5 w-5" />
                   </button>
                </div>
              </div>
            </div>

            {/* Digest Content */}
            <div className="space-y-6">
                <h2 className="text-xl font-semibold text-cyan-400 flex items-center">
                    <CheckCircle className="h-5 w-5 mr-2" />
                    Key Takeaways
                </h2>
                
                <div className="space-y-4">
                    {digestPoints.map((point, index) => (
                        <div key={index} className="flex items-start group">
                            <span className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-800 text-gray-400 flex items-center justify-center text-sm font-mono mr-4 group-hover:bg-purple-500/20 group-hover:text-purple-400 transition-colors">
                                {index + 1}
                            </span>
                            <p className="text-gray-300 text-lg leading-relaxed pt-1 group-hover:text-white transition-colors">
                                {point}
                            </p>
                        </div>
                    ))}
                </div>
            </div>
            
            <div className="mt-12 pt-8 border-t border-gray-800">
                <p className="text-sm text-center text-gray-500 italic">
                    This digest was generated by ByteBrief AI from verified sources.
                </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ArticleDigestPage;

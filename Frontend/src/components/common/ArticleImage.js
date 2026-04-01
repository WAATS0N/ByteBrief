import React, { useState } from 'react';
import { Camera } from 'lucide-react';

const CATEGORY_IMAGES = {
    'Tech': 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&q=80',
    'Technology': 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&q=80',
    'AI & Future Tech': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&q=80',
    'Business': 'https://images.unsplash.com/photo-1444653614773-995cb1ef9efa?w=800&q=80',
    'Startups & Innovation': 'https://images.unsplash.com/photo-1556761175-4b46a572b786?w=800&q=80',
    'Global': 'https://images.unsplash.com/photo-1526470608268-f674ce90ebd4?w=800&q=80',
    'Global Affairs': 'https://images.unsplash.com/photo-1526470608268-f674ce90ebd4?w=800&q=80',
    'Health': 'https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=800&q=80',
    'Sports': 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800&q=80',
    'Politics': 'https://images.unsplash.com/photo-1541872703-74c5e44368f9?w=800&q=80',
    'Finance': 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&q=80',
    'Travel': 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&q=80',
    'Gaming': 'https://images.unsplash.com/photo-1552820728-8b83bb6b773f?w=800&q=80',
    'Entertainment': 'https://images.unsplash.com/photo-1603190287605-e6ade32fa852?w=800&q=80',
    'Climate & Environment': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=80',
    'Cybersecurity': 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&q=80',
    'Space & Research': 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&q=80',
    'Psychology & Mind': 'https://images.unsplash.com/photo-1559757175-5700dde675bc?w=800&q=80',
    'Digital Life': 'https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=800&q=80',
    'Science': 'https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=800&q=80',
    'India News': 'https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=800&q=80',
    'Breaking': 'https://images.unsplash.com/photo-1585829365295-ab7cd400c167?w=800&q=80',
};

const ArticleImage = ({ src, category, alt, className }) => {
    const [imgError, setImgError] = useState(false);
    
    // Fallback based on specific mapped unsplash high-res photos
    const fallbackImage = CATEGORY_IMAGES[category] || CATEGORY_IMAGES['Breaking'];
    
    // Combine frontend checks to ensure real robustness
    const activeSrc = (!src || imgError) ? fallbackImage : src;
    const isFallback = !src || imgError;

    return (
        <div className="relative w-full h-full">
            <img
                src={activeSrc}
                alt={alt || "News feature"}
                className={`${className || ''} ${isFallback ? 'opacity-90 grayscale-[20%]' : ''}`}
                loading="lazy"
                onError={(e) => {
                    // Prevent infinite loops if fallback itself fails (though unsplash is stable)
                    if (!imgError) {
                        setImgError(true);
                    } else {
                        // Ultimate emergency fallback
                        e.target.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='800' height='600' viewBox='0 0 800 600'%3E%3Crect width='100%25' height='100%25' fill='%231f2937' /%3E%3Ctext x='50%25' y='50%25' font-family='sans-serif' font-size='24' fill='%239ca3af' text-anchor='middle' dominant-baseline='middle'%3ENews Article Preview%3C/text%3E%3C/svg%3E";
                    }
                }}
            />
            
            {/* 🧠 UX Marker for auto-generated / fallback photos */}
            {isFallback && (
                <div className="absolute top-2 right-2 sm:bottom-2 sm:top-auto sm:right-2 bg-black/70 backdrop-blur-md px-2 py-1 rounded text-[10px] sm:text-xs text-gray-300 font-medium border border-gray-600/50 flex items-center z-10 pointer-events-none shadow-lg">
                    <Camera className="w-3 h-3 mr-1.5 opacity-80 text-purple-400" />
                    Illustrative Image
                </div>
            )}
        </div>
    );
};

export default ArticleImage;

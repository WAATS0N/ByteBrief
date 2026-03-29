import React from 'react';
import { Home, LayoutGrid, Bookmark, User } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';
import { authService } from '../../services/authService';

const BottomNavigation = () => {
  const location = useLocation();
  const isAuthenticated = authService.isAuthenticated();

  // Highlight active tab
  const isActive = (path) => {
    if (path === '/' && (location.pathname === '/' || location.pathname === '/home')) return true;
    return location.pathname.startsWith(path) && path !== '/';
  };

  const navItems = [
    { label: 'Home', icon: Home, path: isAuthenticated ? '/home' : '/' },
    { label: 'Categories', icon: LayoutGrid, path: '/categories' },
    { label: 'Saved', icon: Bookmark, path: isAuthenticated ? '/saved' : '/login' },
    { label: 'Profile', icon: User, path: isAuthenticated ? '/settings' : '/login' }
  ];

  return (
    <div className="md:hidden fixed bottom-0 left-0 right-0 bg-black/95 backdrop-blur-md border-t border-gray-800 z-50 pb-safe">
      <div className="flex justify-around items-center h-16 px-2">
        {navItems.map((item) => {
          const Icon = item.icon;
          const active = isActive(item.path);
          return (
            <Link 
              key={item.label} 
              to={item.path} 
              className={`flex flex-col items-center justify-center w-full h-full space-y-1 transition-colors ${active ? 'text-purple-400' : 'text-gray-500 hover:text-gray-300'}`}
            >
              <Icon className="h-6 w-6" strokeWidth={active ? 2.5 : 2} fill={active ? "currentColor" : "none"} />
              <span className="text-[10px] sm:text-xs font-medium">{item.label}</span>
            </Link>
          );
        })}
      </div>
    </div>
  );
};

export default BottomNavigation;

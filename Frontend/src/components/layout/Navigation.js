import React, { useState, useRef, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Menu, X, Brain, Settings, LogOut, ChevronDown, User, Search, Bookmark } from 'lucide-react';
import { authService } from '../../services/authService';
import BrandSeal from '../common/BrandSeal';

const Navigation = ({ isMenuOpen, setIsMenuOpen }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const isAuthenticated = authService.isAuthenticated();
  const user = authService.getCurrentUser();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery.trim())}`);
      setSearchQuery('');
      setIsMenuOpen(false);
    }
  };

  const handleLogout = () => {
    authService.logout();
    setDropdownOpen(false);
    navigate('/');
  };

  // Close dropdown on outside click
  useEffect(() => {
    const handleClick = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  const isLandingOrLogin = location.pathname === '/' || location.pathname === '/login';

  if (location.pathname === '/') {
    return (
      <nav className="w-full relative z-50 bg-black py-8 border-b border-white/30 flex justify-center items-center backdrop-blur-sm">
        <Link to="/" className="flex flex-col items-center justify-center transform transition-opacity hover:opacity-80">
          <span className="font-serif text-[32px] sm:text-4xl font-normal tracking-[0.15em] text-white" style={{ fontFamily: "'Playfair Display', serif" }}>
            BYTE BRIEF
          </span>
          <div className="flex items-center justify-center space-x-2 my-1.5 opacity-40">
            <div className="h-px w-8 bg-gray-400"></div>
            <div className="w-[5px] h-[5px] bg-gray-400 transform rotate-45"></div>
            <div className="h-px w-8 bg-gray-400"></div>
          </div>
          <span className="text-gray-300 text-[15px] font-sans font-light tracking-wide">
            Smart News , Instant Insight
          </span>
        </Link>
      </nav>
    );
  }

  return (
    <nav className="sticky top-0 w-full z-50 bg-black border-b border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Link to="/home" className="flex items-center space-x-3 relative group">
              <BrandSeal scale={0.08} />
              <span className="text-xl font-bold bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">
                ByteBrief
              </span>
            </Link>
          </div>

          {/* Rest of Navigation */}
          {!isLandingOrLogin && (
            <>
              {/* Desktop Navigation */}
              <div className="hidden md:flex items-center space-x-8">
                <Link to="/categories" className="text-gray-300 hover:text-white transition-colors">Categories</Link>

                {isAuthenticated && (
                  <Link to="/analytics" className="text-gray-300 hover:text-white transition-colors">Analytics</Link>
                )}

                <div className="flex items-center ml-4 pl-4 border-l border-gray-800">
                  <form onSubmit={handleSearch} className="relative mr-4 hidden lg:block text-gray-300">
                    <input
                      type="text"
                      placeholder="Ask anything..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="bg-gray-900 border border-gray-700 text-sm rounded-full pl-10 pr-4 py-2 focus:outline-none focus:border-cyan-500 w-64 transition-all"
                    />
                    <Search className="absolute left-3 top-2.5 h-4 w-4 text-gray-500" />
                  </form>

                  <div className="flex items-center space-x-4">
                    {isAuthenticated ? (
                      <div className="relative" ref={dropdownRef}>
                        <button
                          onClick={() => setDropdownOpen(!dropdownOpen)}
                          className="flex items-center gap-2 text-gray-300 hover:text-white transition-colors"
                        >
                          <div className="bg-gradient-to-r from-purple-500 to-cyan-500 p-1 rounded-full">
                            <User className="h-5 w-5 text-white" />
                          </div>
                          <span className="text-sm">{user?.first_name || user?.username || 'User'}</span>
                          <ChevronDown className={`h-4 w-4 transition-transform ${dropdownOpen ? 'rotate-180' : ''}`} />
                        </button>

                        {dropdownOpen && (
                          <div className="absolute right-0 mt-2 w-48 bg-gray-900 border border-gray-700 rounded-xl shadow-2xl py-1 z-50">
                            <Link
                              to="/saved"
                              onClick={() => setDropdownOpen(false)}
                              className="flex items-center gap-2 px-4 py-2.5 text-sm text-gray-300 hover:text-white hover:bg-gray-800 transition-colors"
                            >
                              <Bookmark className="h-4 w-4" /> Saved News
                            </Link>
                            <Link
                              to="/settings"
                              onClick={() => setDropdownOpen(false)}
                              className="flex items-center gap-2 px-4 py-2.5 text-sm text-gray-300 hover:text-white hover:bg-gray-800 transition-colors"
                            >
                              <Settings className="h-4 w-4" /> Account Settings
                            </Link>
                            <div className="border-t border-gray-800 my-1" />
                            <button
                              onClick={handleLogout}
                              className="flex items-center gap-2 w-full px-4 py-2.5 text-sm text-red-400 hover:text-red-300 hover:bg-gray-800 transition-colors"
                            >
                              <LogOut className="h-4 w-4" /> Logout
                            </button>
                          </div>
                        )}
                      </div>
                    ) : (
                      <>
                        <Link to="/login" className="text-gray-300 hover:text-white font-medium transition-colors">
                          Log in
                        </Link>
                        <Link to="/login" className="bg-gradient-to-r from-purple-600 to-cyan-600 hover:from-purple-500 hover:to-cyan-500 text-white px-5 py-2 rounded-full font-medium transition-all duration-300 transform hover:scale-105">
                          Sign up
                        </Link>
                      </>
                    )}
                  </div>
                </div>
              </div>

              {/* Mobile menu button */}
              <div className="md:hidden flex items-center">
                <button
                  onClick={() => setIsMenuOpen(!isMenuOpen)}
                  className="text-gray-300 hover:text-white"
                >
                  {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
                </button>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Mobile Navigation */}
      {isMenuOpen && (
        <div className="md:hidden bg-gray-900 border-b border-gray-800">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            {(!isLandingOrLogin || isAuthenticated) && (
              <Link to="/categories" className="block px-3 py-2 text-gray-300 hover:text-white hover:bg-gray-800 rounded-md">Categories</Link>
            )}

            {isAuthenticated && (
              <Link to="/analytics" className="block px-3 py-2 text-gray-300 hover:text-white hover:bg-gray-800 rounded-md">Analytics</Link>
            )}

            <div className="px-3 py-2 mt-2">
              <form onSubmit={handleSearch} className="relative text-gray-300">
                <input
                  type="text"
                  placeholder="Search news..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="bg-gray-800 border border-gray-700 text-sm rounded-lg pl-10 pr-4 py-2 w-full focus:outline-none focus:border-cyan-500"
                />
                <Search className="absolute left-3 top-2.5 h-4 w-4 text-gray-500" />
              </form>
            </div>

            <div className="pt-4 mt-4 border-t border-gray-800">
              {isAuthenticated ? (
                <>
                  <Link to="/saved" className="flex items-center gap-2 px-3 py-2 text-gray-300 hover:text-white hover:bg-gray-800 rounded-md">
                    <Bookmark className="h-4 w-4" /> Saved News
                  </Link>
                  <Link to="/settings" className="flex items-center gap-2 px-3 py-2 text-gray-300 hover:text-white hover:bg-gray-800 rounded-md">
                    <Settings className="h-4 w-4" /> Account Settings
                  </Link>
                  <button
                    onClick={handleLogout}
                    className="flex items-center gap-2 w-full text-left px-3 py-2 text-red-400 hover:text-red-300 hover:bg-gray-800 rounded-md"
                  >
                    <LogOut className="h-4 w-4" /> Logout
                  </button>
                </>
              ) : (
                !isLandingOrLogin && (
                  <>
                    <Link to="/login" className="block px-3 py-2 text-gray-300 hover:text-white hover:bg-gray-800 rounded-md">Log in</Link>
                    <Link to="/login" className="block px-3 py-2 mt-2 text-center bg-gradient-to-r from-purple-600 to-cyan-600 text-white rounded-md font-medium">Sign up</Link>
                  </>
                )
              )}
            </div>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navigation;
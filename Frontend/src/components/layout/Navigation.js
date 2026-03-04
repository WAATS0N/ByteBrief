import { Link } from 'react-router-dom';
import { Search, Menu, X, Brain } from 'lucide-react';

const Navigation = ({ currentTime, isMenuOpen, setIsMenuOpen }) => (
  <nav className="fixed top-0 w-full bg-black/80 backdrop-blur-xl border-b border-purple-500/20 z-50">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="flex items-center justify-between h-16">
        <div className="flex items-center space-x-2">
          <Link to="/" className="flex items-center space-x-2">
            <div className="bg-gradient-to-r from-purple-500 to-cyan-500 p-2 rounded-lg">
              <Brain className="h-6 w-6 text-white" />
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">
              ByteBrief
            </span>
            <span className="text-xs text-gray-400">AI-Powered</span>
          </Link>
        </div>

        <div className="hidden md:flex items-center space-x-8">
          {[
            { name: 'Home', path: '/' },
            { name: 'Categories', path: '/categories' }
          ].map((item) => (
            <Link
              key={item.name}
              to={item.path}
              className="text-sm font-medium text-gray-300 hover:text-purple-400 transition-all duration-300"
            >
              {item.name}
            </Link>
          ))}
        </div>

        <div className="flex items-center space-x-4">
          <div className="text-xs text-gray-400">
            Live: {currentTime.toLocaleTimeString()}
          </div>
          <button className="p-2 rounded-lg bg-gray-800 hover:bg-gray-700 transition-colors">
            <Search className="h-4 w-4 text-gray-300" />
          </button>
          <button
            className="md:hidden p-2"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>
      </div>
    </div>
  </nav>
);

export default Navigation;
import React from 'react';
import Navigation from './Navigation';
import BottomNavigation from './BottomNavigation';
import Footer from './Footer';

const Layout = ({ children, currentTime, isMenuOpen, setIsMenuOpen }) => (
  <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-black text-white flex flex-col relative overflow-x-hidden selection:bg-purple-500/30">

    {/* Global Space Background Theme */}
    <div className="fixed inset-0 opacity-20 pointer-events-none z-0">
      <div className="w-full h-full bg-gradient-to-r from-purple-500/10 to-cyan-500/10" />
    </div>

    <div className="relative z-10 flex flex-col flex-grow">
      <Navigation
        currentTime={currentTime}
        isMenuOpen={isMenuOpen}
        setIsMenuOpen={setIsMenuOpen}
      />
      <main className="flex-grow pb-16 md:pb-0">
        {children}
      </main>
      <Footer />
      <BottomNavigation />
    </div>
  </div>
);

export default Layout;
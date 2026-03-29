import React from 'react';
import Navigation from './Navigation';
import BottomNavigation from './BottomNavigation';
import Footer from './Footer';

const Layout = ({ children, currentTime, isMenuOpen, setIsMenuOpen }) => (
  <div className="min-h-screen bg-black text-white flex flex-col relative">
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
);

export default Layout;
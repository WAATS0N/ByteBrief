import React from 'react';
import Navigation from './Navigation';
import Footer from './Footer';

const Layout = ({ children, currentPage, setCurrentPage, currentTime, isMenuOpen, setIsMenuOpen }) => (
  <div className="min-h-screen bg-black text-white">
    <Navigation 
      currentPage={currentPage}
      setCurrentPage={setCurrentPage}
      currentTime={currentTime}
      isMenuOpen={isMenuOpen}
      setIsMenuOpen={setIsMenuOpen}
    />
    <main>
      {children}
    </main>
    <Footer />
  </div>
);

export default Layout;
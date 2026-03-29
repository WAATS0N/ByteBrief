import React from 'react';

const MastheadLogo = ({ scale = 1, fullWidth = false, className = '', style = {} }) => {
  const scaledWidth = fullWidth ? '100%' : (680 * scale);
  const scaledHeight = 320 * scale;
  
  const innerWidth = fullWidth ? `${100 / scale}%` : '100%';

  return (
    <div className={`masthead-logo-wrapper ${className}`} style={{ width: scaledWidth, height: scaledHeight, position: 'relative', margin: '0 auto', ...style }}>
      <div style={{ transform: `scale(${scale})`, transformOrigin: 'top left', position: 'absolute', top: 0, left: 0, width: innerWidth, height: 320 }}>
        <style>{`
        .mh-logo-container {
          position: relative;
          width: ${fullWidth ? '100%' : '680px'};
          height: 320px;
          background: #f5f0e8;
          border: ${fullWidth ? 'none' : '3px solid #1a1a1a'};
          border-bottom: 3px solid #1a1a1a;
          box-shadow: ${fullWidth ? '0 12px 24px rgba(0,0,0,0.5)' : '8px 8px 0 #000, 16px 16px 0 rgba(0,0,0,0.3)'};
          overflow: hidden;
          margin: 0 auto;
        }
        .mh-logo-container::before {
          content: '';
          position: absolute;
          inset: 0;
          background-image: 
            repeating-linear-gradient(
              0deg,
              transparent,
              transparent 22px,
              rgba(0,0,0,0.06) 22px,
              rgba(0,0,0,0.06) 23px
            );
          pointer-events: none;
          z-index: 1;
        }
        .mh-noise {
          position: absolute;
          inset: 0;
          background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.08'/%3E%3C/svg%3E");
          background-size: 256px;
          pointer-events: none;
          z-index: 2;
          opacity: 0.4;
          mix-blend-mode: multiply;
        }
        .mh-top-rule {
          position: absolute;
          top: 18px;
          left: 24px;
          right: 24px;
          display: flex;
          align-items: center;
          gap: 8px;
          z-index: 5;
        }
        .mh-rule-line { flex: 1; height: 2px; background: #1a1a1a; }
        .mh-rule-dot { width: 5px; height: 5px; background: #1a1a1a; border-radius: 50%; }
        .mh-rule-diamond { width: 8px; height: 8px; background: #1a1a1a; transform: rotate(45deg); }
        .mh-tagline-top {
          position: absolute;
          top: 28px;
          left: 50%;
          transform: translateX(-50%);
          font-family: 'Special Elite', cursive;
          font-size: 9px;
          letter-spacing: 4px;
          text-transform: uppercase;
          color: #1a1a1a;
          white-space: nowrap;
          z-index: 6;
        }
        .mh-bottom-rule {
          position: absolute;
          bottom: 18px;
          left: 24px;
          right: 24px;
          display: flex;
          align-items: center;
          gap: 6px;
          z-index: 5;
        }
        .mh-masthead {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          text-align: center;
          z-index: 10;
          width: 100%;
          margin-top: 10px;
        }
        .mh-brand-name {
          font-family: 'UnifrakturMaguntia', cursive;
          font-size: 92px;
          color: #0d0d0d;
          line-height: 0.95;
          letter-spacing: -2px;
          position: relative;
          display: inline-block;
          text-shadow: 3px 3px 0 rgba(0,0,0,0.15);
        }
        .mh-brand-name .mh-highlight { color: #8b0000; position: relative; }
        .mh-brand-name .mh-dash { color: #555; font-size: 72px; }
        .mh-subtitle-strip {
          position: absolute;
          bottom: 60px;
          left: 50%;
          transform: translateX(-50%);
          background: #1a1a1a;
          color: #f5f0e8;
          font-family: 'Special Elite', cursive;
          font-size: 11px;
          letter-spacing: 5px;
          text-transform: uppercase;
          padding: 6px 28px;
          white-space: nowrap;
          z-index: 10;
        }
        .mh-col-divider {
          position: absolute;
          top: 55px;
          bottom: 55px;
          width: 1px;
          background: rgba(0,0,0,0.25);
          z-index: 3;
        }
        .mh-col-divider.mh-left { left: 100px; }
        .mh-col-divider.mh-right { right: 100px; }
        .mh-filler-text {
          position: absolute;
          font-family: 'IM Fell English', serif;
          font-size: 7px;
          line-height: 1.6;
          color: rgba(0,0,0,0.35);
          z-index: 4;
          top: 60px;
          bottom: 75px;
          overflow: hidden;
        }
        .mh-filler-text.mh-left-col { left: 14px; width: 78px; text-align: left; }
        .mh-filler-text.mh-right-col { right: 14px; width: 78px; text-align: left; }
        .mh-dateline {
          position: absolute;
          bottom: 36px;
          left: 30px;
          font-family: 'Special Elite', cursive;
          font-size: 8px;
          color: rgba(0,0,0,0.5);
          letter-spacing: 1.5px;
          z-index: 10;
        }
        .mh-edition {
          position: absolute;
          bottom: 36px;
          right: 30px;
          font-family: 'Special Elite', cursive;
          font-size: 8px;
          color: rgba(0,0,0,0.5);
          letter-spacing: 1.5px;
          z-index: 10;
        }
        .mh-stamp {
          position: absolute;
          top: 55px;
          right: 34px;
          width: 64px;
          height: 64px;
          border: 3px solid rgba(139,0,0,0.5);
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          transform: rotate(-12deg);
          z-index: 12;
        }
        .mh-stamp-text {
          font-family: 'Special Elite', cursive;
          font-size: 8px;
          color: rgba(139,0,0,0.6);
          letter-spacing: 1px;
          text-align: center;
          text-transform: uppercase;
          line-height: 1.4;
        }
        .mh-ornament {
          font-size: 16px;
          color: #8b0000;
          display: inline-block;
          margin: 0 6px;
          vertical-align: middle;
          opacity: 0.7;
        }
      `}</style>
      <div className="mh-logo-container">
        <div className="mh-noise"></div>

        <div className="mh-filler-text mh-left-col">
          The morning dispatch of all things digital and notable. Our correspondents report from every corner of the network. Latest bulletins and dispatches from the wire. Breaking developments in technology, science, and world affairs. Trusted reporting since the dawn of the information age. All the news that bytes to print.
        </div>
        <div className="mh-filler-text mh-right-col">
          Compiled daily for the discerning reader of modern intelligence. From the server rooms to the streets, we bring you the briefings that matter most. Short, sharp, and to the point — the news in a byte. Subscribe for morning and evening editions delivered directly.
        </div>

        <div className="mh-col-divider mh-left"></div>
        <div className="mh-col-divider mh-right"></div>

        <div className="mh-top-rule">
          <div className="mh-rule-line"></div>
          <div className="mh-rule-diamond"></div>
          <div className="mh-rule-line"></div>
        </div>

        <div className="mh-tagline-top">★ &nbsp; The Digital News Digest &nbsp; ★</div>

        <div className="mh-stamp">
          <div className="mh-stamp-text">AI<br/>POWERED<br/>NEWS</div>
        </div>

        <div className="mh-masthead">
          <div className="mh-brand-name">
            <span className="mh-highlight">B</span>yte<span className="mh-dash">-</span><span className="mh-highlight">B</span>rief
          </div>
        </div>

        <div className="mh-subtitle-strip">
          <span className="mh-ornament">◆</span> Your News. Your Byte. <span className="mh-ornament">◆</span>
        </div>

        <div className="mh-bottom-rule">
          <div className="mh-rule-line"></div>
          <div className="mh-rule-diamond"></div>
          <div className="mh-rule-dot"></div>
          <div className="mh-rule-diamond"></div>
          <div className="mh-rule-line"></div>
        </div>

        <div className="mh-dateline">EST. 2025 · VOL. I</div>
        <div className="mh-edition">DIGITAL EDITION</div>
      </div>
      </div>
    </div>
  );
};

export default MastheadLogo;

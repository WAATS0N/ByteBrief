import React from 'react';

const BrandSeal = ({ scale = 1, rotating = false, className = '', style = {} }) => {
  const scaledSize = 520 * scale;
  return (
    <div className={`brand-seal-wrapper ${className}`} style={{ width: scaledSize, height: scaledSize, position: 'relative', ...style }}>
      <div style={{ transform: `scale(${scale})`, transformOrigin: 'top left', position: 'absolute', top: 0, left: 0 }}>
        <style>{`
          @keyframes logoSpin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
          }
          .logo-circle {
            position: relative;
            width: 520px;
            height: 520px;
          border-radius: 50%;
          background: #f4ede0;
          box-shadow:
            0 0 0 7px #1a1008,
            0 0 0 13px #8b0000,
            0 0 0 20px #1a1008,
            0 30px 80px rgba(0,0,0,0.8);
          overflow: hidden;
          margin: 0 auto;
        }
        .logo-spin {
          animation: logoSpin 20s linear infinite;
        }
        .logo-circle::before {
          content: '';
          position: absolute;
          inset: 0;
          border-radius: 50%;
          background-image: repeating-linear-gradient(
            0deg,
            transparent, transparent 15px,
            rgba(0,0,0,0.042) 15px, rgba(0,0,0,0.042) 16px
          );
          z-index: 1;
          pointer-events: none;
        }
        .logo-circle::after {
          content: '';
          position: absolute;
          inset: 0;
          border-radius: 50%;
          background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.12'/%3E%3C/svg%3E");
          mix-blend-mode: multiply;
          z-index: 2;
          pointer-events: none;
          opacity: 0.5;
        }
        .ring {
          position: absolute;
          border-radius: 50%;
          top: 50%; left: 50%;
          transform: translate(-50%, -50%);
          z-index: 5;
        }
        .ring-1 { width: 498px; height: 498px; border: 2.5px solid rgba(0,0,0,0.55); }
        .ring-2 { width: 470px; height: 470px; border: 1.5px solid rgba(139,0,0,0.45); }
        .ring-3 { width: 444px; height: 444px; border: 2px   solid rgba(0,0,0,0.5); }
        .ring-4 { width: 408px; height: 408px; border: 1px   solid rgba(0,0,0,0.18); }
        .ring-5 { width: 210px; height: 210px; border: 1.5px solid rgba(139,0,0,0.35); }
        .ring-6 { width: 188px; height: 188px; border: 2px   solid rgba(0,0,0,0.45); }
        .circular-text-svg {
          position: absolute;
          top: 0; left: 0;
          width: 100%; height: 100%;
          z-index: 8;
        }
        .micro-text {
          position: absolute;
          font-family: 'IM Fell English', serif;
          font-size: 7px;
          color: rgba(0,0,0,0.22);
          line-height: 1.6;
          text-align: center;
          z-index: 6;
          left: 50%;
          transform: translateX(-50%);
          width: 310px;
        }
        .mt-top    { top: 72px; }
        .mt-bottom { bottom: 68px; }
        .center-content {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -52%);
          text-align: center;
          z-index: 10;
          width: 340px;
        }
        .bb-top-ornament {
          font-family: 'Special Elite', cursive;
          font-size: 9.5px;
          letter-spacing: 4px;
          text-transform: uppercase;
          color: #8b0000;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 6px;
          margin-bottom: 4px;
        }
        .orn-line { flex: 1; height: 1px; background: rgba(139,0,0,0.5); max-width: 44px; }
        .bb-mono {
          font-family: 'Playfair Display', serif;
          font-style: italic;
          font-weight: 700;
          font-size: 24px;
          color: #1a1008;
          letter-spacing: -1px;
          margin-bottom: 2px;
        }
        .brand-main {
          font-family: 'UnifrakturMaguntia', cursive;
          font-size: 84px;
          color: #0d0d0d;
          line-height: 0.92;
          letter-spacing: -1px;
          text-shadow: 3px 4px 0 rgba(0,0,0,0.1);
        }
        .brand-main .b-red { color: #8b0000; }
        .brand-main .dash  { font-size: 62px; color: #444; }
        .divider-rule {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 5px;
          margin: 10px 0 7px;
        }
        .dr-line    { flex: 1; height: 1px; background: #1a1008; max-width: 68px; }
        .dr-diamond { width: 6px; height: 6px; background: #8b0000; transform: rotate(45deg); flex-shrink: 0; }
        .tagline {
          font-family: 'Special Elite', cursive;
          font-size: 11px;
          letter-spacing: 4px;
          text-transform: uppercase;
          color: #2a1a08;
          margin-bottom: 10px;
        }
        .black-band {
          background: #1a1008;
          color: #f4ede0;
          font-family: 'Special Elite', cursive;
          font-size: 10px;
          letter-spacing: 5px;
          text-transform: uppercase;
          padding: 6px 24px;
          display: inline-block;
        }
      `}</style>
      <div className={`logo-circle ${rotating ? 'logo-spin' : ''}`}>
        <div className="ring ring-1"></div>
        <div className="ring ring-2"></div>
        <div className="ring ring-3"></div>
        <div className="ring ring-4"></div>
        <div className="ring ring-5"></div>
        <div className="ring ring-6"></div>

        <svg className="circular-text-svg" viewBox="0 0 520 520">
          <defs>
            <path id="topArc" d="M 50,260 a 210,210 0 0,1 420,0" />
            <path id="bottomArc" d="M 62,272 a 198,198 0 0,0 396,0" />
            <path id="midArc" d="M 86,260 a 174,174 0 0,1 348,0" />
            <path id="midArcB" d="M 96,268 a 164,164 0 0,0 328,0" />
          </defs>

          <text fontFamily="'Special Elite', cursive" fontSize="12.5" fill="#1a1008" letterSpacing="5">
            <textPath href="#topArc" startOffset="4%">✦ BYTE-BRIEF · THE DIGITAL NEWS DIGEST · AI-POWERED ·</textPath>
          </text>
          <text fontFamily="'Special Elite', cursive" fontSize="11" fill="#8b0000" letterSpacing="3.5">
            <textPath href="#bottomArc" startOffset="7%">◆ YOUR NEWS · YOUR BYTE · EVERY DAY · EST. 2025 · VOL. I ◆</textPath>
          </text>
          <text fontFamily="'IM Fell English', serif" fontSize="9" fill="rgba(0,0,0,0.28)" letterSpacing="2.5">
            <textPath href="#midArc" startOffset="0%">· News · Intelligence · Briefings · Digital · Technology ·</textPath>
          </text>
          <text fontFamily="'IM Fell English', serif" fontSize="8.5" fill="rgba(0,0,0,0.22)" letterSpacing="2">
            <textPath href="#midArcB" startOffset="14%">· Headlines · Analysis · Reports · Updates ·</textPath>
          </text>

          <g stroke="#1a1008" strokeWidth="1.8" opacity="0.38">
            <line x1="260" y1="22" x2="260" y2="32" transform="rotate(0,260,260)" />
            <line x1="260" y1="22" x2="260" y2="32" transform="rotate(30,260,260)" />
            <line x1="260" y1="22" x2="260" y2="32" transform="rotate(60,260,260)" />
            <line x1="260" y1="22" x2="260" y2="32" transform="rotate(90,260,260)" />
            <line x1="260" y1="22" x2="260" y2="32" transform="rotate(120,260,260)" />
            <line x1="260" y1="22" x2="260" y2="32" transform="rotate(150,260,260)" />
            <line x1="260" y1="22" x2="260" y2="32" transform="rotate(180,260,260)" />
            <line x1="260" y1="22" x2="260" y2="32" transform="rotate(210,260,260)" />
            <line x1="260" y1="22" x2="260" y2="32" transform="rotate(240,260,260)" />
            <line x1="260" y1="22" x2="260" y2="32" transform="rotate(270,260,260)" />
            <line x1="260" y1="22" x2="260" y2="32" transform="rotate(300,260,260)" />
            <line x1="260" y1="22" x2="260" y2="32" transform="rotate(330,260,260)" />
          </g>

          <g fill="#8b0000" opacity="0.65">
            <rect x="257" y="90" width="7" height="7" transform="rotate(45,260.5,93.5)" />
            <rect x="257" y="90" width="7" height="7" transform="rotate(45,260.5,93.5) rotate(90,260,260)" />
            <rect x="257" y="90" width="7" height="7" transform="rotate(45,260.5,93.5) rotate(180,260,260)" />
            <rect x="257" y="90" width="7" height="7" transform="rotate(45,260.5,93.5) rotate(270,260,260)" />
          </g>
        </svg>

        <div className="micro-text mt-top">All the intelligence that's fit to byte. Dispatches from the digital frontier.</div>
        <div className="micro-text mt-bottom">Compiled by algorithms. Trusted by readers. Morning &amp; evening editions.</div>

        <div className="center-content">
          <div className="bb-top-ornament">
            <span className="orn-line"></span>
            <span>News</span>
            <span class="orn-line"></span>
          </div>

          <div className="bb-mono">Bʙ</div>

          <div className="brand-main">
            <span className="b-red">B</span>yte<span className="dash">-</span><span className="b-red">B</span>rief
          </div>

          <div className="divider-rule">
            <span className="dr-line"></span>
            <span className="dr-diamond"></span>
            <span className="dr-diamond"></span>
            <span className="dr-diamond"></span>
            <span className="dr-line"></span>
          </div>

          <div className="tagline">Digital · Brief · Brilliant</div>
          <div className="black-band">AI News Generator</div>
        </div>
      </div>
    </div>
    </div>
  );
};

export default BrandSeal;

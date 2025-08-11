import React from 'react';
import './Footer.css';

const Footer: React.FC = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-top">
          <div className="footer-section">
            <p className="footer-text">
              Данные взяты из{' '}
              <a
                href="https://www.themoviedb.org/"
                target="_blank"
                rel="noopener noreferrer"
                className="footer-link"
              >
                TMDB
              </a>
            </p>
          </div>
          <div className="footer-section">
            <p className="footer-text">yehor.kvasenko@gmail.com</p>
          </div>
          <div className="footer-section">
            <p className="footer-text">Дизайн от GitHub Copilot</p>
          </div>
        </div>
        <div className="footer-bottom">
          <div className="footer-section">
            <p className="footer-text">© 2025 - Все права не защищены</p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

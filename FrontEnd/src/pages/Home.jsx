import React, { useState, useEffect } from 'react';
import '../css/Home.css';

const AIFleetManager = () => {
  const [scrolled, setScrolled] = useState(false);
  const [statsVisible, setStatsVisible] = useState(false);
  const [animatedStats, setAnimatedStats] = useState({
    cost: 0,
    fuel: 0,
    breakdowns: 0,
    delivery: 0
  });

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 100);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !statsVisible) {
          setStatsVisible(true);
          animateStats();
        }
      },
      { threshold: 0.5 }
    );

    const statsSection = document.getElementById('stats');
    if (statsSection) observer.observe(statsSection);
    return () => observer.disconnect();
  }, [statsVisible]);

  const animateStats = () => {
    const targets = { cost: 30, fuel: 45, breakdowns: 50, delivery: 98 };
    const duration = 2000;
    const steps = 50;
    const stepTime = duration / steps;
    let currentStep = 0;
    const interval = setInterval(() => {
      currentStep++;
      const progress = currentStep / steps;
      setAnimatedStats({
        cost: Math.floor(targets.cost * progress),
        fuel: Math.floor(targets.fuel * progress),
        breakdowns: Math.floor(targets.breakdowns * progress),
        delivery: Math.floor(targets.delivery * progress)
      });
      if (currentStep >= steps) {
        clearInterval(interval);
        setAnimatedStats(targets);
      }
    }, stepTime);
  };

  const smoothScroll = (targetId) => {
    const element = document.getElementById(targetId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  return (
    <div className="page">
      <header className={scrolled ? 'scrolled' : ''}>
        <nav>
          <div className="logo">AI Smart Fleet Manager</div>
          <ul>
            {['features', 'pricing', 'about', 'contact'].map((item, index) => (
              <li key={index}>
                <a href={`#${item}`} onClick={(e) => {
                  e.preventDefault();
                  smoothScroll(item);
                }}>
                  {item.charAt(0).toUpperCase() + item.slice(1)}
                </a>
              </li>
            ))}
          </ul>
          <button className="demo-btn" onClick={() => smoothScroll('demo')}>
            Get Demo
          </button>
        </nav>
      </header>

      <section className="hero">
        <div className="hero-content">
          <h1>Intelligent Fleet Management with AI</h1>
          <p>Optimize your fleet operations with cutting-edge artificial intelligence. Reduce costs, improve efficiency, and enhance safety with our smart fleet management solution.</p>
          <div className="hero-buttons">
            <button className="primary-btn" onClick={() => smoothScroll('demo')}>Start Free Trial</button>
            <button className="secondary-btn" onClick={() => smoothScroll('features')}>Learn More</button>
          </div>
        </div>
      </section>

      <section id="features" className="features">
        <h2>Powerful AI-Driven Features</h2>
        <div className="features-grid">
          {["Route Optimization", "Predictive Maintenance", "Driver Safety Monitoring", "Smart Analytics", "Automated Dispatch", "Real-time Tracking"].map((title, index) => (
            <div className="feature-card" key={index}>
              <h3>{title}</h3>
              <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis nec justo eget.</p>
            </div>
          ))}
        </div>
      </section>

      <section id="stats" className="stats">
        <div className="stats-grid">
          {[
            { number: animatedStats.cost, label: 'Cost Reduction', suffix: '%' },
            { number: animatedStats.fuel, label: 'Fuel Savings', suffix: '%' },
            { number: animatedStats.breakdowns, label: 'Fewer Breakdowns', suffix: '%' },
            { number: animatedStats.delivery, label: 'On-time Delivery', suffix: '%' }
          ].map((stat, i) => (
            <div key={i} className="stat-box">
              <span className="stat-number">{stat.number}{stat.suffix}</span>
              <span className="stat-label">{stat.label}</span>
            </div>
          ))}
        </div>
      </section>

      <section id="demo" className="cta">
        <h2>Ready to Transform Your Fleet?</h2>
        <p>Join thousands of businesses that have revolutionized their fleet operations with AI Smart Fleet Manager</p>
        <button className="primary-btn">Start Your Free Trial Today</button>
      </section>

      <footer className="footer">
        <div className="footer-grid">
          <div>
            <h4>Product</h4>
            <p><a href="#">Features</a></p>
            <p><a href="#">Pricing</a></p>
            <p><a href="#">API</a></p>
          </div>
          <div>
            <h4>Support</h4>
            <p><a href="#">Documentation</a></p>
            <p><a href="#">Help Center</a></p>
            <p><a href="#">Contact</a></p>
          </div>
          <div>
            <h4>Company</h4>
            <p><a href="#">About</a></p>
            <p><a href="#">Blog</a></p>
            <p><a href="#">Careers</a></p>
          </div>
        </div>
        <div className="footer-bottom">
          &copy; 2025 AI Smart Fleet Manager. All rights reserved.
        </div>
      </footer>
    </div>
  );
};

export default AIFleetManager;

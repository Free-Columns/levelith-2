/**
 * Landing Page - Main entry point for Levelith
 * Uses ONETRUTH configuration for all styling
 */

import React from 'react';
import { Link } from 'react-router-dom';
import { ONETRUTH } from '../config/ONETRUTH';

const Landing: React.FC = () => {
  const styles = {
    container: {
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column' as const,
      background: `linear-gradient(135deg, ${ONETRUTH.colors.primary} 0%, ${ONETRUTH.colors.primaryDark} 100%)`,
    },
    header: {
      padding: ONETRUTH.spacing.lg,
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
    },
    logo: {
      fontSize: ONETRUTH.fonts.sizes['3xl'],
      fontFamily: ONETRUTH.fonts.heading,
      fontWeight: ONETRUTH.fonts.weights.bold,
      color: ONETRUTH.colors.textInverse,
    },
    nav: {
      display: 'flex',
      gap: ONETRUTH.spacing.md,
    },
    navLink: {
      padding: `${ONETRUTH.spacing.sm} ${ONETRUTH.spacing.md}`,
      color: ONETRUTH.colors.textInverse,
      fontSize: ONETRUTH.fonts.sizes.base,
      fontWeight: ONETRUTH.fonts.weights.medium,
      borderRadius: ONETRUTH.borderRadius.md,
      transition: `background-color ${ONETRUTH.transitions.fast}`,
      backgroundColor: 'transparent',
      border: 'none',
      cursor: 'pointer',
    },
    hero: {
      flex: 1,
      display: 'flex',
      flexDirection: 'column' as const,
      justifyContent: 'center',
      alignItems: 'center',
      textAlign: 'center' as const,
      padding: ONETRUTH.spacing['2xl'],
      color: ONETRUTH.colors.textInverse,
    },
    heroTitle: {
      fontSize: ONETRUTH.fonts.sizes['5xl'],
      fontFamily: ONETRUTH.fonts.heading,
      fontWeight: ONETRUTH.fonts.weights.extrabold,
      marginBottom: ONETRUTH.spacing.lg,
      lineHeight: ONETRUTH.fonts.lineHeights.tight,
    },
    heroSubtitle: {
      fontSize: ONETRUTH.fonts.sizes['2xl'],
      fontWeight: ONETRUTH.fonts.weights.normal,
      marginBottom: ONETRUTH.spacing['2xl'],
      maxWidth: '800px',
      lineHeight: ONETRUTH.fonts.lineHeights.relaxed,
      opacity: 0.95,
    },
    ctaContainer: {
      display: 'flex',
      gap: ONETRUTH.spacing.lg,
      marginTop: ONETRUTH.spacing.xl,
    },
    ctaButton: {
      padding: `${ONETRUTH.spacing.md} ${ONETRUTH.spacing['2xl']}`,
      fontSize: ONETRUTH.fonts.sizes.lg,
      fontWeight: ONETRUTH.fonts.weights.semibold,
      borderRadius: ONETRUTH.borderRadius.lg,
      border: 'none',
      cursor: 'pointer',
      transition: `all ${ONETRUTH.transitions.base}`,
      boxShadow: ONETRUTH.shadows.md,
    },
    ctaPrimary: {
      backgroundColor: ONETRUTH.colors.secondary,
      color: ONETRUTH.colors.textInverse,
    },
    ctaSecondary: {
      backgroundColor: ONETRUTH.colors.surface,
      color: ONETRUTH.colors.primary,
    },
    features: {
      padding: ONETRUTH.spacing['3xl'],
      backgroundColor: ONETRUTH.colors.background,
    },
    featuresTitle: {
      fontSize: ONETRUTH.fonts.sizes['4xl'],
      fontFamily: ONETRUTH.fonts.heading,
      fontWeight: ONETRUTH.fonts.weights.bold,
      color: ONETRUTH.colors.textDark,
      textAlign: 'center' as const,
      marginBottom: ONETRUTH.spacing['2xl'],
    },
    featuresGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
      gap: ONETRUTH.spacing.xl,
      maxWidth: '1200px',
      margin: '0 auto',
    },
    featureCard: {
      padding: ONETRUTH.spacing.xl,
      backgroundColor: ONETRUTH.colors.surface,
      borderRadius: ONETRUTH.borderRadius.lg,
      boxShadow: ONETRUTH.shadows.sm,
      transition: `all ${ONETRUTH.transitions.base}`,
    },
    featureIcon: {
      fontSize: ONETRUTH.fonts.sizes['4xl'],
      marginBottom: ONETRUTH.spacing.md,
    },
    featureTitle: {
      fontSize: ONETRUTH.fonts.sizes['2xl'],
      fontFamily: ONETRUTH.fonts.heading,
      fontWeight: ONETRUTH.fonts.weights.semibold,
      color: ONETRUTH.colors.textDark,
      marginBottom: ONETRUTH.spacing.sm,
    },
    featureDescription: {
      fontSize: ONETRUTH.fonts.sizes.base,
      color: ONETRUTH.colors.textLight,
      lineHeight: ONETRUTH.fonts.lineHeights.relaxed,
    },
    footer: {
      padding: ONETRUTH.spacing.xl,
      backgroundColor: ONETRUTH.colors.surfaceDark,
      color: ONETRUTH.colors.textInverse,
      textAlign: 'center' as const,
    },
  };

  const features = [
    {
      icon: '🎓',
      title: 'Track Education',
      description: 'Document certificates, degrees, and courses to showcase your learning journey.',
      color: ONETRUTH.colors.education,
    },
    {
      icon: '💼',
      title: 'Workplace Experience',
      description: 'Track gigs, part-time, and full-time positions with industry-specific categorization.',
      color: ONETRUTH.colors.workplace,
    },
    {
      icon: '🚀',
      title: 'Skills Showcase',
      description: 'Highlight soft skills, hard skills, and native talents that set you apart.',
      color: ONETRUTH.colors.skills,
    },
    {
      icon: '🎮',
      title: 'Gamification',
      description: 'Earn points, achievements, and level up as you build your professional profile.',
      color: ONETRUTH.colors.secondary,
    },
    {
      icon: '🌐',
      title: 'Social Networking',
      description: 'Connect with professionals and share your experiences in an engaging format.',
      color: ONETRUTH.colors.primary,
    },
    {
      icon: '📊',
      title: 'Industry Insights',
      description: 'NAICS-based categorization provides valuable industry-specific analytics.',
      color: ONETRUTH.colors.info,
    },
  ];

  return (
    <div style={styles.container}>
      {/* Header */}
      <header style={styles.header}>
        <div style={styles.logo}>Levelith</div>
        <nav style={styles.nav}>
          <Link to="/docs" style={styles.navLink}>Docs</Link>
          <Link to="/admin" style={styles.navLink}>Admin</Link>
        </nav>
      </header>

      {/* Hero Section */}
      <section style={styles.hero}>
        <h1 style={styles.heroTitle}>
          Transform Your Professional Journey
        </h1>
        <p style={styles.heroSubtitle}>
          Levelith is a gamified social-resume platform that turns experience tracking
          into an engaging, interactive adventure. Build your profile, earn achievements,
          and connect with professionals worldwide.
        </p>
        <div style={styles.ctaContainer}>
          <button
            style={{ ...styles.ctaButton, ...styles.ctaPrimary }}
            onMouseOver={(e) => {
              e.currentTarget.style.backgroundColor = ONETRUTH.colors.secondaryDark;
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = ONETRUTH.shadows.lg;
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.backgroundColor = ONETRUTH.colors.secondary;
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = ONETRUTH.shadows.md;
            }}
          >
            Get Started
          </button>
          <Link to="/docs">
            <button
              style={{ ...styles.ctaButton, ...styles.ctaSecondary }}
              onMouseOver={(e) => {
                e.currentTarget.style.backgroundColor = ONETRUTH.colors.borderLight;
                e.currentTarget.style.transform = 'translateY(-2px)';
                e.currentTarget.style.boxShadow = ONETRUTH.shadows.lg;
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.backgroundColor = ONETRUTH.colors.surface;
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = ONETRUTH.shadows.md;
              }}
            >
              Learn More
            </button>
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section style={styles.features}>
        <h2 style={styles.featuresTitle}>Key Features</h2>
        <div style={styles.featuresGrid}>
          {features.map((feature, index) => (
            <div
              key={index}
              style={styles.featureCard}
              onMouseOver={(e) => {
                e.currentTarget.style.transform = 'translateY(-8px)';
                e.currentTarget.style.boxShadow = ONETRUTH.shadows.lg;
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = ONETRUTH.shadows.sm;
              }}
            >
              <div style={{ ...styles.featureIcon, color: feature.color }}>
                {feature.icon}
              </div>
              <h3 style={styles.featureTitle}>{feature.title}</h3>
              <p style={styles.featureDescription}>{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer style={styles.footer}>
        <p>© 2025 Levelith by Semour Media Group. Built with AI-first methodology.</p>
      </footer>
    </div>
  );
};

export default Landing;

import type { ReactNode } from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={clsx('hero', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className={styles.heroTitle}>
          {siteConfig.title}
        </Heading>
        <p className={styles.heroSubtitle}>{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className={clsx('button button--lg', styles.primaryButton)}
            to="/book/intro">
            Start Learning
          </Link>
          <Link
            className={clsx('button button--lg', styles.secondaryButton)}
            to="/profile">
            Create Profile
          </Link>
        </div>
      </div>
    </header>
  );
}

interface FeatureItem {
  title: string;
  icon: string;
  description: string;
}

const features: FeatureItem[] = [
  {
    title: 'AI-Powered Learning',
    icon: '🤖',
    description: 'Learn AI development with comprehensive, structured content covering LLMs, RAG systems, and AI agents.',
  },
  {
    title: 'Intelligent Chatbot',
    icon: '💬',
    description: 'Ask questions about any chapter. Select text to get instant explanations with citations.',
  },
  {
    title: 'Personalized Experience',
    icon: '✨',
    description: 'Content adapts to your skill level, known programming languages, and learning goals.',
  },
  {
    title: 'Urdu Translation',
    icon: '🌐',
    description: 'Toggle Urdu translation on any chapter while preserving code blocks and structure.',
  },
  {
    title: 'Spec-Kit Plus Methodology',
    icon: '📚',
    description: 'Each chapter follows: Objectives → Concepts → Examples → Exercises → Summary.',
  },
  {
    title: 'Production-Ready Code',
    icon: '💻',
    description: 'All examples use real-world patterns with FastAPI, OpenAI, Qdrant, and modern Python.',
  },
];

function Feature({ title, icon, description }: FeatureItem) {
  return (
    <div className={styles.feature}>
      <div className={styles.featureIcon}>{icon}</div>
      <h3 className={styles.featureTitle}>{title}</h3>
      <p className={styles.featureDescription}>{description}</p>
    </div>
  );
}

function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className={styles.featuresGrid}>
          {features.map((feature, idx) => (
            <Feature key={idx} {...feature} />
          ))}
        </div>
      </div>
    </section>
  );
}

function ChaptersPreview() {
  const chapters = [
    { num: 1, title: 'AI Foundations', desc: 'Core concepts and history of AI' },
    { num: 2, title: 'LLM Fundamentals', desc: 'Understanding Large Language Models' },
    { num: 3, title: 'Prompt Engineering', desc: 'Crafting effective AI prompts' },
    { num: 4, title: 'RAG Systems', desc: 'Building knowledge-grounded AI' },
    { num: 5, title: 'AI Agents', desc: 'Creating autonomous AI systems' },
    { num: 6, title: 'Building AI Apps', desc: 'Full-stack AI development' },
  ];

  return (
    <section className={styles.chapters}>
      <div className="container">
        <h2 className={styles.sectionTitle}>What You'll Learn</h2>
        <div className={styles.chaptersGrid}>
          {chapters.map((chapter) => (
            <Link
              key={chapter.num}
              to={`/book/chapter-${chapter.num}/overview`}
              className={styles.chapterCard}
            >
              <span className={styles.chapterNum}>Chapter {chapter.num}</span>
              <h3>{chapter.title}</h3>
              <p>{chapter.desc}</p>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}

function CallToAction() {
  return (
    <section className={styles.cta}>
      <div className="container">
        <h2>Ready to Master AI Development?</h2>
        <p>Start your journey from AI fundamentals to building production-ready applications.</p>
        <Link
          className={clsx('button button--lg', styles.ctaButton)}
          to="/book/intro">
          Begin Your Journey
        </Link>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title="Home"
      description={siteConfig.tagline}>
      <HomepageHeader />
      <main>
        <HomepageFeatures />
        <ChaptersPreview />
        <CallToAction />
      </main>
    </Layout>
  );
}

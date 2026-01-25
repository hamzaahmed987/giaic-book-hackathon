import React, { useState } from 'react';
import styles from './styles.module.css';

interface ChapterActionsProps {
  chapterId: string;
}

export default function ChapterActions({ chapterId }: ChapterActionsProps): JSX.Element {
  const [isPersonalizing, setIsPersonalizing] = useState(false);
  const [isTranslating, setIsTranslating] = useState(false);
  const [isUrdu, setIsUrdu] = useState(false);
  const [isPersonalized, setIsPersonalized] = useState(false);

  // API base URL - uses window location in production, localhost in development
  const getApiBaseUrl = () => window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : `${window.location.protocol}//${window.location.hostname}:8000`;

  const handlePersonalize = async () => {
    setIsPersonalizing(true);
    try {
      const response = await fetch(`${getApiBaseUrl()}/api/content/personalize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ chapter_id: chapterId }),
      });

      if (response.ok) {
        const data = await response.json();
        setIsPersonalized(true);
        // In a real implementation, this would update the page content
        console.log('Personalized content:', data);
      }
    } catch (error) {
      console.error('Personalization error:', error);
    } finally {
      setIsPersonalizing(false);
    }
  };

  const handleTranslate = async () => {
    setIsTranslating(true);
    try {
      const response = await fetch(`${getApiBaseUrl()}/api/content/translate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          chapter_id: chapterId,
          target_language: isUrdu ? 'en' : 'ur'
        }),
      });

      if (response.ok) {
        setIsUrdu(!isUrdu);
        // In a real implementation, this would update the page content
      }
    } catch (error) {
      console.error('Translation error:', error);
    } finally {
      setIsTranslating(false);
    }
  };

  return (
    <div className={styles.chapterActions}>
      <button
        className={`${styles.actionButton} ${styles.personalizeButton} ${isPersonalized ? styles.active : ''}`}
        onClick={handlePersonalize}
        disabled={isPersonalizing}
      >
        {isPersonalizing ? (
          <span className={styles.spinner}>⏳</span>
        ) : (
          <>
            <span className={styles.icon}>✨</span>
            {isPersonalized ? 'Personalized' : 'Personalize this chapter'}
          </>
        )}
      </button>

      <button
        className={`${styles.actionButton} ${styles.translateButton} ${isUrdu ? styles.active : ''}`}
        onClick={handleTranslate}
        disabled={isTranslating}
      >
        {isTranslating ? (
          <span className={styles.spinner}>⏳</span>
        ) : (
          <>
            <span className={styles.icon}>🌐</span>
            {isUrdu ? 'Switch to English' : 'اردو میں ترجمہ کریں'}
          </>
        )}
      </button>
    </div>
  );
}

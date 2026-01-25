import React, { useState } from 'react';
import Layout from '@theme/Layout';
import styles from './profile.module.css';

export default function Profile(): JSX.Element {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isSignUp, setIsSignUp] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
  });
  const [profile, setProfile] = useState({
    experience_level: 'beginner',
    known_languages: [] as string[],
    hardware_tier: 'medium',
    goals: [] as string[],
  });

  const languageOptions = ['Python', 'JavaScript', 'TypeScript', 'Java', 'C++', 'Go', 'Rust'];
  const goalOptions = ['Learning', 'Professional Development', 'Research', 'Building Projects'];

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleProfileChange = (field: string, value: any) => {
    setProfile({ ...profile, [field]: value });
  };

  const toggleArrayItem = (field: 'known_languages' | 'goals', item: string) => {
    const current = profile[field];
    const updated = current.includes(item)
      ? current.filter(i => i !== item)
      : [...current, item];
    handleProfileChange(field, updated);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // In production, this would call the auth API
    console.log('Form submitted:', formData);
    setIsLoggedIn(true);
  };

  const handleProfileSave = async () => {
    // In production, this would call the profile API
    console.log('Profile saved:', profile);
    alert('Profile saved successfully!');
  };

  if (!isLoggedIn) {
    return (
      <Layout title="Profile" description="Manage your profile">
        <div className={styles.container}>
          <div className={styles.authCard}>
            <h1>{isSignUp ? 'Create Account' : 'Welcome Back'}</h1>
            <p className={styles.subtitle}>
              {isSignUp
                ? 'Join us to get personalized learning experience'
                : 'Sign in to continue your learning journey'}
            </p>

            <form onSubmit={handleSubmit} className={styles.form}>
              {isSignUp && (
                <div className={styles.inputGroup}>
                  <label htmlFor="name">Name</label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    placeholder="Your name"
                    required
                  />
                </div>
              )}

              <div className={styles.inputGroup}>
                <label htmlFor="email">Email</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  placeholder="your@email.com"
                  required
                />
              </div>

              <div className={styles.inputGroup}>
                <label htmlFor="password">Password</label>
                <input
                  type="password"
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  placeholder="••••••••"
                  required
                />
              </div>

              <button type="submit" className={styles.submitButton}>
                {isSignUp ? 'Create Account' : 'Sign In'}
              </button>
            </form>

            <p className={styles.switchText}>
              {isSignUp ? 'Already have an account?' : "Don't have an account?"}
              <button
                type="button"
                className={styles.switchButton}
                onClick={() => setIsSignUp(!isSignUp)}
              >
                {isSignUp ? 'Sign In' : 'Sign Up'}
              </button>
            </p>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout title="Profile" description="Manage your profile">
      <div className={styles.container}>
        <div className={styles.profileCard}>
          <h1>Your Profile</h1>
          <p className={styles.subtitle}>
            Help us personalize your learning experience
          </p>

          <div className={styles.profileSection}>
            <h2>Experience Level</h2>
            <div className={styles.radioGroup}>
              {['beginner', 'intermediate', 'advanced'].map(level => (
                <label key={level} className={styles.radioLabel}>
                  <input
                    type="radio"
                    name="experience"
                    value={level}
                    checked={profile.experience_level === level}
                    onChange={() => handleProfileChange('experience_level', level)}
                  />
                  <span className={styles.radioButton}></span>
                  {level.charAt(0).toUpperCase() + level.slice(1)}
                </label>
              ))}
            </div>
          </div>

          <div className={styles.profileSection}>
            <h2>Programming Languages Known</h2>
            <div className={styles.chipGroup}>
              {languageOptions.map(lang => (
                <button
                  key={lang}
                  type="button"
                  className={`${styles.chip} ${profile.known_languages.includes(lang) ? styles.chipActive : ''}`}
                  onClick={() => toggleArrayItem('known_languages', lang)}
                >
                  {lang}
                </button>
              ))}
            </div>
          </div>

          <div className={styles.profileSection}>
            <h2>Hardware Tier</h2>
            <p className={styles.hint}>This helps us adjust code examples for your setup</p>
            <div className={styles.radioGroup}>
              {[
                { value: 'low', label: 'Low-end (< 8GB RAM)', desc: 'Basic laptop/computer' },
                { value: 'medium', label: 'Medium (8-16GB RAM)', desc: 'Standard development machine' },
                { value: 'high', label: 'High-end (16GB+ RAM, GPU)', desc: 'Powerful workstation' },
              ].map(option => (
                <label key={option.value} className={styles.radioLabel}>
                  <input
                    type="radio"
                    name="hardware"
                    value={option.value}
                    checked={profile.hardware_tier === option.value}
                    onChange={() => handleProfileChange('hardware_tier', option.value)}
                  />
                  <span className={styles.radioButton}></span>
                  <div>
                    <strong>{option.label}</strong>
                    <small>{option.desc}</small>
                  </div>
                </label>
              ))}
            </div>
          </div>

          <div className={styles.profileSection}>
            <h2>Learning Goals</h2>
            <div className={styles.chipGroup}>
              {goalOptions.map(goal => (
                <button
                  key={goal}
                  type="button"
                  className={`${styles.chip} ${profile.goals.includes(goal) ? styles.chipActive : ''}`}
                  onClick={() => toggleArrayItem('goals', goal)}
                >
                  {goal}
                </button>
              ))}
            </div>
          </div>

          <button onClick={handleProfileSave} className={styles.saveButton}>
            Save Profile
          </button>

          <button
            onClick={() => setIsLoggedIn(false)}
            className={styles.signOutButton}
          >
            Sign Out
          </button>
        </div>
      </div>
    </Layout>
  );
}

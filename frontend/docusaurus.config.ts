import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'AI-Powered Learning',
  tagline: 'Master AI Development with Personalized, Interactive Learning',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  // Updated for Vercel deployment
  url: 'https://your-frontend.vercel.app',
  baseUrl: '/',
  trailingSlash: false,

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  // Custom scripts for chatbot
  scripts: [],

  // Custom fields for API endpoints - now configurable via environment
  customFields: {
    apiBaseUrl: process.env.API_BASE_URL || 'https://your-backend.vercel.app/api',
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: 'book',
          editUrl: 'https://github.com/your-username/giaic-hackathon/tree/main/frontend/',
          showLastUpdateTime: true,
          showLastUpdateAuthor: true,
        },
        blog: false, // Disable blog
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/social-card.jpg',
    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    docs: {
      sidebar: {
        hideable: true,
        autoCollapseCategories: true,
      },
    },
    navbar: {
      title: 'AI-Powered Learning',
      logo: {
        alt: 'AI Book Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'bookSidebar',
          position: 'left',
          label: '📚 Book',
        },
        {
          to: '/profile',
          label: '👤 Profile',
          position: 'left',
        },
        {
          href: 'https://github.com/your-username/giaic-hackathon',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Learn',
          items: [
            {
              label: 'Start Learning',
              to: '/book/intro',
            },
            {
              label: 'Chapter 1: Foundations',
              to: '/book/chapter-1/overview',
            },
          ],
        },
        {
          title: 'Features',
          items: [
            {
              label: 'AI Chatbot',
              to: '/book/intro#chatbot',
            },
            {
              label: 'Personalization',
              to: '/book/intro#personalization',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/your-username/giaic-hackathon',
            },
            {
              label: 'Spec-Kit Plus',
              href: 'https://github.com/panaversity/spec-kit-plus',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} AI-Powered Learning Platform. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'bash', 'json', 'typescript', 'sql'],
    },
    tableOfContents: {
      minHeadingLevel: 2,
      maxHeadingLevel: 4,
    },
  } satisfies Preset.ThemeConfig,

  plugins: [
    // Add any custom plugins here
  ],
};

export default config;
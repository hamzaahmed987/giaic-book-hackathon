import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  bookSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Chapter 1: AI Foundations',
      collapsed: false,
      items: [
        'chapter-1/overview',
        'chapter-1/concepts',
        'chapter-1/examples',
        'chapter-1/exercises',
        'chapter-1/summary',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 2: LLM Fundamentals',
      collapsed: true,
      items: [
        'chapter-2/overview',
        'chapter-2/concepts',
        'chapter-2/examples',
        'chapter-2/exercises',
        'chapter-2/summary',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 3: Prompt Engineering',
      collapsed: true,
      items: [
        'chapter-3/overview',
        'chapter-3/concepts',
        'chapter-3/examples',
        'chapter-3/exercises',
        'chapter-3/summary',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 4: RAG Systems',
      collapsed: true,
      items: [
        'chapter-4/overview',
        'chapter-4/concepts',
        'chapter-4/examples',
        'chapter-4/exercises',
        'chapter-4/summary',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 5: AI Agents',
      collapsed: true,
      items: [
        'chapter-5/overview',
        'chapter-5/concepts',
        'chapter-5/examples',
        'chapter-5/exercises',
        'chapter-5/summary',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 6: Building AI Applications',
      collapsed: true,
      items: [
        'chapter-6/overview',
        'chapter-6/concepts',
        'chapter-6/examples',
        'chapter-6/exercises',
        'chapter-6/summary',
      ],
    },
  ],
};

export default sidebars;

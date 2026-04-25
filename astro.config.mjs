import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

const cat = (label, directory) => ({
  label,
  collapsed: true,
  autogenerate: { directory },
});

export default defineConfig({
  site: 'https://ungovernable.tech',
  integrations: [
    starlight({
      title: 'ungovernable.tech',
      description:
        'A knowledge base of building blocks for a freer internet — confidential computing, cryptography, decentralized infrastructure, and more.',
      logo: { src: './src/assets/logo.svg', replacesTitle: false },
      favicon: '/favicon.svg',
      customCss: ['./src/styles/custom.css'],
      tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 3 },
      pagination: true,
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/aljazceru/ungovernable.tech' },
      ],
      head: [
        {
          tag: 'link',
          attrs: { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        },
        {
          tag: 'link',
          attrs: { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        },
        {
          tag: 'link',
          attrs: {
            rel: 'stylesheet',
            href: 'https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT,WONK@9..144,300..700,0..100,0..1&family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap',
          },
        },
        {
          tag: 'script',
          attrs: {
            defer: true,
            'data-domain': 'ungovernable.tech',
            src: 'https://analytics.cypherpunk.cloud/js/script.js',
          },
        },
      ],
      sidebar: [
        cat('Confidential Computing', 'confidential-computing'),
        cat('Cryptography', 'cryptography'),
        cat('Decentralized DNS', 'decentralized-dns'),
        cat('Decentralized Compute', 'decentralized-compute'),
        cat('Off-Grid Networks', 'off-grid-networks'),
        cat('Financial Sovereignty', 'financial-sovereignty'),
        cat('Encrypted Messaging', 'encrypted-messaging'),
        cat('Mix Networks', 'mix-networks'),
        cat('Zero Knowledge', 'zero-knowledge'),
        cat('Post-Quantum', 'post-quantum'),
        cat('Identity', 'identity'),
        cat('Meta', 'meta'),
      ],
    }),
  ],
});

import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://ungovernable.tech',
  integrations: [
    starlight({
      title: 'Ungovernable.tech',
      description:
        'A knowledge base of building blocks for a freer internet — confidential computing, cryptography, decentralized infrastructure, and more.',
      logo: { src: './src/assets/logo.svg' },
      favicon: '/favicon.svg',
      customCss: ['./src/styles/custom.css'],
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/aljazceru/ungovernable.tech' },
      ],
      head: [
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
        { label: 'Start here', link: '/' },
        { label: 'Confidential Computing', autogenerate: { directory: 'confidential-computing' } },
        { label: 'Cryptography', autogenerate: { directory: 'cryptography' } },
        { label: 'Decentralized DNS', autogenerate: { directory: 'decentralized-dns' } },
        { label: 'Decentralized Compute', autogenerate: { directory: 'decentralized-compute' } },
        { label: 'Off-Grid Networks', autogenerate: { directory: 'off-grid-networks' } },
        { label: 'Financial Sovereignty', autogenerate: { directory: 'financial-sovereignty' } },
        { label: 'Encrypted Messaging', autogenerate: { directory: 'encrypted-messaging' } },
        { label: 'Mix Networks', autogenerate: { directory: 'mix-networks' } },
        { label: 'Zero Knowledge', autogenerate: { directory: 'zero-knowledge' } },
        { label: 'Post-Quantum', autogenerate: { directory: 'post-quantum' } },
        { label: 'Identity', autogenerate: { directory: 'identity' } },
        { label: 'Meta', autogenerate: { directory: 'meta' } },
      ],
    }),
  ],
});

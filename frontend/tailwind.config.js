/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './src/**/*.{vue,js,ts}',
    '../templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        // Base palette
        bg: 'var(--bg)',
        surface: 'var(--surface)',
        ink: 'var(--ink)',
        muted: 'var(--muted)',
        line: 'var(--line)',
        accent: 'var(--accent)',
        'accent-ink': 'var(--accent-ink)',
      },
      fontFamily: {
        sans: ['Arial', 'Helvetica', 'sans-serif'],
      },
      fontSize: {
        'eyebrow': ['0.875rem', { lineHeight: '1.25rem', fontWeight: '600' }],
        'lead': ['1.125rem', { lineHeight: '1.75rem' }],
      },
      boxShadow: {
        'app': '0 12px 30px rgba(18, 30, 42, 0.08)',
        'subtle': '0 2px 14px rgba(18, 30, 42, 0.05)',
      },
      spacing: {
        'gutter': '1rem',
        'section': '2rem',
      },
      borderRadius: {
        'sm': '4px',
        'md': '6px',
        'lg': '8px',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}

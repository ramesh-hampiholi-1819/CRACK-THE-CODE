document.addEventListener('DOMContentLoaded', function () {
  const root = document.documentElement;
  const themeSelector = document.querySelector('[data-theme-select]');
  const accentSelector = document.querySelector('[data-accent-select]');

  const getStoredTheme = () => localStorage.getItem('theme') || 'system';
  const getStoredAccent = () => localStorage.getItem('accentColor') || '#7854f7';

  const DEFAULT_ACCENT = '#7854f7';

  const applyTheme = (theme) => {
    const resolved = theme === 'system'
      ? (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
      : theme;
    root.setAttribute('data-theme', resolved);
    if (themeSelector) themeSelector.value = theme;
  };

  const applyAccent = (accent) => {
    const value = accent || DEFAULT_ACCENT;
    root.style.setProperty('--accent', value);
    root.style.setProperty('--accent-strong', value);
    root.style.setProperty('--accent-soft', `${value}22`);
    if (accentSelector) accentSelector.value = value;
  };

  applyTheme(getStoredTheme());
  applyAccent(getStoredAccent());

  if (themeSelector) {
    themeSelector.addEventListener('change', function () {
      const theme = this.value;
      localStorage.setItem('theme', theme);
      applyTheme(theme);
    });
  }

  if (accentSelector) {
    accentSelector.addEventListener('input', function () {
      const accent = this.value;
      localStorage.setItem('accentColor', accent);
      applyAccent(accent);
    });
  }

  const resetAccentButton = document.getElementById('reset-accent');
  if (resetAccentButton) {
    resetAccentButton.addEventListener('click', function () {
      localStorage.setItem('accentColor', DEFAULT_ACCENT);
      applyAccent(DEFAULT_ACCENT);
      if (accentSelector) accentSelector.value = DEFAULT_ACCENT;
    });
  }

  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function () {
    const savedTheme = getStoredTheme();
    if (savedTheme === 'system') applyTheme('system');
  });
});

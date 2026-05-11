const API_BASE = localStorage.getItem('api_base') || 'http://localhost:8000';

export async function apiFetch(path, opts = {}) {
  const token = localStorage.getItem('jwt');
  opts.headers = opts.headers || {};
  opts.headers['Content-Type'] = 'application/json';
  if (token) opts.headers['Authorization'] = `Bearer ${token}`;
  const response = await fetch(API_BASE + path, opts);
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed ${response.status}`);
  }
  return response.json();
}

export function saveToken(token) {
  localStorage.setItem('jwt', token);
}

export function logout() {
  localStorage.removeItem('jwt');
  window.location.href = '/frontend/user/login.html';
}

export function getJwt() {
  return localStorage.getItem('jwt');
}

export function requireAuth() {
  if (!getJwt()) {
    window.location.href = '/frontend/user/login.html';
  }
}

export function showMessage(text) {
  alert(text);
}

const themeToggleButton = document.getElementById('theme-toggle');
const themeStorageKey = 'citybus-theme';

function applyTheme(theme) {
  const body = document.body;
  const nextTheme = theme === 'light' ? 'light' : 'dark';
  body.classList.toggle('light-mode', nextTheme === 'light');
  body.dataset.theme = nextTheme;
  if (themeToggleButton) {
    themeToggleButton.textContent = nextTheme === 'light' ? '☀️' : '🌙';
    themeToggleButton.setAttribute('aria-label', `Switch to ${nextTheme === 'light' ? 'dark' : 'light'} mode`);
  }
  localStorage.setItem(themeStorageKey, nextTheme);
}

function loadTheme() {
  const savedTheme = localStorage.getItem(themeStorageKey);
  const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  applyTheme(savedTheme || (systemPrefersDark ? 'dark' : 'light'));
}

if (themeToggleButton) {
  themeToggleButton.addEventListener('click', () => {
    const currentTheme = document.body.dataset.theme === 'light' ? 'light' : 'dark';
    applyTheme(currentTheme === 'light' ? 'dark' : 'light');
  });
}

loadTheme();

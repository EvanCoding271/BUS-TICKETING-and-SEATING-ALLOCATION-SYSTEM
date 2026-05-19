const API_BASE = localStorage.getItem('api_base') || '/api';

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

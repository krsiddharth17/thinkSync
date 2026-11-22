function getApiBaseUrl() {
  const envUrl = import.meta.env.VITE_API_BASE_URL;
  if (!envUrl || envUrl.trim() === '') {
    return '/api';
  }
  let trimmed = envUrl.trim().replace(/\/+$/, '');
  if (!trimmed.endsWith('/api') && !trimmed.startsWith('/')) {
    trimmed = `${trimmed}/api`;
  }
  return trimmed;
}

const API_BASE_URL = getApiBaseUrl();

export function getAuthToken() {
  return localStorage.getItem('thinksync_token');
}

export function setAuthToken(token) {
  if (token) {
    localStorage.setItem('thinksync_token', token);
  } else {
    localStorage.removeItem('thinksync_token');
  }
}

export async function apiRequest(endpoint, options = {}) {
  const token = getAuthToken();
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(options.headers || {}),
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let errorDetail = 'API request failed';
    try {
      const errorJson = await response.json();
      errorDetail = errorJson.detail || errorDetail;
    } catch {
      errorDetail = response.statusText || errorDetail;
    }
    throw new Error(errorDetail);
  }

  return response.json();
}

export const authApi = {
  login: (username, password) =>
    apiRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    }),
  register: (userData) =>
    apiRequest('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    }),
  getMe: () => apiRequest('/auth/me'),
};

export const topicsApi = {
  list: () => apiRequest('/topics'),
  get: (slug) => apiRequest(`/topics/${slug}`),
  getQuestions: (slug, difficulty) => {
    const query = difficulty ? `?difficulty=${difficulty}` : '';
    return apiRequest(`/topics/${slug}/questions${query}`);
  },
};

export const assessmentApi = {
  evaluate: (payload) =>
    apiRequest('/assessment/evaluate', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  requestHint: (payload) =>
    apiRequest('/assessment/hint', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
};

export const studentApi = {
  getDashboard: () => apiRequest('/student/dashboard'),
};

export const teacherApi = {
  getDashboard: () => apiRequest('/teacher/dashboard'),
};

export const mlApi = {
  predict: (payload) =>
    apiRequest('/ml/predict', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
  getMetrics: () => apiRequest('/ml/metrics'),
};

export const systemApi = {
  getHealth: () => apiRequest('/health'),
};

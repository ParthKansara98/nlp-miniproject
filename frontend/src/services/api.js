/**
 * API service for communicating with the backend
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API functions

/**
 * Translate Gujarati text to English
 */
export const translateText = async (text, sourceLang = 'gu', targetLang = 'en') => {
  try {
    const response = await api.post('/translate', {
      text,
      source_lang: sourceLang,
      target_lang: targetLang,
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Translation failed');
  }
};

/**
 * Summarize English text
 */
export const summarizeText = async (text, maxLength = 150, minLength = 50) => {
  try {
    const response = await api.post('/summarize', {
      text,
      max_length: maxLength,
      min_length: minLength,
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Summarization failed');
  }
};

/**
 * Process content (extract from URL, translate, and/or summarize)
 */
export const processContent = async (inputType, content, translate = true, summarize = true) => {
  try {
    const response = await api.post('/process', {
      inputType: inputType,
      content,
      translate,
      summarize,
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Processing failed');
  }
};

/**
 * Get application statistics
 */
export const getStatistics = async () => {
  try {
    const response = await api.get('/stats');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch statistics');
  }
};

/**
 * Get recent activity
 */
export const getRecentActivity = async (limit = 10) => {
  try {
    const response = await api.get(`/recent-activity?limit=${limit}`);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch recent activity');
  }
};

/**
 * Get model information
 */
export const getModelInfo = async () => {
  try {
    const response = await api.get('/models');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch model info');
  }
};

/**
 * Health check
 */
export const healthCheck = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Health check failed');
  }
};

// Export the axios instance for direct use if needed
export default api;
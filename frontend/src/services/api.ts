import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
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
    
    if (error.code === 'ECONNABORTED') {
      throw new Error('Request timeout. Please try again.');
    }
    
    if (error.response?.status === 500) {
      throw new Error('Server error. Please try again later.');
    }
    
    if (error.response?.status === 400) {
      throw new Error(error.response.data.detail || 'Invalid request data.');
    }
    
    throw new Error(error.message || 'An unexpected error occurred.');
  }
);

export const predictFatigue = async (behavioralData: any) => {
  try {
    const response = await api.post('/predict', behavioralData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getModelInfo = async () => {
  try {
    const response = await api.get('/model-info');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getModelMetrics = async () => {
  try {
    const response = await api.get('/model-metrics');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getFeatureImportance = async () => {
  try {
    const response = await api.get('/feature-importance');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export default api;

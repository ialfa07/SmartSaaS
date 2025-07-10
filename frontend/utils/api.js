import axios from 'axios'

// Configuration dynamique de l'URL de base
const getAPIBaseURL = () => {
  if (typeof window !== 'undefined') {
    // Côté client
    const hostname = window.location.hostname;

    if (hostname.includes('.replit.app') || hostname.includes('.replit.dev')) {
      // URL Replit publique
      return `https://${hostname.replace('-3000', '-8000')}`;
    } else if (hostname === 'localhost') {
      // Développement local
      return 'http://localhost:8000';
    } else {
      // Domaine personnalisé
      return `https://${hostname}:8000`;
    }
  }

  // Côté serveur (fallback)
  return 'http://localhost:8000';
};

const API_BASE_URL = getAPIBaseURL();

// Instance axios avec configuration par défaut
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour ajouter le token d'authentification
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Intercepteur pour gérer les erreurs
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/auth';
    }
    return Promise.reject(error);
  }
);

export default api;

// Fonctions API spécifiques
export const authAPI = {
  register: (email, password) => api.post('/auth/register', { email, password }),
  login: (email, password) => api.post('/auth/login', { email, password }),
  getUserInfo: () => api.get('/user-info'),
}

export const contentAPI = {
  generateText: (prompt) => api.post('/generate', { prompt }),
  generateImage: (prompt, size = '1024x1024', quality = 'standard') => 
    api.post('/generate-image', { prompt, size, quality }),
  generateMarketing: (businessType, targetAudience, platform) =>
    api.post('/generate-marketing-content', { 
      business_type: businessType, 
      target_audience: targetAudience, 
      platform 
    }),
  generateCalendar: (businessType, durationDays = 30) =>
    api.post('/generate-calendar', { 
      business_type: businessType, 
      duration_days: durationDays 
    }),
}

export const tokensAPI = {
  getBalance: () => api.get('/tokens/balance'),
  claimDailyReward: () => api.post('/tokens/daily-reward'),
  getReferralData: () => api.get('/tokens/referral'),
  referUser: (email) => api.post('/tokens/refer', { referred_email: email }),
  getLeaderboard: () => api.get('/tokens/leaderboard'),
  exchangeForCredits: (amount) => api.post('/tokens/exchange', null, { params: { amount } }),
}

export const web3API = {
  getNetworkInfo: () => api.get('/web3/network-info'),
  connectWallet: (walletAddress, signature) => 
    api.post('/web3/connect-wallet', { wallet_address: walletAddress, signature }),
  syncTokens: () => api.post('/web3/sync-tokens'),
  getWalletBalance: (address) => api.get(`/web3/wallet/${address}`),
}

export const paymentsAPI = {
  getPlans: () => api.get('/plans'),
  createCheckout: (planId) => api.post('/create-checkout', { plan_id: planId }),
  verifyPayment: (sessionId) => api.post('/verify-payment', null, { params: { session_id: sessionId } }),
}

import axios from 'axios'

const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-repl-url.replit.app' 
  : 'http://localhost:8000'

// Instance axios avec configuration par défaut
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Intercepteur pour ajouter le token d'authentification
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Intercepteur pour gérer les erreurs d'authentification
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api

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

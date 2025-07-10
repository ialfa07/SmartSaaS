
import { createContext, useContext, useState, useEffect } from 'react'
import { authAPI } from '../utils/api'
import toast from 'react-hot-toast'

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  useEffect(() => {
    checkAuthStatus()
  }, [])

  const checkAuthStatus = async () => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      setLoading(false)
      return
    }

    try {
      const response = await authAPI.getUserInfo()
      setUser(response.data)
      setIsAuthenticated(true)
    } catch (error) {
      localStorage.removeItem('access_token')
      setIsAuthenticated(false)
    } finally {
      setLoading(false)
    }
  }

  const login = async (email, password) => {
    try {
      const response = await authAPI.login(email, password)
      const { access_token, user: userData } = response.data
      
      localStorage.setItem('access_token', access_token)
      setUser(userData)
      setIsAuthenticated(true)
      
      toast.success('Connexion réussie !')
      return { success: true }
    } catch (error) {
      const message = error.response?.data?.detail || 'Erreur de connexion'
      toast.error(message)
      return { success: false, error: message }
    }
  }

  const register = async (email, password) => {
    try {
      const response = await authAPI.register(email, password)
      const { access_token, user: userData } = response.data
      
      localStorage.setItem('access_token', access_token)
      setUser(userData)
      setIsAuthenticated(true)
      
      toast.success('Inscription réussie ! Bienvenue !')
      return { success: true }
    } catch (error) {
      const message = error.response?.data?.detail || 'Erreur lors de l\'inscription'
      toast.error(message)
      return { success: false, error: message }
    }
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    setUser(null)
    setIsAuthenticated(false)
    toast.success('Déconnexion réussie')
  }

  const updateUserCredits = (newCredits) => {
    setUser(prev => ({ ...prev, credits: newCredits }))
  }

  const value = {
    user,
    loading,
    isAuthenticated,
    login,
    register,
    logout,
    updateUserCredits,
    checkAuthStatus
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

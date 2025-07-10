
import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import axios from 'axios'

const PricingPage = () => {
  const [plans, setPlans] = useState({})
  const [loading, setLoading] = useState(false)
  const [selectedPlan, setSelectedPlan] = useState(null)

  useEffect(() => {
    fetchPlans()
  }, [])

  const fetchPlans = async () => {
    try {
      const response = await axios.get('http://localhost:8000/plans')
      setPlans(response.data.plans)
    } catch (error) {
      console.error('Erreur lors du chargement des plans:', error)
    }
  }

  const handleSubscribe = async (planId) => {
    setLoading(true)
    setSelectedPlan(planId)
    
    try {
      const response = await axios.post('http://localhost:8000/create-checkout', {
        plan_id: planId
      })
      
      // Rediriger vers Stripe Checkout
      window.location.href = response.data.checkout_url
    } catch (error) {
      console.error('Erreur lors de la création du checkout:', error)
      alert('Erreur lors de la création du paiement')
    } finally {
      setLoading(false)
      setSelectedPlan(null)
    }
  }

  const planOrder = ['starter', 'pro', 'premium']

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-12 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <motion.h1 
            className="text-5xl font-bold text-gray-900 mb-4"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            Choisissez votre plan
          </motion.h1>
          <motion.p 
            className="text-xl text-gray-600 max-w-2xl mx-auto"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            Accédez à toutes les fonctionnalités IA pour booster votre marketing
          </motion.p>
        </div>

        {/* Plans */}
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {planOrder.map((planId, index) => {
            const plan = plans[planId]
            if (!plan) return null
            
            const isPopular = planId === 'pro'
            
            return (
              <motion.div
                key={planId}
                className={`relative bg-white rounded-2xl shadow-xl overflow-hidden ${
                  isPopular ? 'ring-4 ring-blue-500 scale-105' : ''
                }`}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
              >
                {isPopular && (
                  <div className="absolute top-0 left-0 right-0 bg-gradient-to-r from-blue-600 to-purple-600 text-white text-center py-2 text-sm font-medium">
                    ⭐ Plus populaire
                  </div>
                )}
                
                <div className={`p-8 ${isPopular ? 'pt-16' : ''}`}>
                  <div className="text-center mb-8">
                    <h3 className="text-2xl font-bold text-gray-900 mb-2">
                      {plan.name}
                    </h3>
                    <div className="text-4xl font-bold text-gray-900 mb-2">
                      {plan.price}€
                      <span className="text-lg font-normal text-gray-600">/mois</span>
                    </div>
                    <p className="text-gray-600">
                      {plan.credits} crédits inclus
                    </p>
                  </div>
                  
                  <ul className="space-y-3 mb-8">
                    {plan.features.map((feature, featureIndex) => (
                      <li key={featureIndex} className="flex items-center">
                        <svg className="w-5 h-5 text-green-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                        <span className="text-gray-700">{feature}</span>
                      </li>
                    ))}
                  </ul>
                  
                  <button
                    onClick={() => handleSubscribe(planId)}
                    disabled={loading && selectedPlan === planId}
                    className={`w-full py-3 px-6 rounded-xl font-semibold text-white transition-all duration-300 ${
                      isPopular
                        ? 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700'
                        : 'bg-gray-900 hover:bg-gray-800'
                    } ${loading && selectedPlan === planId ? 'opacity-50 cursor-not-allowed' : 'transform hover:scale-105'}`}
                  >
                    {loading && selectedPlan === planId ? (
                      <div className="flex items-center justify-center">
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                        Chargement...
                      </div>
                    ) : (
                      'Commencer maintenant'
                    )}
                  </button>
                </div>
              </motion.div>
            )
          })}
        </div>

        {/* Garantie */}
        <motion.div 
          className="text-center mt-16"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.8 }}
        >
          <div className="inline-flex items-center bg-green-50 rounded-full px-6 py-3">
            <svg className="w-6 h-6 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            <span className="text-green-700 font-medium">
              Satisfait ou remboursé sous 30 jours
            </span>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default PricingPage

import { useState, useEffect } from 'react'
import { useRouter } from 'next/router'
import axios from 'axios'

export default function Success() {
  const router = useRouter()
  const [loading, setLoading] = useState(true)
  const [paymentStatus, setPaymentStatus] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    const verifyPayment = async () => {
      const { session_id } = router.query

      if (session_id) {
        try {
          const response = await axios.post('http://localhost:8000/verify-payment', {
            session_id
          })
          setPaymentStatus(response.data)
        } catch (err) {
          setError('Erreur lors de la vérification du paiement')
          console.error(err)
        } finally {
          setLoading(false)
        }
      }
    }

    if (router.isReady) {
      verifyPayment()
    }
  }, [router.isReady, router.query])

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-green-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Vérification du paiement...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-red-50 to-pink-50 flex items-center justify-center">
        <div className="bg-white rounded-2xl p-8 shadow-xl text-center max-w-md">
          <div className="text-6xl mb-4">❌</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Erreur</h1>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={() => router.push('/pricing')}
            className="bg-red-600 text-white px-6 py-3 rounded-lg hover:bg-red-700 transition"
          >
            Retourner aux plans
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 flex items-center justify-center">
      <div className="bg-white rounded-2xl p-8 shadow-xl text-center max-w-md">
        <div className="text-6xl mb-4">🎉</div>
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Paiement réussi !
        </h1>
        <p className="text-gray-600 mb-6">
          Votre abonnement a été activé avec succès.
        </p>

        {paymentStatus && (
          <div className="bg-green-50 rounded-lg p-4 mb-6">
            <div className="text-left">
              <p className="font-semibold text-green-800">
                Nouveaux crédits : +{paymentStatus.credits}
              </p>
              <p className="text-green-700">
                Crédits totaux : {paymentStatus.credits}
              </p>
            </div>
          </div>
        )}

        <div className="space-y-3">
          <button
            onClick={() => router.push('/')}
            className="w-full bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition"
          >
            Accéder au tableau de bord
          </button>
          <button
            onClick={() => router.push('/pricing')}
            className="w-full bg-gray-200 text-gray-800 px-6 py-3 rounded-lg hover:bg-gray-300 transition"
          >
            Voir d'autres plans
          </button>
        </div>
      </div>
    </div>
  )
}
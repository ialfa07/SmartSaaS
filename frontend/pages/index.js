
import { useState, useEffect } from 'react'
import axios from 'axios'

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('generate')
  const [prompt, setPrompt] = useState("")
  const [response, setResponse] = useState("")
  const [loading, setLoading] = useState(false)
  const [credits, setCredits] = useState(5)
  const [isDark, setIsDark] = useState(false)

  const handleGenerate = async () => {
    setLoading(true)
    try {
      const res = await axios.post("http://localhost:8000/generate", {
        prompt: prompt
      })
      setResponse(res.data.result)
      setCredits(res.data.credits_left)
    } catch (error) {
      console.error(error)
      setResponse("Erreur lors de la génération.")
    } finally {
      setLoading(false)
    }
  }

  const sidebarItems = [
    { id: 'generate', icon: '🤖', label: 'Générateur IA', desc: 'Créez du contenu avec IA' },
    { id: 'images', icon: '🎨', label: 'Images IA', desc: 'Générez des visuels' },
    { id: 'calendar', icon: '📅', label: 'Planificateur', desc: 'Programmez vos posts' },
    { id: 'social', icon: '📱', label: 'Réseaux sociaux', desc: 'Gérez vos comptes' },
    { id: 'email', icon: '✉️', label: 'Email Marketing', desc: 'Campagnes automatisées' },
    { id: 'analytics', icon: '📊', label: 'Analytics', desc: 'Analysez vos performances' },
    { id: 'tokens', icon: '🪙', label: 'Tokens SaaS', desc: 'Gérez vos jetons' },
    { id: 'referral', icon: '👥', label: 'Parrainage', desc: 'Invitez des amis' },
    { id: 'settings', icon: '⚙️', label: 'Paramètres', desc: 'Configuration' },
  ]

  const renderContent = () => {
    switch(activeTab) {
      case 'generate':
        return (
          <div className="space-y-6">
            <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg">
              <h2 className="text-2xl font-bold mb-4 text-gray-800 dark:text-white">
                🤖 Générateur de contenu IA
              </h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Décrivez ce que vous voulez créer
                  </label>
                  <textarea
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    className="w-full p-4 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    rows={4}
                    placeholder="Ex: Écris un post LinkedIn sur les tendances marketing 2024..."
                  />
                </div>
                <button
                  onClick={handleGenerate}
                  disabled={loading || credits <= 0}
                  className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-lg font-semibold transition-all duration-300 hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105"
                >
                  {loading ? (
                    <div className="flex items-center justify-center">
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                      Génération en cours...
                    </div>
                  ) : (
                    `Générer (${credits} crédits restants)`
                  )}
                </button>
              </div>
            </div>
            
            {response && (
              <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg animate-fadeIn">
                <h3 className="text-lg font-semibold mb-4 text-gray-800 dark:text-white">
                  ✨ Résultat généré
                </h3>
                <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                  <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">{response}</p>
                </div>
                <div className="mt-4 flex gap-2">
                  <button className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors">
                    📋 Copier
                  </button>
                  <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                    📤 Partager
                  </button>
                </div>
              </div>
            )}
          </div>
        )
      
      default:
        return (
          <div className="bg-white dark:bg-gray-800 rounded-xl p-8 shadow-lg text-center">
            <div className="text-6xl mb-4">{sidebarItems.find(item => item.id === activeTab)?.icon}</div>
            <h2 className="text-2xl font-bold mb-2 text-gray-800 dark:text-white">
              {sidebarItems.find(item => item.id === activeTab)?.label}
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              Cette fonctionnalité sera bientôt disponible !
            </p>
            <div className="bg-gradient-to-r from-blue-100 to-purple-100 dark:from-blue-900 dark:to-purple-900 p-4 rounded-lg">
              <p className="text-sm text-gray-700 dark:text-gray-300">
                🚀 En développement - Restez connecté pour les mises à jour !
              </p>
            </div>
          </div>
        )
    }
  }

  return (
    <div className={`min-h-screen ${isDark ? 'dark' : ''}`}>
      <div className="bg-gray-50 dark:bg-gray-900 min-h-screen flex">
        {/* Sidebar */}
        <div className="w-64 bg-white dark:bg-gray-800 shadow-xl border-r border-gray-200 dark:border-gray-700">
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              SmartSaaS
            </h1>
            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
              Plateforme Marketing IA
            </p>
          </div>
          
          <nav className="mt-6 px-3">
            {sidebarItems.map((item) => (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center px-3 py-3 mb-2 rounded-lg transition-all duration-200 ${
                  activeTab === item.id
                    ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg'
                    : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}
              >
                <span className="text-2xl mr-3">{item.icon}</span>
                <div className="text-left">
                  <div className="font-medium">{item.label}</div>
                  <div className="text-xs opacity-75">{item.desc}</div>
                </div>
              </button>
            ))}
          </nav>
        </div>

        {/* Main Content */}
        <div className="flex-1 flex flex-col">
          {/* Header */}
          <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 px-6 py-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold text-gray-800 dark:text-white">
                  {sidebarItems.find(item => item.id === activeTab)?.label}
                </h2>
                <p className="text-gray-600 dark:text-gray-400">
                  {sidebarItems.find(item => item.id === activeTab)?.desc}
                </p>
              </div>
              
              <div className="flex items-center gap-4">
                <div className="bg-gradient-to-r from-green-500 to-blue-500 text-white px-4 py-2 rounded-lg">
                  💳 {credits} crédits
                </div>
                <button
                  onClick={() => setIsDark(!isDark)}
                  className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                >
                  {isDark ? '☀️' : '🌙'}
                </button>
                <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold">
                  U
                </div>
              </div>
            </div>
          </header>

          {/* Content Area */}
          <main className="flex-1 p-6">
            {renderContent()}
          </main>
        </div>
      </div>
    </div>
  )
}

export default Dashboard

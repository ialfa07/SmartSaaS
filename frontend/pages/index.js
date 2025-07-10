import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { useRouter } from 'next/router'

export default function Home() {
  const { user, logout } = useAuth()
  const router = useRouter()
  const [activeSection, setActiveSection] = useState('generate')
  const [isDark, setIsDark] = useState(true)
  const [currentTheme, setCurrentTheme] = useState('cyberpunk')
  const [sidebarOpen, setSidebarOpen] = useState(true)

  // Thèmes disponibles
  const themes = {
    cyberpunk: { name: 'Cyberpunk Dark', emoji: '🌆', desc: 'Futuriste et néon' },
    minimal: { name: 'Minimal Light', emoji: '☀️', desc: 'Épuré et moderne' },
    ocean: { name: 'Ocean Blue', emoji: '🌊', desc: 'Profondeur marine' },
    forest: { name: 'Forest Green', emoji: '🌲', desc: 'Nature et zen' },
    sunset: { name: 'Sunset Warm', emoji: '🌅', desc: 'Chaleur dorée' },
    galaxy: { name: 'Purple Galaxy', emoji: '🌌', desc: 'Cosmos mystique' }
  }

  useEffect(() => {
    if (!user) {
      router.push('/auth')
    }
  }, [user, router])

  useEffect(() => {
    // Appliquer le thème
    document.documentElement.className = `theme-${currentTheme}`
  }, [currentTheme])

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
    { id: 'billing', icon: '💳', label: 'Facturation', desc: 'Abonnements & paiements' }
  ]

  const renderContent = () => {
    switch(activeSection) {
      case 'generate':
        return (
          <div className="space-y-6">
            <div className="glass-card p-8 floating-animation">
              <h2 className="text-3xl font-bold gradient-text mb-4">🤖 Générateur de Contenu IA</h2>
              <p className="text-lg mb-6 opacity-80">Créez du contenu engageant avec l'intelligence artificielle</p>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div className="card p-6 hover:scale-105 transition-transform pulse-glow">
                  <div className="text-4xl mb-4">📝</div>
                  <h3 className="text-xl font-semibold mb-2">Articles de Blog</h3>
                  <p className="opacity-70">Générez des articles optimisés SEO</p>
                  <button className="mt-4 px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg hover:shadow-lg transition-all">
                    Créer
                  </button>
                </div>

                <div className="card p-6 hover:scale-105 transition-transform pulse-glow">
                  <div className="text-4xl mb-4">📱</div>
                  <h3 className="text-xl font-semibold mb-2">Posts Sociaux</h3>
                  <p className="opacity-70">Contenu viral pour vos réseaux</p>
                  <button className="mt-4 px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg hover:shadow-lg transition-all">
                    Générer
                  </button>
                </div>

                <div className="card p-6 hover:scale-105 transition-transform pulse-glow">
                  <div className="text-4xl mb-4">✉️</div>
                  <h3 className="text-xl font-semibold mb-2">Emails Marketing</h3>
                  <p className="opacity-70">Campagnes qui convertissent</p>
                  <button className="mt-4 px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg hover:shadow-lg transition-all">
                    Lancer
                  </button>
                </div>
              </div>
            </div>
          </div>
        )

      case 'tokens':
        return (
          <div className="space-y-6">
            <div className="glass-card p-8 floating-animation">
              <h2 className="text-3xl font-bold gradient-text mb-4">🪙 Tokens SaaS</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="card p-6 text-center pulse-glow">
                  <div className="text-5xl mb-4">💰</div>
                  <h3 className="text-2xl font-bold">1,250</h3>
                  <p className="opacity-70">Tokens disponibles</p>
                </div>
                <div className="card p-6 text-center pulse-glow">
                  <div className="text-5xl mb-4">🎯</div>
                  <h3 className="text-2xl font-bold">875</h3>
                  <p className="opacity-70">Tokens utilisés</p>
                </div>
                <div className="card p-6 text-center pulse-glow">
                  <div className="text-5xl mb-4">⭐</div>
                  <h3 className="text-2xl font-bold">Niveau 3</h3>
                  <p className="opacity-70">Statut premium</p>
                </div>
              </div>
            </div>
          </div>
        )

      default:
        return (
          <div className="text-center py-20">
            <div className="text-6xl mb-4 floating-animation">🚀</div>
            <h2 className="text-3xl font-bold gradient-text mb-4">Fonctionnalité en développement</h2>
            <p className="text-xl opacity-70">Cette section sera bientôt disponible !</p>
          </div>
        )
    }
  }

  if (!user) {
    return <div className="min-h-screen flex items-center justify-center">
      <div className="spinner"></div>
    </div>
  }

  return (
    <div className={`min-h-screen theme-${currentTheme}`}>
      <div className="bg-gradient-to-br from-gray-900 to-black min-h-screen flex">

        {/* Sidebar */}
        <div className={`${sidebarOpen ? 'w-80' : 'w-20'} transition-all duration-300 bg-gradient-to-b from-gray-800 to-gray-900 border-r border-opacity-20`}>

          {/* Header Sidebar */}
          <div className="p-6 border-b border-opacity-20">
            <div className="flex items-center justify-between">
              <div className={`${sidebarOpen ? 'block' : 'hidden'}`}>
                <h1 className="text-2xl font-bold gradient-text">SmartSaaS</h1>
                <p className="text-sm opacity-60">Marketing IA Platform</p>
              </div>
              <button 
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="p-2 hover:bg-white hover:bg-opacity-10 rounded-lg transition-all"
              >
                {sidebarOpen ? '◀' : '▶'}
              </button>
            </div>
          </div>

          {/* User Info */}
          <div className="p-4 border-b border-opacity-20">
            <div className={`flex items-center space-x-3 ${sidebarOpen ? '' : 'justify-center'}`}>
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                <span className="text-white font-bold">{user.email[0].toUpperCase()}</span>
              </div>
              {sidebarOpen && (
                <div>
                  <p className="font-medium text-sm">{user.email}</p>
                  <p className="text-xs opacity-60">Premium User</p>
                </div>
              )}
            </div>
          </div>

          {/* Navigation */}
          <div className="p-4 space-y-2">
            {sidebarItems.map((item) => (
              <button
                key={item.id}
                onClick={() => setActiveSection(item.id)}
                className={`w-full flex items-center space-x-3 p-3 rounded-lg transition-all hover:bg-white hover:bg-opacity-10 ${
                  activeSection === item.id ? 'bg-white bg-opacity-20 border border-opacity-30' : ''
                } ${sidebarOpen ? 'justify-start' : 'justify-center'}`}
              >
                <span className="text-xl">{item.icon}</span>
                {sidebarOpen && (
                  <div className="text-left">
                    <p className="font-medium text-sm">{item.label}</p>
                    <p className="text-xs opacity-60">{item.desc}</p>
                  </div>
                )}
              </button>
            ))}
          </div>

          {/* Theme Selector */}
          {sidebarOpen && (
            <div className="p-4 border-t border-opacity-20">
              <h3 className="text-sm font-semibold mb-3 opacity-80">🎨 Thèmes</h3>
              <div className="space-y-2">
                {Object.entries(themes).map(([key, theme]) => (
                  <button
                    key={key}
                    onClick={() => setCurrentTheme(key)}
                    className={`w-full flex items-center space-x-2 p-2 rounded text-xs transition-all hover:bg-white hover:bg-opacity-10 ${
                      currentTheme === key ? 'bg-white bg-opacity-20' : ''
                    }`}
                  >
                    <span>{theme.emoji}</span>
                    <div className="text-left">
                      <p className="font-medium">{theme.name}</p>
                      <p className="opacity-60">{theme.desc}</p>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Logout */}
          <div className="absolute bottom-4 left-4 right-4">
            <button 
              onClick={logout}
              className={`w-full flex items-center space-x-3 p-3 rounded-lg bg-red-600 hover:bg-red-700 transition-all ${
                sidebarOpen ? 'justify-start' : 'justify-center'
              }`}
            >
              <span>🚪</span>
              {sidebarOpen && <span className="font-medium">Déconnexion</span>}
            </button>
          </div>
        </div>

        {/* Contenu principal */}
        <div className="flex-1 overflow-auto">
          {/* Header */}
          <div className="p-6 border-b border-opacity-20 bg-gradient-to-r from-transparent to-white to-transparent bg-opacity-5">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold gradient-text">
                  {sidebarItems.find(item => item.id === activeSection)?.label}
                </h1>
                <p className="opacity-70">
                  {sidebarItems.find(item => item.id === activeSection)?.desc}
                </p>
              </div>
              <div className="flex items-center space-x-4">
                <div className="px-4 py-2 bg-gradient-to-r from-green-500 to-blue-600 rounded-full text-sm font-medium">
                  🟢 En ligne
                </div>
                <div className="text-sm opacity-70">
                  {new Date().toLocaleDateString('fr-FR')}
                </div>
              </div>
            </div>
          </div>

          {/* Contenu */}
          <div className="p-6">
            {renderContent()}
          </div>
        </div>
      </div>
    </div>
  )
}
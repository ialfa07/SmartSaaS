
import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import Link from 'next/link'

const themes = [
  {
    name: 'Dark Modern',
    class: 'theme-dark-modern',
    description: 'Sombre et moderne avec des accents bleus/violets',
    preview: { bg: '#0f172a', accent: '#6366f1' }
  },
  {
    name: 'Cyber Neon',
    class: 'theme-cyber-neon', 
    description: 'Style cyberpunk avec des néons verts/roses',
    preview: { bg: '#0a0a0a', accent: '#00ff88' }
  },
  {
    name: 'Sunset Gradient',
    class: 'theme-sunset',
    description: 'Dégradé coucher de soleil orange/violet',
    preview: { bg: '#1e1b4b', accent: '#f97316' }
  },
  {
    name: 'Ocean Deep',
    class: 'theme-ocean',
    description: 'Bleu océan profond avec des tons aquatiques',
    preview: { bg: '#0c4a6e', accent: '#0ea5e9' }
  },
  {
    name: 'Minimalist White',
    class: 'theme-minimal-white',
    description: 'Blanc minimaliste avec touches de couleur',
    preview: { bg: '#ffffff', accent: '#3b82f6' }
  }
]

export default function Home() {
  const [currentTheme, setCurrentTheme] = useState(themes[0])
  const [isAnimating, setIsAnimating] = useState(false)

  const changeTheme = (theme) => {
    setIsAnimating(true)
    setTimeout(() => {
      setCurrentTheme(theme)
      setIsAnimating(false)
    }, 300)
  }

  useEffect(() => {
    // Appliquer le thème au document
    document.documentElement.className = currentTheme.class
  }, [currentTheme])

  return (
    <div className={`theme-container ${currentTheme.class}`}>
      {/* Sélecteur de thème */}
      <div className="theme-toggle">
        <select 
          value={currentTheme.name} 
          onChange={(e) => changeTheme(themes.find(t => t.name === e.target.value))}
          className="theme-input"
          style={{ minWidth: '200px' }}
        >
          {themes.map(theme => (
            <option key={theme.name} value={theme.name}>
              {theme.name}
            </option>
          ))}
        </select>
      </div>

      {/* Navigation */}
      <nav className="theme-nav">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <motion.div 
              className="flex items-center space-x-2"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5 }}
            >
              <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg"></div>
              <h1 className="text-2xl font-bold">SmartSaaS</h1>
            </motion.div>
            
            <div className="flex items-center space-x-6">
              <Link href="/pricing" className="hover:text-blue-400 transition-colors">
                Tarifs
              </Link>
              <Link href="/auth" className="theme-button">
                Connexion
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Section Hero */}
      <section className="theme-hero">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center"
          >
            <h1 className="text-6xl font-bold mb-6">
              Créez du contenu avec
              <span className="bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent block">
                l'Intelligence Artificielle
              </span>
            </h1>
            
            <p className="text-xl mb-8 max-w-3xl mx-auto" style={{ color: 'var(--text-secondary)' }}>
              Générez des textes, images et campagnes marketing automatiquement. 
              Gagnez des jetons SaaS et développez votre business en ligne.
            </p>
            
            <div className="flex justify-center space-x-4">
              <Link href="/auth" className="theme-button text-lg px-8 py-4">
                Commencer Gratuitement
              </Link>
              <button className="theme-button bg-transparent border-2 border-current text-lg px-8 py-4">
                Voir la Démo
              </button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Aperçu des thèmes */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4">Choisissez votre thème</h2>
            <p className="text-xl" style={{ color: 'var(--text-secondary)' }}>
              Personnalisez l'apparence de votre interface
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {themes.map((theme, index) => (
              <motion.div
                key={theme.name}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className={`theme-card cursor-pointer ${currentTheme.name === theme.name ? 'ring-2 ring-blue-500' : ''}`}
                onClick={() => changeTheme(theme)}
              >
                <div className="mb-4">
                  <div 
                    className="w-full h-32 rounded-lg mb-3"
                    style={{ 
                      background: `linear-gradient(135deg, ${theme.preview.bg} 0%, ${theme.preview.accent} 100%)` 
                    }}
                  ></div>
                  <h3 className="text-xl font-semibold mb-2">{theme.name}</h3>
                  <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                    {theme.description}
                  </p>
                </div>
                
                <div className="flex justify-between items-center">
                  <div className="flex space-x-2">
                    <div 
                      className="w-4 h-4 rounded-full" 
                      style={{ backgroundColor: theme.preview.bg }}
                    ></div>
                    <div 
                      className="w-4 h-4 rounded-full" 
                      style={{ backgroundColor: theme.preview.accent }}
                    ></div>
                  </div>
                  
                  {currentTheme.name === theme.name && (
                    <span className="text-sm font-medium text-green-400">✓ Actif</span>
                  )}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Fonctionnalités */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4">Fonctionnalités Puissantes</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                icon: '🤖',
                title: 'IA Générative',
                description: 'Créez du contenu avec GPT-4 et DALL-E'
              },
              {
                icon: '💰',
                title: 'Jetons SaaS',
                description: 'Système de récompenses blockchain'
              },
              {
                icon: '📧',
                title: 'Email Marketing',
                description: 'Automatisation des campagnes'
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.2 }}
                className="theme-stat-card"
              >
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p style={{ color: 'var(--text-secondary)' }}>
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Final */}
      <section className="py-20 text-center">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h2 className="text-4xl font-bold mb-6">
              Prêt à révolutionner votre contenu ?
            </h2>
            <p className="text-xl mb-8" style={{ color: 'var(--text-secondary)' }}>
              Rejoignez des milliers d'entrepreneurs qui utilisent déjà SmartSaaS
            </p>
            <Link href="/auth" className="theme-button text-lg px-8 py-4 animate-pulse">
              Commencer Maintenant
            </Link>
          </motion.div>
        </div>
      </section>
    </div>
  )
}

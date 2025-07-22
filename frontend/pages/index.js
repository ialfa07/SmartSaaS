
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';

export default function Home() {
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    setIsLoaded(true);
  }, []);

  return (
    <div className="min-h-screen" style={{ background: 'var(--bg-primary)' }}>
      {/* Navigation */}
      <nav className="border-b border-gray-700 bg-gray-800/50 backdrop-blur-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <motion.div 
              className="flex items-center space-x-3"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5 }}
            >
              <div className="w-8 h-8 rounded-lg bg-gradient-to-r from-indigo-500 to-purple-600"></div>
              <h1 className="text-xl font-bold text-white">SmartSaaS</h1>
            </motion.div>
            
            <div className="flex items-center space-x-6">
              <Link href="/pricing" className="text-gray-300 hover:text-white transition-colors">
                Tarifs
              </Link>
              <Link href="/auth" className="btn btn-primary">
                Connexion
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <motion.section 
        className="py-20 px-4 text-center"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: isLoaded ? 1 : 0, y: isLoaded ? 0 : 20 }}
        transition={{ duration: 0.8 }}
      >
        <div className="max-w-4xl mx-auto">
          <motion.h1 
            className="text-5xl md:text-6xl font-bold mb-6"
            style={{ color: 'var(--text-primary)' }}
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.8 }}
          >
            Le Marketing.{' '}
            <span className="text-gradient">
              Réinventé par l'IA.
            </span>
          </motion.h1>
          
          <motion.p 
            className="text-xl mb-8 max-w-2xl mx-auto"
            style={{ color: 'var(--text-secondary)' }}
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.8 }}
          >
            Générez du contenu marketing intelligent, automatisez vos campagnes 
            et gagnez des récompenses crypto. Tout-en-un.
          </motion.p>
          
          <motion.div 
            className="flex flex-col sm:flex-row gap-4 justify-center items-center"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 0.8 }}
          >
            <Link href="/auth" className="btn btn-primary text-lg px-8 py-4">
              Commencer Gratuitement
            </Link>
            <Link href="/pricing" className="btn btn-secondary text-lg px-8 py-4">
              Voir les Prix
            </Link>
          </motion.div>
        </div>
      </motion.section>

      {/* Features Section */}
      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <motion.div 
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8, duration: 0.6 }}
          >
            <h2 className="text-4xl font-bold mb-4" style={{ color: 'var(--text-primary)' }}>
              Tout ce dont vous avez besoin
            </h2>
            <p className="text-xl" style={{ color: 'var(--text-secondary)' }}>
              Une plateforme complète pour révolutionner votre marketing
            </p>
          </motion.div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                title: "Génération IA",
                description: "Créez du contenu marketing avec GPT-4 et DALL-E",
                icon: "🤖",
                gradient: "from-blue-500 to-cyan-500"
              },
              {
                title: "Système de Récompenses",
                description: "Gagnez des jetons SaaS pour chaque action",
                icon: "💰",
                gradient: "from-yellow-500 to-orange-500"
              },
              {
                title: "Automatisation",
                description: "Campagnes emails et posts automatiques",
                icon: "⚡",
                gradient: "from-purple-500 to-pink-500"
              },
              {
                title: "Multi-Plateformes",
                description: "Optimisé pour LinkedIn, Instagram, Twitter",
                icon: "📱",
                gradient: "from-green-500 to-emerald-500"
              },
              {
                title: "Parrainage",
                description: "Invitez vos amis et gagnez plus de jetons",
                icon: "🎯",
                gradient: "from-indigo-500 to-purple-500"
              },
              {
                title: "Analytics",
                description: "Suivez vos performances en temps réel",
                icon: "📊",
                gradient: "from-rose-500 to-red-500"
              }
            ].map((feature, index) => (
              <motion.div
                key={feature.title}
                className="card card-highlight p-6"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1 + index * 0.1, duration: 0.6 }}
              >
                <div className={`text-4xl mb-4 w-16 h-16 rounded-lg bg-gradient-to-r ${feature.gradient} flex items-center justify-center`}>
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold mb-3" style={{ color: 'var(--text-primary)' }}>
                  {feature.title}
                </h3>
                <p style={{ color: 'var(--text-secondary)' }}>
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="card glass p-12 text-center">
            <motion.h2 
              className="text-3xl font-bold mb-8"
              style={{ color: 'var(--text-primary)' }}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1.5, duration: 0.6 }}
            >
              Rejoignez la révolution IA
            </motion.h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {[
                { number: "10K+", label: "Contenus générés" },
                { number: "500+", label: "Utilisateurs actifs" },
                { number: "1M+", label: "Jetons distribués" }
              ].map((stat, index) => (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 1.7 + index * 0.2, duration: 0.6 }}
                >
                  <div className="widget-stat text-gradient">{stat.number}</div>
                  <p style={{ color: 'var(--text-secondary)' }}>{stat.label}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <motion.div 
          className="max-w-3xl mx-auto text-center"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 2, duration: 0.6 }}
        >
          <h2 className="text-4xl font-bold mb-6" style={{ color: 'var(--text-primary)' }}>
            Prêt à révolutionner votre marketing ?
          </h2>
          <p className="text-xl mb-8" style={{ color: 'var(--text-secondary)' }}>
            Commencez gratuitement et découvrez la puissance de l'IA
          </p>
          <Link href="/auth" className="btn btn-success text-lg px-12 py-4">
            Démarrer Maintenant
          </Link>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-700 py-12">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <div className="flex items-center justify-center space-x-3 mb-4">
            <div className="w-6 h-6 rounded bg-gradient-to-r from-indigo-500 to-purple-600"></div>
            <span className="font-semibold" style={{ color: 'var(--text-primary)' }}>
              SmartSaaS
            </span>
          </div>
          <p style={{ color: 'var(--text-secondary)' }}>
            © 2024 SmartSaaS. Le futur du marketing intelligent.
          </p>
        </div>
      </footer>
    </div>
  );
}

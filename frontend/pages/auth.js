
import { useState } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { useAuth } from '../contexts/AuthContext';

export default function Auth() {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: ''
  });
  const [loading, setLoading] = useState(false);
  const { login, register } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      if (isLogin) {
        await login(formData.email, formData.password);
      } else {
        await register(formData.name, formData.email, formData.password);
      }
    } catch (error) {
      console.error('Erreur auth:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex" style={{ background: 'var(--bg-primary)' }}>
      {/* Colonne de gauche - Visuel */}
      <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-600 via-purple-600 to-cyan-600"></div>
        
        {/* Animation de particules/ondes */}
        <div className="absolute inset-0">
          {Array.from({ length: 50 }).map((_, i) => (
            <motion.div
              key={i}
              className="absolute w-2 h-2 bg-white rounded-full opacity-20"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
              }}
              animate={{
                y: [0, -30, 0],
                opacity: [0.2, 0.8, 0.2],
              }}
              transition={{
                duration: 3 + Math.random() * 2,
                repeat: Infinity,
                delay: Math.random() * 2,
              }}
            />
          ))}
        </div>
        
        {/* Contenu de la colonne gauche */}
        <div className="relative z-10 flex flex-col justify-center px-12 text-white">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <div className="flex items-center space-x-3 mb-8">
              <div className="w-12 h-12 rounded-xl bg-white/20 backdrop-blur-sm flex items-center justify-center">
                <span className="text-2xl">🚀</span>
              </div>
              <h1 className="text-3xl font-bold">SmartSaaS</h1>
            </div>
            
            <h2 className="text-4xl font-bold mb-6">
              Le Marketing.
              <br />
              <span className="text-cyan-300">Réinventé par l'IA.</span>
            </h2>
            
            <p className="text-xl text-white/80 mb-8 leading-relaxed">
              Rejoignez des milliers d'entrepreneurs qui révolutionnent 
              leur marketing avec l'intelligence artificielle.
            </p>
            
            <div className="space-y-4">
              {[
                "🤖 Génération de contenu intelligent",
                "💰 Système de récompenses crypto",
                "⚡ Automatisation complète"
              ].map((feature, index) => (
                <motion.div
                  key={feature}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 1 + index * 0.2, duration: 0.6 }}
                  className="flex items-center text-white/90"
                >
                  {feature}
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>

      {/* Colonne de droite - Formulaire */}
      <div className="w-full lg:w-1/2 flex flex-col justify-center px-8 lg:px-16">
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8 }}
          className="max-w-md mx-auto w-full"
        >
          {/* Titre */}
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold mb-2" style={{ color: 'var(--text-primary)' }}>
              {isLogin ? 'Connectez-vous' : 'Créez votre compte'}
            </h2>
            <p style={{ color: 'var(--text-secondary)' }}>
              {isLogin 
                ? 'Bon retour sur SmartSaaS !' 
                : 'Rejoignez la révolution du marketing IA'
              }
            </p>
          </div>

          {/* Boutons de connexion sociale */}
          <div className="space-y-3 mb-6">
            <button className="w-full btn btn-secondary flex items-center justify-center space-x-3 py-4">
              <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
              <span>Continuer avec Google</span>
            </button>
            
            <button className="w-full btn btn-secondary flex items-center justify-center space-x-3 py-4">
              <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
              <span>Continuer avec GitHub</span>
            </button>
          </div>

          {/* Séparateur */}
          <div className="relative mb-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t" style={{ borderColor: 'var(--border-primary)' }}></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-4" style={{ 
                background: 'var(--bg-primary)', 
                color: 'var(--text-secondary)' 
              }}>
                ou
              </span>
            </div>
          </div>

          {/* Formulaire */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {!isLogin && (
              <div>
                <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-primary)' }}>
                  Nom complet
                </label>
                <input
                  type="text"
                  required={!isLogin}
                  className="form-input"
                  placeholder="Votre nom complet"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                />
              </div>
            )}

            <div>
              <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-primary)' }}>
                Email
              </label>
              <input
                type="email"
                required
                className="form-input"
                placeholder="votre@email.com"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-primary)' }}>
                Mot de passe
              </label>
              <input
                type="password"
                required
                className="form-input"
                placeholder="••••••••"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full btn btn-primary py-4 text-lg font-semibold"
            >
              {loading ? (
                <span className="animate-pulse">Chargement...</span>
              ) : (
                isLogin ? 'Se Connecter' : 'Créer mon Compte'
              )}
            </button>
          </form>

          {/* Lien de basculement */}
          <div className="text-center mt-6">
            <button
              type="button"
              onClick={() => setIsLogin(!isLogin)}
              className="text-sm hover:underline"
              style={{ color: 'var(--text-secondary)' }}
            >
              {isLogin 
                ? "Pas encore de compte ? Inscrivez-vous"
                : "Déjà un compte ? Connectez-vous"
              }
            </button>
          </div>

          {/* Liens légaux */}
          <div className="text-center mt-8 space-x-4 text-xs" style={{ color: 'var(--text-muted)' }}>
            <Link href="/legal/privacy" className="hover:underline">
              Confidentialité
            </Link>
            <span>•</span>
            <Link href="/legal/terms" className="hover:underline">
              Conditions
            </Link>
          </div>
        </motion.div>
      </div>
    </div>
  );
}

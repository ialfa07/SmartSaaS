import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '../contexts/AuthContext';
import api from '../utils/api';

export default function Dashboard() {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    credits: 0,
    tokens: 0,
    generations: 0,
    level: { name: 'Débutant', level: 1 }
  });
  const [dailyRewardClaimed, setDailyRewardClaimed] = useState(false);
  const [weeklyProgress, setWeeklyProgress] = useState({ current: 1, target: 3 });

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const [userInfo, tokenBalance] = await Promise.all([
        api.get('/user-info'),
        api.get('/tokens/balance')
      ]);

      setStats({
        credits: userInfo.data.credits,
        tokens: tokenBalance.data.balance,
        generations: 0, // À implémenter
        level: tokenBalance.data.level
      });
    } catch (error) {
      console.error('Erreur chargement stats:', error);
    }
  };

  const claimDailyReward = async () => {
    try {
      await api.post('/tokens/daily-reward');
      setDailyRewardClaimed(true);
      loadStats(); // Recharger les stats
    } catch (error) {
      console.error('Erreur réclamation récompense:', error);
    }
  };

  const sidebarItems = [
    { name: 'Dashboard', icon: '📊', active: true },
    { name: 'Génération IA', icon: '🤖', href: '/generate' },
    { name: 'Mes Contenus', icon: '📝', href: '/content' },
    { name: 'Automatisation', icon: '⚡', href: '/automation' },
    { name: 'Parrainage', icon: '🎯', href: '/referral' },
    { name: 'Profil', icon: '👤', href: '/profile' },
  ];

  const quickAccessTools = [
    { name: 'Post LinkedIn', icon: '💼', color: 'from-blue-500 to-blue-600' },
    { name: 'Story Instagram', icon: '📸', color: 'from-pink-500 to-purple-600' },
    { name: 'Thread Twitter', icon: '🐦', color: 'from-cyan-400 to-cyan-600' },
    { name: 'Email Marketing', icon: '📧', color: 'from-green-500 to-green-600' },
  ];

  return (
    <div className="min-h-screen flex" style={{ background: 'var(--bg-primary)' }}>
      {/* Sidebar */}
      <nav className="sidebar">
        <div className="px-6 mb-8">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-r from-indigo-500 to-purple-600"></div>
            <h1 className="text-xl font-bold" style={{ color: 'var(--text-primary)' }}>
              SmartSaaS
            </h1>
          </div>
        </div>

        <div className="space-y-1">
          {sidebarItems.map((item, index) => (
            <motion.a
              key={item.name}
              href={item.href || '#'}
              className={`sidebar-item ${item.active ? 'active' : ''}`}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <span className="sidebar-item-icon">{item.icon}</span>
              {item.name}
            </motion.a>
          ))}
        </div>

        {/* User info en bas */}
        <div className="absolute bottom-4 left-4 right-4">
          <div className="card p-4">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 rounded-full bg-gradient-to-r from-indigo-400 to-purple-500 flex items-center justify-center text-white font-semibold">
                {user?.email?.[0]?.toUpperCase() || 'U'}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate" style={{ color: 'var(--text-primary)' }}>
                  {user?.email?.split('@')[0] || 'Utilisateur'}
                </p>
                <p className="text-xs" style={{ color: 'var(--text-secondary)' }}>
                  {stats.level.name}
                </p>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Contenu principal */}
      <main className="main-content">
        {/* Header */}
        <motion.div 
          className="mb-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h1 className="text-3xl font-bold mb-2" style={{ color: 'var(--text-primary)' }}>
            Bonjour, {user?.email?.split('@')[0] || 'Utilisateur'} ! 👋
          </h1>
          <p style={{ color: 'var(--text-secondary)' }}>
            Voici un aperçu de votre activité marketing IA
          </p>
        </motion.div>

        {/* Stats rapides */}
        <motion.div 
          className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <div className="card card-interactive">
            <div className="card-header">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 rounded-lg bg-gradient-to-r from-indigo-500 to-purple-600 flex items-center justify-center">
                  <span className="text-xl">🤖</span>
                </div>
                <div className="card-title">Crédits IA</div>
              </div>
            </div>
            <div className="card-body">
              <div className="widget-stat text-gradient">{stats.credits}</div>
              <p style={{ 
                color: 'var(--text-secondary)', 
                fontSize: 'var(--font-size-sm)' 
              }}>
                Générations disponibles
              </p>
            </div>
          </div>

          <div className="card card-success card-interactive">
            <div className="card-header">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 rounded-lg" style={{ 
                  background: 'var(--accent-success)' 
                }}>
                  <div className="flex items-center justify-center h-full">
                    <span className="text-xl">💰</span>
                  </div>
                </div>
                <div className="card-title">Jetons SaaS</div>
              </div>
            </div>
            <div className="card-body">
              <div className="widget-stat" style={{ color: 'var(--accent-success)' }}>
                {stats.tokens}
              </div>
              <p style={{ 
                color: 'var(--text-secondary)', 
                fontSize: 'var(--font-size-sm)' 
              }}>
                Récompenses gagnées
              </p>
            </div>
          </div>

          <div className="card card-interactive">
            <div className="card-header">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 rounded-lg bg-gradient-to-r from-cyan-500 to-blue-600 flex items-center justify-center">
                  <span className="text-xl">📊</span>
                </div>
                <div className="card-title">Contenus Générés</div>
              </div>
            </div>
            <div className="card-body">
              <div className="widget-stat text-gradient">{stats.generations}</div>
              <p style={{ 
                color: 'var(--text-secondary)', 
                fontSize: 'var(--font-size-sm)' 
              }}>
                Ce mois
              </p>
            </div>
          </div>
        </motion.div>

        {/* Grille de widgets */}
        <div className="widget-grid">
          {/* Accès rapide */}
          <motion.div 
            className="widget col-span-2"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3 }}
          >
            <div className="widget-title">🚀 Accès Rapide</div>
            <div className="grid grid-cols-2 gap-4 mt-4">
              {quickAccessTools.map((tool, index) => (
                <motion.button
                  key={tool.name}
                  className={`p-4 rounded-lg bg-gradient-to-r ${tool.color} text-white font-medium hover:scale-105 transition-transform`}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 + index * 0.1 }}
                >
                  <div className="text-2xl mb-2">{tool.icon}</div>
                  {tool.name}
                </motion.button>
              ))}
            </div>
          </motion.div>

          {/* Récompense quotidienne */}
          <motion.div 
            className="widget widget-success"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.5 }}
          >
            <div className="widget-title">🎁 Récompense Quotidienne</div>
            <div className="text-center mt-4">
              <div className="text-4xl mb-3">💰</div>
              <p className="mb-4" style={{ color: 'var(--text-secondary)' }}>
                Réclamez vos 5 jetons quotidiens !
              </p>
              {!dailyRewardClaimed ? (
                <button 
                  onClick={claimDailyReward}
                  className="btn btn-success w-full"
                >
                  Réclamer
                </button>
              ) : (
                <div className="reward-badge">
                  ✅ Réclamé aujourd'hui
                </div>
              )}
            </div>
          </motion.div>

          {/* Activité récente */}
          <motion.div 
            className="widget"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.6 }}
          >
            <div className="widget-title">📋 Activité Récente</div>
            <div className="space-y-3 mt-4">
              <div className="flex items-center space-x-3 p-3 rounded-lg" style={{ background: 'var(--bg-tertiary)' }}>
                <div className="text-xl">📝</div>
                <div>
                  <p className="font-medium" style={{ color: 'var(--text-primary)' }}>
                    Post LinkedIn généré
                  </p>
                  <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                    Il y a 2 heures
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-3 p-3 rounded-lg" style={{ background: 'var(--bg-tertiary)' }}>
                <div className="text-xl">🖼️</div>
                <div>
                  <p className="font-medium" style={{ color: 'var(--text-primary)' }}>
                    Image DALL-E créée
                  </p>
                  <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                    Hier
                  </p>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Objectif hebdomadaire */}
          <motion.div 
            className="widget"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.7 }}
          >
            <div className="widget-title">🎯 Objectif de la Semaine</div>
            <div className="mt-4">
              <p className="mb-3" style={{ color: 'var(--text-secondary)' }}>
                Générez du contenu pour 3 plateformes différentes
              </p>
              <div className="progress-bar">
                <div 
                  className="progress-fill"
                  style={{ width: `${(weeklyProgress.current / weeklyProgress.target) * 100}%` }}
                ></div>
              </div>
              <div className="flex justify-between text-sm mt-2">
                <span style={{ color: 'var(--text-secondary)' }}>
                  {weeklyProgress.current}/{weeklyProgress.target} plateformes
                </span>
                <span className="text-yellow-400 font-medium">
                  +50 jetons
                </span>
              </div>
            </div>
          </motion.div>
        </div>
      </main>
    </div>
  );
}
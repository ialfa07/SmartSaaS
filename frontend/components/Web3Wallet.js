
import { useState, useEffect } from 'react';
import { toast } from 'react-hot-toast';

export default function Web3Wallet({ user, onWalletConnected }) {
  const [walletAddress, setWalletAddress] = useState('');
  const [isConnecting, setIsConnecting] = useState(false);
  const [web3Info, setWeb3Info] = useState(null);
  const [balance, setBalance] = useState(null);

  useEffect(() => {
    fetchNetworkInfo();
  }, []);

  const fetchNetworkInfo = async () => {
    try {
      const response = await fetch('/api/web3/network-info');
      const data = await response.json();
      setWeb3Info(data);
    } catch (error) {
      console.error('Erreur réseau blockchain:', error);
    }
  };

  const connectWallet = async () => {
    if (!window.ethereum) {
      toast.error('MetaMask non détecté. Veuillez installer MetaMask.');
      return;
    }

    setIsConnecting(true);
    try {
      // Demander l'accès au portefeuille
      const accounts = await window.ethereum.request({
        method: 'eth_requestAccounts'
      });

      if (accounts.length > 0) {
        const address = accounts[0];
        setWalletAddress(address);

        // Connecter le portefeuille côté serveur
        const response = await fetch('/api/web3/connect-wallet', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify({
            wallet_address: address
          })
        });

        const result = await response.json();
        
        if (result.success) {
          toast.success(`Portefeuille connecté ! Vous avez gagné ${result.reward} jetons SaaS 🎉`);
          setBalance(result.reward);
          onWalletConnected && onWalletConnected(address);
          
          // Récupérer le solde blockchain
          fetchWalletBalance(address);
        } else {
          toast.error('Erreur lors de la connexion du portefeuille');
        }
      }
    } catch (error) {
      console.error('Erreur connexion portefeuille:', error);
      toast.error('Erreur lors de la connexion');
    } finally {
      setIsConnecting(false);
    }
  };

  const fetchWalletBalance = async (address) => {
    try {
      const response = await fetch(`/api/web3/wallet/${address}`);
      const data = await response.json();
      
      if (data.success) {
        setBalance(data);
      }
    } catch (error) {
      console.error('Erreur récupération solde:', error);
    }
  };

  const syncTokens = async () => {
    try {
      const response = await fetch('/api/web3/sync-tokens', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      const result = await response.json();
      
      if (result.success) {
        toast.success(`${result.tokens_synced} jetons synchronisés sur la blockchain !`);
        fetchWalletBalance(walletAddress);
      } else {
        toast.error('Erreur lors de la synchronisation');
      }
    } catch (error) {
      console.error('Erreur sync:', error);
      toast.error('Erreur lors de la synchronisation');
    }
  };

  const addTokenToWallet = async () => {
    if (!window.ethereum || !web3Info?.contract_address) return;

    try {
      await window.ethereum.request({
        method: 'wallet_watchAsset',
        params: {
          type: 'ERC20',
          options: {
            address: web3Info.contract_address,
            symbol: 'SAAS',
            decimals: 18,
            image: 'https://smartsaas.com/icon-saas-token.png'
          }
        }
      });
      toast.success('Token SaaS ajouté à votre portefeuille !');
    } catch (error) {
      console.error('Erreur ajout token:', error);
      toast.error('Erreur lors de l\'ajout du token');
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-800">
          🔗 Portefeuille Web3
        </h3>
        {web3Info?.connected && (
          <span className="px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs">
            Blockchain connectée
          </span>
        )}
      </div>

      {!walletAddress ? (
        <div className="text-center">
          <div className="mb-4">
            <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full mx-auto mb-3 flex items-center justify-center">
              <span className="text-white text-2xl">💳</span>
            </div>
            <p className="text-gray-600 mb-4">
              Connectez votre portefeuille MetaMask pour gérer vos jetons SaaS sur la blockchain
            </p>
            
            <button
              onClick={connectWallet}
              disabled={isConnecting}
              className={`w-full py-3 px-4 rounded-lg font-semibold transition-colors ${
                isConnecting
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-gradient-to-r from-purple-500 to-blue-500 text-white hover:from-purple-600 hover:to-blue-600'
              }`}
            >
              {isConnecting ? 'Connexion...' : 'Connecter MetaMask'}
            </button>
          </div>

          {web3Info && (
            <div className="text-sm text-gray-500 space-y-1">
              <p>Réseau: {web3Info.chain_id === 80001 ? 'Polygon Mumbai' : 'Autre'}</p>
              <p>Statut: {web3Info.connected ? '✅ Connecté' : '❌ Déconnecté'}</p>
            </div>
          )}
        </div>
      ) : (
        <div className="space-y-4">
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-gray-600">Adresse du portefeuille</span>
              <button
                onClick={() => navigator.clipboard.writeText(walletAddress)}
                className="text-blue-500 hover:text-blue-600 text-xs"
              >
                Copier
              </button>
            </div>
            <p className="font-mono text-sm break-all">
              {walletAddress}
            </p>
          </div>

          {balance && (
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-purple-50 rounded-lg p-3">
                <p className="text-sm text-purple-600">Jetons SaaS</p>
                <p className="text-xl font-bold text-purple-800">
                  {balance.saas_balance || 0}
                </p>
              </div>
              <div className="bg-blue-50 rounded-lg p-3">
                <p className="text-sm text-blue-600">MATIC</p>
                <p className="text-xl font-bold text-blue-800">
                  {balance.eth_balance?.toFixed(4) || '0.0000'}
                </p>
              </div>
            </div>
          )}

          <div className="space-y-2">
            <button
              onClick={syncTokens}
              className="w-full py-2 px-4 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
            >
              🔄 Synchroniser les jetons
            </button>
            
            <button
              onClick={addTokenToWallet}
              className="w-full py-2 px-4 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors"
            >
              ➕ Ajouter SaaS à MetaMask
            </button>
          </div>

          <div className="text-xs text-gray-500 space-y-1">
            <p>• Les jetons SaaS sont sur Polygon Mumbai (testnet)</p>
            <p>• Synchronisation automatique avec votre activité</p>
            <p>• Échangeable contre des crédits IA</p>
          </div>
        </div>
      )}
    </div>
  );
}

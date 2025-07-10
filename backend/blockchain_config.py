
import os
from web3 import Web3
from solcx import compile_standard, install_solc
import json

class BlockchainConfig:
    def __init__(self):
        self.networks = {
            "mumbai": {
                "rpc_url": "https://rpc-mumbai.maticvigil.com/",
                "chain_id": 80001,
                "name": "Polygon Mumbai Testnet",
                "explorer": "https://mumbai.polygonscan.com/",
                "gas_price": "20000000000"  # 20 gwei
            },
            "polygon": {
                "rpc_url": "https://polygon-rpc.com/",
                "chain_id": 137,
                "name": "Polygon Mainnet",
                "explorer": "https://polygonscan.com/",
                "gas_price": "30000000000"  # 30 gwei
            },
            "goerli": {
                "rpc_url": f"https://goerli.infura.io/v3/{os.getenv('INFURA_PROJECT_ID', '')}",
                "chain_id": 5,
                "name": "Ethereum Goerli Testnet",
                "explorer": "https://goerli.etherscan.io/",
                "gas_price": "20000000000"
            }
        }
        
        self.current_network = os.getenv("BLOCKCHAIN_NETWORK", "mumbai")
        self.network_config = self.networks[self.current_network]
    
    def get_deployment_info(self):
        """Informations pour déployer le contrat"""
        return {
            "network": self.current_network,
            "config": self.network_config,
            "contract_name": "SaasToken",
            "estimated_gas": 2000000,
            "deployment_steps": [
                "1. Compiler le contrat Solidity",
                "2. Déployer sur " + self.network_config["name"],
                "3. Vérifier le contrat sur " + self.network_config["explorer"],
                "4. Configurer les variables d'environnement",
                "5. Tester les fonctionnalités"
            ]
        }
    
    def generate_env_template(self, contract_address: str = ""):
        """Génère un template de variables d'environnement"""
        return f"""
# Configuration Blockchain/Web3
WEB3_RPC_URL={self.network_config["rpc_url"]}
WEB3_CHAIN_ID={self.network_config["chain_id"]}
WEB3_PRIVATE_KEY=your_private_key_here
SAAS_TOKEN_CONTRACT={contract_address or "contract_address_after_deployment"}

# Autres services (optionnel)
INFURA_PROJECT_ID=your_infura_project_id
ALCHEMY_API_KEY=your_alchemy_api_key
"""

# Instance globale
blockchain_config = BlockchainConfig()

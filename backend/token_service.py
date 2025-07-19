
from web3 import Web3
import os
import json
from typing import Dict, Optional
from logger import logger
from database import db_service

class TokenService:
    def __init__(self):
        self.w3 = None
        self.contract = None
        self.account = None
        self.initialize_web3()
    
    def initialize_web3(self):
        """Initialise la connexion Web3"""
        try:
            rpc_url = os.getenv("WEB3_RPC_URL", "https://polygon-mumbai.g.alchemy.com/v2/demo")
            self.w3 = Web3(Web3.HTTPProvider(rpc_url))
            
            if self.w3.is_connected():
                logger.info("✅ Connexion blockchain établie")
                self.setup_contract()
            else:
                logger.warning("⚠️ Connexion blockchain échouée")
                
        except Exception as e:
            logger.error(f"Erreur initialisation Web3: {e}")
    
    def setup_contract(self):
        """Configure le contrat intelligent"""
        try:
            contract_address = os.getenv("CONTRACT_ADDRESS")
            private_key = os.getenv("WEB3_PRIVATE_KEY")
            
            if not contract_address or not private_key:
                logger.warning("⚠️ Configuration blockchain manquante")
                return
            
            # ABI du contrat (simplifié)
            contract_abi = [
                {
                    "inputs": [{"name": "user", "type": "address"}, {"name": "amount", "type": "uint256"}, {"name": "reason", "type": "string"}],
                    "name": "rewardUser",
                    "outputs": [],
                    "stateMutability": "nonpayable",
                    "type": "function"
                },
                {
                    "inputs": [{"name": "account", "type": "address"}],
                    "name": "balanceOf",
                    "outputs": [{"name": "", "type": "uint256"}],
                    "stateMutability": "view",
                    "type": "function"
                }
            ]
            
            self.contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(contract_address),
                abi=contract_abi
            )
            
            self.account = self.w3.eth.account.from_key(private_key)
            logger.info("✅ Contrat intelligent configuré")
            
        except Exception as e:
            logger.error(f"Erreur configuration contrat: {e}")
    
    def is_connected(self) -> bool:
        """Vérifie si la blockchain est connectée"""
        return self.w3 is not None and self.w3.is_connected() and self.contract is not None
    
    def get_balance(self, wallet_address: str) -> Dict:
        """Récupère le solde blockchain d'une adresse"""
        try:
            if not self.is_connected():
                return {"success": False, "error": "Blockchain non connectée"}
            
            balance = self.contract.functions.balanceOf(
                Web3.to_checksum_address(wallet_address)
            ).call()
            
            return {
                "success": True,
                "balance": balance,
                "wallet_address": wallet_address
            }
            
        except Exception as e:
            logger.error(f"Erreur lecture solde: {e}")
            return {"success": False, "error": str(e)}
    
    def reward_user(self, wallet_address: str, amount: int, reason: str) -> Dict:
        """Récompense un utilisateur avec des tokens"""
        try:
            if not self.is_connected():
                return {"success": False, "error": "Blockchain non connectée"}
            
            # Construire la transaction
            transaction = self.contract.functions.rewardUser(
                Web3.to_checksum_address(wallet_address),
                amount,
                reason
            ).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 100000,
                'gasPrice': self.w3.to_wei('20', 'gwei')
            })
            
            # Signer et envoyer la transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Attendre la confirmation
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            if receipt.status == 1:
                return {
                    "success": True,
                    "tx_hash": tx_hash.hex(),
                    "amount": amount,
                    "wallet_address": wallet_address
                }
            else:
                return {"success": False, "error": "Transaction échouée"}
                
        except Exception as e:
            logger.error(f"Erreur récompense utilisateur: {e}")
            return {"success": False, "error": str(e)}
    
    def sync_user_tokens(self, user_id: int) -> Dict:
        """Synchronise les tokens entre la DB et la blockchain"""
        try:
            # Récupérer les données utilisateur
            user_tokens = db_service.get_user_saas_tokens(user_id)
            user_wallet = db_service.get_user_wallet(user_id)
            
            if not user_wallet:
                return {"success": False, "error": "Aucun portefeuille connecté"}
            
            # Récupérer le solde blockchain
            blockchain_balance = self.get_balance(user_wallet)
            
            if not blockchain_balance["success"]:
                return blockchain_balance
            
            # Calculer la différence
            db_balance = user_tokens["balance"]
            chain_balance = blockchain_balance["balance"]
            difference = db_balance - chain_balance
            
            if difference > 0:
                # Mint les tokens manquants sur la blockchain
                result = self.reward_user(
                    user_wallet, 
                    difference, 
                    "Synchronisation base de données"
                )
                return result
            else:
                return {
                    "success": True,
                    "message": "Synchronisation déjà à jour",
                    "db_balance": db_balance,
                    "chain_balance": chain_balance
                }
                
        except Exception as e:
            logger.error(f"Erreur synchronisation tokens: {e}")
            return {"success": False, "error": str(e)}
    
    def validate_address(self, address: str) -> bool:
        """Valide une adresse Ethereum"""
        try:
            return Web3.is_address(address)
        except:
            return False
    
    def get_network_info(self) -> Dict:
        """Informations sur le réseau blockchain"""
        try:
            if not self.w3:
                return {"connected": False, "error": "Web3 non initialisé"}
            
            if not self.w3.is_connected():
                return {"connected": False, "error": "Réseau non accessible"}
            
            chain_id = self.w3.eth.chain_id
            latest_block = self.w3.eth.block_number
            
            network_names = {
                1: "Ethereum Mainnet",
                137: "Polygon Mainnet", 
                80001: "Polygon Mumbai Testnet",
                8453: "Base Mainnet",
                84531: "Base Goerli Testnet"
            }
            
            return {
                "connected": True,
                "chain_id": chain_id,
                "network_name": network_names.get(chain_id, f"Unknown ({chain_id})"),
                "latest_block": latest_block,
                "contract_address": os.getenv("CONTRACT_ADDRESS"),
                "minter_address": self.account.address if self.account else None
            }
            
        except Exception as e:
            logger.error(f"Erreur info réseau: {e}")
            return {"connected": False, "error": str(e)}

token_service = TokenService()

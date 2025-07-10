
from web3 import Web3
from eth_account import Account
import os
import json
from typing import Dict, Optional
from datetime import datetime

class Web3Service:
    def __init__(self):
        # Configuration réseau (Polygon Mumbai testnet pour les tests)
        self.rpc_url = os.getenv("WEB3_RPC_URL", "https://rpc-mumbai.maticvigil.com/")
        self.chain_id = int(os.getenv("WEB3_CHAIN_ID", "80001"))  # Mumbai testnet
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        
        # Clé privée du contrat (pour les transactions automatiques)
        self.private_key = os.getenv("WEB3_PRIVATE_KEY", "")
        if self.private_key:
            self.account = Account.from_key(self.private_key)
        
        # Adresse du contrat SaaS Token (à déployer)
        self.contract_address = os.getenv("SAAS_TOKEN_CONTRACT", "")
        
        # ABI simplifié du contrat ERC-20
        self.contract_abi = [
            {
                "inputs": [{"name": "to", "type": "address"}, {"name": "amount", "type": "uint256"}],
                "name": "mint",
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
            },
            {
                "inputs": [{"name": "from", "type": "address"}, {"name": "to", "type": "address"}, {"name": "amount", "type": "uint256"}],
                "name": "transferFrom",
                "outputs": [{"name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            }
        ]
    
    def is_connected(self) -> bool:
        """Vérifie la connexion à la blockchain"""
        try:
            return self.w3.is_connected()
        except:
            return False
    
    def get_contract(self):
        """Récupère l'instance du contrat SaaS Token"""
        if not self.contract_address:
            return None
        return self.w3.eth.contract(
            address=self.contract_address,
            abi=self.contract_abi
        )
    
    def validate_address(self, address: str) -> bool:
        """Valide une adresse Ethereum"""
        try:
            return self.w3.is_address(address) and self.w3.is_checksum_address(address)
        except:
            return False
    
    def get_balance(self, wallet_address: str) -> Dict:
        """Récupère le solde de jetons SaaS d'une adresse"""
        try:
            if not self.validate_address(wallet_address):
                return {"success": False, "error": "Adresse invalide"}
            
            contract = self.get_contract()
            if not contract:
                return {"success": False, "error": "Contrat non configuré"}
            
            balance = contract.functions.balanceOf(wallet_address).call()
            
            # Récupérer le solde ETH/MATIC aussi
            eth_balance = self.w3.eth.get_balance(wallet_address)
            eth_balance_ether = self.w3.from_wei(eth_balance, 'ether')
            
            return {
                "success": True,
                "saas_balance": balance,
                "eth_balance": float(eth_balance_ether),
                "address": wallet_address
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def mint_tokens(self, recipient_address: str, amount: int) -> Dict:
        """Crée de nouveaux jetons SaaS pour un utilisateur"""
        try:
            if not self.private_key:
                return {"success": False, "error": "Clé privée non configurée"}
            
            if not self.validate_address(recipient_address):
                return {"success": False, "error": "Adresse destinataire invalide"}
            
            contract = self.get_contract()
            if not contract:
                return {"success": False, "error": "Contrat non configuré"}
            
            # Préparer la transaction
            nonce = self.w3.eth.get_transaction_count(self.account.address)
            gas_price = self.w3.eth.gas_price
            
            # Construire la transaction
            transaction = contract.functions.mint(
                recipient_address, 
                amount
            ).build_transaction({
                'chainId': self.chain_id,
                'gas': 100000,
                'gasPrice': gas_price,
                'nonce': nonce,
            })
            
            # Signer et envoyer
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            return {
                "success": True,
                "tx_hash": tx_hash.hex(),
                "amount": amount,
                "recipient": recipient_address
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def transfer_tokens(self, from_address: str, to_address: str, amount: int, private_key: str) -> Dict:
        """Transfère des jetons entre deux adresses"""
        try:
            if not self.validate_address(from_address) or not self.validate_address(to_address):
                return {"success": False, "error": "Adresse invalide"}
            
            contract = self.get_contract()
            if not contract:
                return {"success": False, "error": "Contrat non configuré"}
            
            # Créer un compte temporaire avec la clé privée
            temp_account = Account.from_key(private_key)
            
            # Préparer la transaction
            nonce = self.w3.eth.get_transaction_count(from_address)
            gas_price = self.w3.eth.gas_price
            
            transaction = contract.functions.transferFrom(
                from_address,
                to_address, 
                amount
            ).build_transaction({
                'chainId': self.chain_id,
                'gas': 100000,
                'gasPrice': gas_price,
                'nonce': nonce,
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            return {
                "success": True,
                "tx_hash": tx_hash.hex(),
                "amount": amount,
                "from": from_address,
                "to": to_address
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_transaction_status(self, tx_hash: str) -> Dict:
        """Vérifie le statut d'une transaction"""
        try:
            receipt = self.w3.eth.get_transaction_receipt(tx_hash)
            return {
                "success": True,
                "status": "confirmed" if receipt.status == 1 else "failed",
                "block_number": receipt.blockNumber,
                "gas_used": receipt.gasUsed
            }
        except Exception as e:
            return {"success": False, "error": "Transaction non trouvée"}
    
    def get_network_info(self) -> Dict:
        """Informations sur le réseau blockchain"""
        try:
            latest_block = self.w3.eth.block_number
            gas_price = self.w3.eth.gas_price
            
            return {
                "success": True,
                "connected": self.is_connected(),
                "chain_id": self.chain_id,
                "latest_block": latest_block,
                "gas_price_gwei": self.w3.from_wei(gas_price, 'gwei'),
                "rpc_url": self.rpc_url
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

# Instance globale du service
web3_service = Web3Service()

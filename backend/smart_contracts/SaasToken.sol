
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

contract SaasToken is ERC20, Ownable, Pausable {
    
    // Événements personnalisés
    event TokensRewarded(address indexed user, uint256 amount, string reason);
    event TokensSpent(address indexed user, uint256 amount, string purpose);
    event LevelUp(address indexed user, uint8 newLevel);
    
    // Mapping pour suivre les niveaux des utilisateurs
    mapping(address => uint8) public userLevels;
    mapping(address => uint256) public totalEarned;
    mapping(address => bool) public authorizedMinters;
    
    // Limites et paramètres
    uint256 public constant MAX_SUPPLY = 1000000000 * 10**18; // 1 milliard de tokens
    uint256 public rewardPool;
    
    // Niveaux et seuils
    uint256[] public levelThresholds = [0, 100, 500, 1500, 5000, 15000];
    string[] public levelNames = ["Débutant", "Actif", "Expert", "Maître", "Légende", "Titan"];
    
    constructor() ERC20("SaaS Token", "SAAS") {
        // Mint initial supply pour le pool de récompenses
        rewardPool = 100000000 * 10**18; // 100 millions pour les récompenses
        _mint(address(this), rewardPool);
        
        // Autoriser le propriétaire à mint
        authorizedMinters[msg.sender] = true;
    }
    
    modifier onlyMinter() {
        require(authorizedMinters[msg.sender], "Non autorisé à créer des tokens");
        _;
    }
    
    function addMinter(address minter) external onlyOwner {
        authorizedMinters[minter] = true;
    }
    
    function removeMinter(address minter) external onlyOwner {
        authorizedMinters[minter] = false;
    }
    
    function rewardUser(address user, uint256 amount, string memory reason) external onlyMinter whenNotPaused {
        require(user != address(0), "Adresse invalide");
        require(amount > 0, "Montant doit être positif");
        require(balanceOf(address(this)) >= amount, "Pool de récompenses insuffisant");
        
        // Transférer depuis le pool de récompenses
        _transfer(address(this), user, amount);
        
        // Mettre à jour les statistiques
        totalEarned[user] += amount;
        
        // Vérifier si l'utilisateur monte de niveau
        uint8 oldLevel = userLevels[user];
        uint8 newLevel = calculateLevel(totalEarned[user]);
        
        if (newLevel > oldLevel) {
            userLevels[user] = newLevel;
            emit LevelUp(user, newLevel);
        }
        
        emit TokensRewarded(user, amount, reason);
    }
    
    function spendTokens(address user, uint256 amount, string memory purpose) external onlyMinter whenNotPaused {
        require(balanceOf(user) >= amount, "Solde insuffisant");
        
        // Brûler les tokens dépensés
        _burn(user, amount);
        
        emit TokensSpent(user, amount, purpose);
    }
    
    function calculateLevel(uint256 totalTokens) public view returns (uint8) {
        for (uint8 i = uint8(levelThresholds.length - 1); i >= 0; i--) {
            if (totalTokens >= levelThresholds[i] * 10**18) {
                return i;
            }
        }
        return 0;
    }
    
    function getUserInfo(address user) external view returns (
        uint256 balance,
        uint256 totalEarnedTokens,
        uint8 level,
        string memory levelName,
        uint256 nextLevelThreshold
    ) {
        balance = balanceOf(user);
        totalEarnedTokens = totalEarned[user];
        level = userLevels[user];
        levelName = level < levelNames.length ? levelNames[level] : "Max Level";
        
        if (level < levelThresholds.length - 1) {
            nextLevelThreshold = levelThresholds[level + 1] * 10**18;
        } else {
            nextLevelThreshold = 0; // Niveau maximum atteint
        }
    }
    
    function getTopHolders(uint256 limit) external view returns (
        address[] memory holders,
        uint256[] memory balances
    ) {
        // Note: Dans un vrai contrat, cette fonction serait optimisée
        // Pour cette démo, on retourne des données limitées
        holders = new address[](limit);
        balances = new uint256[](limit);
        
        // Cette implémentation est simplifiée pour la démo
        // Dans la réalité, on utiliserait un système d'indexation off-chain
    }
    
    function emergencyWithdraw() external onlyOwner {
        uint256 balance = balanceOf(address(this));
        if (balance > 0) {
            _transfer(address(this), owner(), balance);
        }
    }
    
    function pause() external onlyOwner {
        _pause();
    }
    
    function unpause() external onlyOwner {
        _unpause();
    }
    
    // Override pour ajouter des vérifications lors des transferts
    function _beforeTokenTransfer(address from, address to, uint256 amount) internal override whenNotPaused {
        super._beforeTokenTransfer(from, to, amount);
    }
    
    // Fonction pour recevoir des ETH
    receive() external payable {
        // Le contrat peut recevoir de l'ETH pour le gas des transactions
    }
    
    // Retirer l'ETH du contrat
    function withdrawETH() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }
}

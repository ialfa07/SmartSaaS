
#!/usr/bin/env python3
"""
Script de test et analyse complète de SmartSaaS
"""

import os
import sys
import json
import subprocess
import requests
import time
from pathlib import Path
import ast
import re
from datetime import datetime

class SmartSaaSAnalyzer:
    def __init__(self):
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "structure": {},
            "backend": {},
            "frontend": {},
            "security": {},
            "performance": {},
            "recommendations": [],
            "errors": [],
            "score": 0
        }
        
    def analyze_project_structure(self):
        """Analyse la structure du projet"""
        print("📁 Analyse de la structure du projet...")
        
        required_files = {
            "backend": ["main.py", "models.py", "requirements.txt"],
            "frontend": ["package.json", "pages/index.js"],
            "root": ["README.md", ".env"]
        }
        
        missing_files = []
        
        for category, files in required_files.items():
            for file in files:
                if category == "root":
                    path = Path(file)
                else:
                    path = Path(category) / file
                    
                if not path.exists():
                    missing_files.append(str(path))
                    
        self.report["structure"] = {
            "missing_files": missing_files,
            "backend_exists": Path("backend").exists(),
            "frontend_exists": Path("frontend").exists(),
            "smart_contracts_exists": Path("backend/smart_contracts").exists()
        }
        
        if missing_files:
            self.report["errors"].append(f"Fichiers manquants: {missing_files}")
        
    def analyze_backend_code(self):
        """Analyse le code backend"""
        print("🔧 Analyse du backend...")
        
        backend_path = Path("backend")
        if not backend_path.exists():
            self.report["errors"].append("Dossier backend introuvable")
            return
            
        # Analyse des imports et dépendances
        main_py = backend_path / "main.py"
        if main_py.exists():
            with open(main_py, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Vérifier les imports critiques
            critical_imports = [
                "fastapi", "uvicorn", "sqlalchemy", "stripe", 
                "openai", "web3", "jose", "passlib"
            ]
            
            missing_imports = []
            for imp in critical_imports:
                if imp not in content:
                    missing_imports.append(imp)
                    
            # Analyser les endpoints
            endpoints = re.findall(r'@app\.(get|post|put|delete)\("([^"]+)"\)', content)
            
            # Vérifier la sécurité
            security_issues = []
            if "SECRET_KEY" in content and "your-secret-key-here" in content:
                security_issues.append("Clé secrète par défaut détectée")
            if "cors" in content.lower() and '"*"' in content:
                security_issues.append("CORS trop permissif")
                
            self.report["backend"] = {
                "endpoints": len(endpoints),
                "endpoint_list": endpoints,
                "missing_imports": missing_imports,
                "security_issues": security_issues,
                "file_size": len(content),
                "lines_of_code": len(content.split('\n'))
            }
            
        # Vérifier requirements.txt
        req_file = backend_path / "requirements.txt"
        if req_file.exists():
            with open(req_file, 'r') as f:
                requirements = f.read().strip().split('\n')
            self.report["backend"]["requirements_count"] = len(requirements)
            
    def analyze_frontend_code(self):
        """Analyse le code frontend"""
        print("💻 Analyse du frontend...")
        
        frontend_path = Path("frontend")
        if not frontend_path.exists():
            self.report["errors"].append("Dossier frontend introuvable")
            return
            
        # Vérifier package.json
        package_json = frontend_path / "package.json"
        if package_json.exists():
            with open(package_json, 'r') as f:
                package_data = json.load(f)
                
            self.report["frontend"] = {
                "dependencies": len(package_data.get("dependencies", {})),
                "dev_dependencies": len(package_data.get("devDependencies", {})),
                "scripts": list(package_data.get("scripts", {}).keys()),
                "framework": "Next.js" if "next" in package_data.get("dependencies", {}) else "Unknown"
            }
            
        # Analyser les pages
        pages_path = frontend_path / "pages"
        if pages_path.exists():
            pages = list(pages_path.glob("*.js"))
            self.report["frontend"]["pages_count"] = len(pages)
            
    def test_backend_startup(self):
        """Test de démarrage du backend"""
        print("🚀 Test de démarrage du backend...")
        
        try:
            # Changer vers le dossier backend
            os.chdir("backend")
            
            # Installer les dépendances
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                self.report["errors"].append(f"Erreur installation dépendances: {result.stderr}")
                return False
                
            self.report["backend"]["dependencies_installed"] = True
            return True
            
        except subprocess.TimeoutExpired:
            self.report["errors"].append("Timeout lors de l'installation des dépendances")
            return False
        except Exception as e:
            self.report["errors"].append(f"Erreur test backend: {str(e)}")
            return False
        finally:
            os.chdir("..")
            
    def test_api_endpoints(self):
        """Test des endpoints API"""
        print("🌐 Test des endpoints API...")
        
        # Démarrer le serveur en arrière-plan pour les tests
        try:
            import subprocess
            import time
            
            os.chdir("backend")
            server_process = subprocess.Popen([sys.executable, "main.py"], 
                                            stdout=subprocess.PIPE, 
                                            stderr=subprocess.PIPE)
            time.sleep(5)  # Attendre que le serveur démarre
            
            # Tester l'endpoint racine
            try:
                response = requests.get("http://localhost:8000/", timeout=5)
                if response.status_code == 200:
                    self.report["backend"]["api_accessible"] = True
                else:
                    self.report["backend"]["api_accessible"] = False
                    self.report["errors"].append(f"API retourne {response.status_code}")
            except requests.RequestException as e:
                self.report["backend"]["api_accessible"] = False
                self.report["errors"].append(f"Impossible de joindre l'API: {str(e)}")
                
            server_process.terminate()
            
        except Exception as e:
            self.report["errors"].append(f"Erreur test API: {str(e)}")
        finally:
            os.chdir("..")
            
    def check_security(self):
        """Analyse de sécurité"""
        print("🔒 Analyse de sécurité...")
        
        security_score = 100
        issues = []
        
        # Vérifier .env
        if Path(".env").exists():
            with open(".env", 'r') as f:
                env_content = f.read()
            if "SECRET_KEY" not in env_content:
                issues.append("SECRET_KEY manquante dans .env")
                security_score -= 20
        else:
            issues.append("Fichier .env manquant")
            security_score -= 30
            
        # Vérifier la configuration CORS
        main_py = Path("backend/main.py")
        if main_py.exists():
            with open(main_py, 'r') as f:
                content = f.read()
            if 'allow_origins=["*"]' in content or '"*"' in content:
                issues.append("Configuration CORS trop permissive")
                security_score -= 25
                
        # Vérifier les clés API hardcodées
        for file_path in Path("backend").rglob("*.py"):
            with open(file_path, 'r') as f:
                content = f.read()
            if re.search(r'sk_test_|sk_live_|api_key.*=.*"[^"]{20,}"', content):
                issues.append(f"Clé API potentiellement hardcodée dans {file_path}")
                security_score -= 15
                
        self.report["security"] = {
            "score": max(0, security_score),
            "issues": issues
        }
        
    def calculate_overall_score(self):
        """Calcule le score global"""
        print("📊 Calcul du score global...")
        
        score = 0
        max_score = 100
        
        # Structure (20 points)
        if self.report["structure"]["backend_exists"]:
            score += 10
        if self.report["structure"]["frontend_exists"]:
            score += 10
            
        # Backend (40 points)
        if self.report["backend"].get("dependencies_installed"):
            score += 15
        if self.report["backend"].get("endpoints", 0) > 10:
            score += 15
        if self.report["backend"].get("api_accessible"):
            score += 10
            
        # Frontend (20 points)
        if self.report["frontend"].get("dependencies", 0) > 0:
            score += 10
        if self.report["frontend"].get("pages_count", 0) > 3:
            score += 10
            
        # Sécurité (20 points)
        security_score = self.report["security"].get("score", 0)
        score += int(security_score * 0.2)
        
        # Pénalités pour erreurs
        score -= len(self.report["errors"]) * 5
        
        self.report["score"] = max(0, min(100, score))
        
    def generate_recommendations(self):
        """Génère des recommandations"""
        print("💡 Génération de recommandations...")
        
        recommendations = []
        
        # Recommandations structurelles
        if not self.report["structure"]["backend_exists"]:
            recommendations.append("Créer la structure backend avec main.py")
            
        # Recommandations backend
        if self.report["backend"].get("security_issues"):
            recommendations.append("Corriger les problèmes de sécurité identifiés")
            
        # Recommandations frontend
        if self.report["frontend"].get("pages_count", 0) < 5:
            recommendations.append("Ajouter plus de pages pour une application complète")
            
        # Recommandations sécurité
        if self.report["security"]["score"] < 80:
            recommendations.append("Améliorer la sécurité (configuration CORS, variables d'environnement)")
            
        # Recommandations générales
        if len(self.report["errors"]) > 5:
            recommendations.append("Corriger les erreurs critiques avant mise en production")
            
        recommendations.extend([
            "Ajouter des tests unitaires",
            "Implémenter un système de logging",
            "Configurer un monitoring",
            "Documenter l'API avec Swagger",
            "Mettre en place CI/CD",
            "Optimiser les performances"
        ])
        
        self.report["recommendations"] = recommendations[:10]  # Top 10
        
    def run_analysis(self):
        """Lance l'analyse complète"""
        print("🔍 Démarrage de l'analyse SmartSaaS...")
        print("=" * 50)
        
        self.analyze_project_structure()
        self.analyze_backend_code()
        self.analyze_frontend_code()
        self.test_backend_startup()
        self.test_api_endpoints()
        self.check_security()
        self.calculate_overall_score()
        self.generate_recommendations()
        
        return self.report
        
    def print_report(self):
        """Affiche le rapport détaillé"""
        print("\n" + "=" * 60)
        print("📋 RAPPORT D'ANALYSE SMARTSAAS")
        print("=" * 60)
        
        print(f"\n🎯 SCORE GLOBAL: {self.report['score']}/100")
        
        if self.report['score'] >= 80:
            print("✅ EXCELLENT - Projet prêt pour la production")
        elif self.report['score'] >= 60:
            print("⚠️  BON - Quelques améliorations nécessaires")
        elif self.report['score'] >= 40:
            print("🔶 MOYEN - Corrections importantes requises")
        else:
            print("❌ CRITIQUE - Refactoring majeur nécessaire")
            
        print(f"\n📁 STRUCTURE DU PROJET")
        print(f"   Backend: {'✅' if self.report['structure']['backend_exists'] else '❌'}")
        print(f"   Frontend: {'✅' if self.report['structure']['frontend_exists'] else '❌'}")
        print(f"   Smart Contracts: {'✅' if self.report['structure']['smart_contracts_exists'] else '❌'}")
        
        if self.report['structure']['missing_files']:
            print(f"   Fichiers manquants: {', '.join(self.report['structure']['missing_files'])}")
            
        print(f"\n🔧 BACKEND")
        print(f"   Endpoints: {self.report['backend'].get('endpoints', 0)}")
        print(f"   Lignes de code: {self.report['backend'].get('lines_of_code', 0)}")
        print(f"   Dépendances installées: {'✅' if self.report['backend'].get('dependencies_installed') else '❌'}")
        print(f"   API accessible: {'✅' if self.report['backend'].get('api_accessible') else '❌'}")
        
        if self.report['backend'].get('security_issues'):
            print(f"   Problèmes sécurité: {len(self.report['backend']['security_issues'])}")
            
        print(f"\n💻 FRONTEND")
        print(f"   Framework: {self.report['frontend'].get('framework', 'Non détecté')}")
        print(f"   Pages: {self.report['frontend'].get('pages_count', 0)}")
        print(f"   Dépendances: {self.report['frontend'].get('dependencies', 0)}")
        
        print(f"\n🔒 SÉCURITÉ")
        print(f"   Score: {self.report['security']['score']}/100")
        if self.report['security']['issues']:
            print("   Problèmes détectés:")
            for issue in self.report['security']['issues']:
                print(f"   - {issue}")
                
        print(f"\n❌ ERREURS ({len(self.report['errors'])})")
        for error in self.report['errors'][:5]:  # Top 5 erreurs
            print(f"   - {error}")
            
        print(f"\n💡 RECOMMANDATIONS TOP 5")
        for i, rec in enumerate(self.report['recommendations'][:5], 1):
            print(f"   {i}. {rec}")
            
        print("\n" + "=" * 60)
        print("📊 ANALYSE TERMINÉE")
        print("=" * 60)

if __name__ == "__main__":
    analyzer = SmartSaaSAnalyzer()
    report = analyzer.run_analysis()
    analyzer.print_report()
    
    # Sauvegarder le rapport
    with open("smartsaas_analysis_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Rapport sauvegardé dans: smartsaas_analysis_report.json")

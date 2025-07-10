
#!/usr/bin/env python3
"""
Test rapide des fonctionnalités SmartSaaS
"""

import sys
import subprocess
import json
from pathlib import Path

def test_imports():
    """Test des imports Python critiques"""
    print("🐍 Test des imports Python...")
    
    critical_modules = [
        'fastapi', 'uvicorn', 'sqlalchemy', 'stripe', 
        'requests', 'jose', 'passlib', 'psycopg2'
    ]
    
    missing = []
    for module in critical_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            print(f"   ❌ {module}")
            missing.append(module)
    
    return len(missing) == 0

def test_backend_syntax():
    """Test de la syntaxe du backend"""
    print("\n🔧 Test syntaxe backend...")
    
    backend_files = list(Path("backend").glob("*.py"))
    errors = []
    
    for file in backend_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                compile(f.read(), file, 'exec')
            print(f"   ✅ {file.name}")
        except SyntaxError as e:
            print(f"   ❌ {file.name}: {e}")
            errors.append(f"{file.name}: {e}")
    
    return len(errors) == 0

def test_frontend_config():
    """Test de la configuration frontend"""
    print("\n💻 Test configuration frontend...")
    
    package_json = Path("frontend/package.json")
    if not package_json.exists():
        print("   ❌ package.json manquant")
        return False
    
    try:
        with open(package_json, 'r') as f:
            config = json.load(f)
        
        required_deps = ['next', 'react', 'react-dom']
        missing_deps = []
        
        deps = config.get('dependencies', {})
        for dep in required_deps:
            if dep in deps:
                print(f"   ✅ {dep}: {deps[dep]}")
            else:
                print(f"   ❌ {dep}: manquant")
                missing_deps.append(dep)
        
        return len(missing_deps) == 0
        
    except json.JSONDecodeError as e:
        print(f"   ❌ Erreur JSON: {e}")
        return False

def test_database_models():
    """Test des modèles de base de données"""
    print("\n🗄️  Test modèles base de données...")
    
    try:
        sys.path.append('backend')
        from models import User, SaasToken, Payment, Base
        
        print("   ✅ Modèle User")
        print("   ✅ Modèle SaasToken")
        print("   ✅ Modèle Payment")
        print("   ✅ Base SQLAlchemy")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Erreur import: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Erreur modèles: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 SmartSaaS - Test Rapide")
    print("=" * 40)
    
    tests = [
        ("Imports Python", test_imports),
        ("Syntaxe Backend", test_backend_syntax),
        ("Config Frontend", test_frontend_config),
        ("Modèles DB", test_database_models)
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"   ❌ Erreur dans {name}: {e}")
            results.append((name, False))
    
    print(f"\n📊 RÉSULTATS")
    print("=" * 40)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {name}: {status}")
    
    print(f"\nScore: {passed}/{total} ({int(passed/total*100)}%)")
    
    if passed == total:
        print("🎉 Tous les tests sont passés!")
    else:
        print("⚠️  Certains tests ont échoué - vérifiez la configuration")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

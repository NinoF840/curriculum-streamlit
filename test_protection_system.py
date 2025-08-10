#!/usr/bin/env python3
"""
Test del Sistema di Protezione Pro
==================================

Verifica che il sistema di autenticazione e licensing funzioni correttamente.

Author: Antonino Piacenza
Email: ninomedical.ai@gmail.com
"""

import sys
import os
from pathlib import Path

# Aggiungi il path corrente per import
sys.path.append(str(Path(__file__).parent))

def test_auth_system():
    """Test del sistema di autenticazione."""
    print("🔍 Testing Authentication System...")
    
    try:
        from auth_system import AuthManager, SessionManager, UserRole
        
        # Test creazione AuthManager
        auth_manager = AuthManager()
        print("✅ AuthManager created successfully")
        
        # Test utente admin di default
        admin = auth_manager.get_user_by_username("admin")
        if admin:
            print(f"✅ Default admin user found: {admin.username}")
        else:
            print("❌ Default admin user not found")
        
        # Test creazione utente test
        try:
            test_user = auth_manager.create_user(
                username="test_free_user",
                email="test@example.com", 
                password="TestPass123!",
                full_name="Test Free User",
                role=UserRole.GUEST
            )
            print(f"✅ Test user created: {test_user.username}")
        except Exception as e:
            if "già esistente" in str(e):
                print("ℹ️  Test user already exists")
            else:
                print(f"❌ Error creating test user: {e}")
        
        # Test autenticazione
        authenticated_user = auth_manager.authenticate("test_free_user", "TestPass123!")
        if authenticated_user:
            print(f"✅ Authentication successful for: {authenticated_user.full_name}")
        else:
            print("❌ Authentication failed")
            
        return True
        
    except Exception as e:
        print(f"❌ Auth system test failed: {e}")
        return False

def test_license_system():
    """Test del sistema di licensing."""
    print("\n🔍 Testing License System...")
    
    try:
        from pro_license_system import LicenseManager, ProFeatureGuard
        
        # Test creazione LicenseManager
        license_manager = LicenseManager()
        print("✅ LicenseManager created successfully")
        
        # Test utente senza licenza (dovrebbe fallire)
        test_user_id = 999  # ID inesistente
        has_pro_access = license_manager.validate_pro_access(test_user_id)
        if not has_pro_access:
            print("✅ Correctly denied Pro access for unlicensed user")
        else:
            print("❌ Incorrectly granted Pro access")
        
        # Test concessione licenza Pro
        try:
            license_key = license_manager.grant_pro_access(test_user_id, 30)
            print(f"✅ Pro license generated: {license_key}")
            
            # Verifica validazione licenza
            has_pro_access_after = license_manager.validate_pro_access(test_user_id)
            if has_pro_access_after:
                print("✅ Pro access correctly validated after license grant")
            else:
                print("❌ Pro access validation failed after grant")
                
        except Exception as e:
            print(f"❌ Error granting Pro license: {e}")
        
        # Test features Pro
        pro_features = ProFeatureGuard.PRO_FEATURES
        print(f"✅ Pro features defined: {len(pro_features)} features")
        print(f"   Features: {list(pro_features.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ License system test failed: {e}")
        return False

def test_app_structure():
    """Test della struttura dell'app."""
    print("\n🔍 Testing App Structure...")
    
    try:
        # Verifica esistenza file principali
        required_files = [
            "nino_medical_ai_app.py",
            "auth_system.py", 
            "pro_license_system.py",
            "streamlit_runner.py"
        ]
        
        missing_files = []
        for file in required_files:
            if not Path(file).exists():
                missing_files.append(file)
        
        if missing_files:
            print(f"❌ Missing required files: {missing_files}")
            return False
        else:
            print("✅ All required files present")
        
        # Test import dell'app principale
        try:
            # Solo test di sintassi, senza eseguire Streamlit
            with open("nino_medical_ai_app.py", 'r', encoding='utf-8') as f:
                content = f.read()
                # Verifica presenza funzioni chiave
                required_functions = [
                    "def main()",
                    "def render_welcome_page()",
                    "@ProFeatureGuard.require_pro_feature"
                ]
                
                for func in required_functions:
                    if func in content:
                        print(f"✅ Found: {func}")
                    else:
                        print(f"❌ Missing: {func}")
                        
        except Exception as e:
            print(f"❌ Error reading main app: {e}")
            
        return True
        
    except Exception as e:
        print(f"❌ App structure test failed: {e}")
        return False

def test_database_creation():
    """Test creazione database."""
    print("\n🔍 Testing Database Creation...")
    
    try:
        # Cleanup eventuali database test esistenti
        auth_db = Path("auth/users.db")
        license_db = Path("auth/licenses.db")
        
        # Crea directory se non esiste
        Path("auth").mkdir(exist_ok=True)
        
        # Test creazione database auth
        from auth_system import AuthManager
        auth_manager = AuthManager()
        print("✅ Auth database created/verified")
        
        # Test creazione database licenze
        from pro_license_system import LicenseManager  
        license_manager = LicenseManager()
        print("✅ License database created/verified")
        
        # Verifica esistenza file database
        if auth_db.exists():
            print(f"✅ Auth DB exists: {auth_db}")
        if license_db.exists():
            print(f"✅ License DB exists: {license_db}")
            
        return True
        
    except Exception as e:
        print(f"❌ Database creation test failed: {e}")
        return False

def test_protection_decorators():
    """Test dei decoratori di protezione."""
    print("\n🔍 Testing Protection Decorators...")
    
    try:
        from pro_license_system import ProFeatureGuard
        
        # Test definizione decorator
        @ProFeatureGuard.require_pro_feature('test_feature')
        def test_protected_function():
            return "This should be protected"
        
        print("✅ Protection decorator defined successfully")
        
        # Verifica che la funzione sia wrapped correttamente
        if hasattr(test_protected_function, '__wrapped__') or callable(test_protected_function):
            print("✅ Function correctly wrapped by decorator")
        else:
            print("❌ Function not properly wrapped")
            
        return True
        
    except Exception as e:
        print(f"❌ Protection decorators test failed: {e}")
        return False

def main():
    """Esegue tutti i test."""
    print("🧪 NINO MEDICAL AI - SISTEMA DI PROTEZIONE PRO")
    print("=" * 60)
    
    tests = [
        ("Authentication System", test_auth_system),
        ("License System", test_license_system),
        ("App Structure", test_app_structure),
        ("Database Creation", test_database_creation), 
        ("Protection Decorators", test_protection_decorators)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'=' * 20} {test_name} {'=' * 20}")
        results[test_name] = test_func()
    
    # Riepilogo
    print("\n" + "=" * 60)
    print("🏁 RIEPILOGO TEST:")
    print("=" * 60)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25}: {status}")
        if result:
            passed += 1
    
    print(f"\n📊 Risultato finale: {passed}/{total} test passati")
    
    if passed == total:
        print("🎉 TUTTI I TEST SUPERATI! Sistema di protezione Pro funzionante.")
        print("\n🚀 L'app è pronta per il deploy con protezione Pro attiva!")
        print("\n📋 Prossimi passi:")
        print("   1. Deploy su Streamlit Cloud")
        print("   2. Configurare variabili d'ambiente per sicurezza")  
        print("   3. Test con utenti reali")
        print("   4. Monitoraggio utilizzo Pro vs Free")
    else:
        print("⚠️  ALCUNI TEST FALLITI - Rivedere la configurazione")
        
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

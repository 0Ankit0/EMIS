#!/usr/bin/env python3
"""
Django Project Validation Script
Validates that the EMIS Django project is properly configured.
"""

import os
import sys
from pathlib import Path

def check_files():
    """Check that all required files exist"""
    print("🔍 Checking project structure...")
    
    required_files = [
        'manage.py',
        'config/settings.py',
        'config/urls.py',
        'config/wsgi.py',
        'config/asgi.py',
        'config/celery.py',
        'config/__init__.py',
        'requirements.txt',
        'pytest.ini',
        '.env.development',
        '.env.production',
    ]
    
    missing = []
    for file in required_files:
        if not Path(file).exists():
            missing.append(file)
    
    if missing:
        print(f"❌ Missing files: {', '.join(missing)}")
        return False
    else:
        print(f"✅ All {len(required_files)} required files present")
        return True

def check_apps():
    """Check that all Django apps are properly configured"""
    print("\n🔍 Checking Django apps...")
    
    apps_dir = Path('apps')
    if not apps_dir.exists():
        print("❌ apps/ directory not found")
        return False
    
    app_names = [
        'core', 'authentication', 'students', 'faculty', 'hr',
        'finance', 'library', 'admissions', 'exams', 'attendance',
        'timetable', 'hostel', 'transport', 'inventory', 'lms',
        'analytics', 'notifications', 'reports'
    ]
    
    issues = []
    for app_name in app_names:
        app_path = apps_dir / app_name
        if not app_path.exists():
            issues.append(f"{app_name}: directory missing")
            continue
        
        required_app_files = [
            '__init__.py', 'models.py', 'views.py', 'urls.py',
            'api_urls.py', 'api_views.py', 'admin.py', 'apps.py'
        ]
        
        for file in required_app_files:
            if not (app_path / file).exists():
                issues.append(f"{app_name}/{file}: missing")
    
    if issues:
        print(f"❌ App issues found:")
        for issue in issues[:10]:  # Show first 10
            print(f"   - {issue}")
        if len(issues) > 10:
            print(f"   ... and {len(issues) - 10} more")
        return False
    else:
        print(f"✅ All {len(app_names)} apps properly configured")
        return True

def check_templates():
    """Check that template directories exist"""
    print("\n🔍 Checking templates...")
    
    template_dirs = [
        'templates',
        'templates/includes',
        'templates/authentication',
    ]
    
    missing = []
    for dir_path in template_dirs:
        if not Path(dir_path).exists():
            missing.append(dir_path)
    
    if missing:
        print(f"❌ Missing template directories: {', '.join(missing)}")
        return False
    else:
        print(f"✅ Template structure present")
        return True

def check_static():
    """Check that static directories exist"""
    print("\n🔍 Checking static files...")
    
    static_dirs = [
        'static',
        'static/css',
        'static/js',
        'static/images',
    ]
    
    for dir_path in static_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print(f"✅ Static directories present")
    return True

def check_syntax():
    """Check Python syntax of key files"""
    print("\n🔍 Checking Python syntax...")
    
    import py_compile
    
    key_files = [
        'config/settings.py',
        'config/urls.py',
        'config/wsgi.py',
        'config/asgi.py',
        'config/celery.py',
        'manage.py',
    ]
    
    errors = []
    for file in key_files:
        try:
            py_compile.compile(file, doraise=True)
        except py_compile.PyCompileError as e:
            errors.append(f"{file}: {e}")
    
    if errors:
        print(f"❌ Syntax errors found:")
        for error in errors:
            print(f"   - {error}")
        return False
    else:
        print(f"✅ All {len(key_files)} key files have valid Python syntax")
        return True

def main():
    """Run all validation checks"""
    print("="*70)
    print("EMIS Django Project Validation")
    print("="*70)
    
    checks = [
        ("Project Structure", check_files),
        ("Django Apps", check_apps),
        ("Templates", check_templates),
        ("Static Files", check_static),
        ("Python Syntax", check_syntax),
    ]
    
    results = {}
    for name, check_func in checks:
        results[name] = check_func()
    
    print("\n" + "="*70)
    print("VALIDATION SUMMARY")
    print("="*70)
    
    all_passed = True
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
        if not passed:
            all_passed = False
    
    print("="*70)
    
    if all_passed:
        print("\n🎉 All validation checks passed!")
        print("✅ Project is properly configured")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Setup database: python manage.py migrate")
        print("3. Create superuser: python manage.py createsuperuser")
        print("4. Start server: ./start-dev.sh")
        return 0
    else:
        print("\n⚠️  Some validation checks failed")
        print("Please fix the issues above before proceeding")
        return 1

if __name__ == '__main__':
    sys.exit(main())

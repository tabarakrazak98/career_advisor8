import os

# إعدادات الأمان
SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
CSRF_ENABLED = True

# إعدادات التطبيق
APP_NAME = "مستشارك المهني الذكي"
MAX_RESULTS = 50
SUPPORTED_LANGUAGES = ['ar']
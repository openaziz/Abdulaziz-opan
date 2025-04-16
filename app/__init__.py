from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os
from datetime import datetime

# تهيئة المكتبات
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # إعدادات التطبيق
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'مفتاح-سري-افتراضي-للتطوير-فقط'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///cybersecurity.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # تهيئة قاعدة البيانات
    db.init_app(app)
    migrate.init_app(app, db)
    
    # تهيئة نظام تسجيل الدخول
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'يرجى تسجيل الدخول للوصول إلى هذه الصفحة'
    login_manager.login_message_category = 'info'
    
    # تسجيل المسارات
    from app.routes.pages import pages
    from app.routes.auth import auth
    from app.routes.admin import admin
    
    app.register_blueprint(pages)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')
    
    # إضافة دالة مساعدة للقوالب
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}
    
    # إنشاء قاعدة البيانات إذا لم تكن موجودة
    with app.app_context():
        db.create_all()
    
    return app

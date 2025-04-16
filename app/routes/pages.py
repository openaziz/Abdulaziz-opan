from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import SecurityTip, Tool, Tutorial
from app import db
from flask_login import current_user, login_required

pages = Blueprint('pages', __name__)

@pages.route('/')
def index():
    tips = SecurityTip.query.order_by(SecurityTip.created_at.desc()).limit(3).all()
    return render_template('index.html', tips=tips, page_title="الصفحة الرئيسية")

@pages.route('/kali-linux')
def kali_linux():
    tools = Tool.query.filter_by(category='kali').all()
    tutorials = Tutorial.query.filter_by(category='kali').all()
    return render_template('kali_linux.html', tools=tools, tutorials=tutorials, page_title="كالي لينكس")

@pages.route('/termux')
def termux():
    tools = Tool.query.filter_by(category='termux').all()
    tutorials = Tutorial.query.filter_by(category='termux').all()
    return render_template('termux.html', tools=tools, tutorials=tutorials, page_title="تيرمكس")

@pages.route('/code-generator')
def code_generator():
    return render_template('code_generator.html', page_title="مولد الأكواد")

@pages.route('/bot-builder')
def bot_builder():
    return render_template('bot_builder.html', page_title="إنشاء البوتات")

@pages.route('/key-generator')
def key_generator():
    return render_template('key_generator.html', page_title="مولد المفاتيح")

@pages.route('/apk-downloads')
def apk_downloads():
    return render_template('apk_downloads.html', page_title="تحميل تطبيقات APK")

@pages.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        flash('غير مصرح لك بالوصول إلى لوحة التحكم', 'danger')
        return redirect(url_for('pages.index'))
    
    users_count = 0  # سيتم تحديثه لاحقاً
    tools_count = Tool.query.count()
    tips_count = SecurityTip.query.count()
    tutorials_count = Tutorial.query.count()
    
    return render_template('dashboard.html', 
                          users_count=users_count,
                          tools_count=tools_count,
                          tips_count=tips_count,
                          tutorials_count=tutorials_count,
                          page_title="لوحة التحكم")

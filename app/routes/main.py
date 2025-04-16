from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import SecurityTip, Tool, Tutorial
from app import db
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    tips = SecurityTip.query.order_by(SecurityTip.created_at.desc()).limit(3).all()
    return render_template('index.html', tips=tips)

@main.route('/kali-linux')
def kali_linux():
    tools = Tool.query.filter_by(category='kali').all()
    tutorials = Tutorial.query.filter_by(category='kali').all()
    return render_template('kali_linux.html', tools=tools, tutorials=tutorials)

@main.route('/termux')
def termux():
    tools = Tool.query.filter_by(category='termux').all()
    tutorials = Tutorial.query.filter_by(category='termux').all()
    return render_template('termux.html', tools=tools, tutorials=tutorials)

@main.route('/protection-accounts')
def protection_accounts():
    tips = SecurityTip.query.filter_by(category='accounts').all()
    return render_template('protection_accounts.html', tips=tips)

@main.route('/cyber-attacks')
def cyber_attacks():
    attacks = SecurityTip.query.filter_by(category='attacks').all()
    return render_template('cyber_attacks.html', attacks=attacks)

@main.route('/code-generator')
def code_generator():
    return render_template('code_generator.html')

@main.route('/bot-builder')
def bot_builder():
    return render_template('bot_builder.html')

@main.route('/key-generator')
def key_generator():
    return render_template('key_generator.html')

@main.route('/apk-downloads')
def apk_downloads():
    return render_template('apk_downloads.html')

@main.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('main.index'))
    
    tools = Tool.query.filter(Tool.name.contains(query) | Tool.description.contains(query)).all()
    tips = SecurityTip.query.filter(SecurityTip.title.contains(query) | SecurityTip.content.contains(query)).all()
    tutorials = Tutorial.query.filter(Tutorial.title.contains(query) | Tutorial.content.contains(query)).all()
    
    return render_template('search_results.html', 
                          query=query, 
                          tools=tools, 
                          tips=tips, 
                          tutorials=tutorials)

@main.route('/initialize-data')
def initialize_data():
    """مسار لتهيئة البيانات الأولية للموقع (للتطوير فقط)"""
    if not current_user.is_authenticated or not current_user.is_admin:
        flash('غير مصرح لك بالوصول إلى هذه الصفحة', 'danger')
        return redirect(url_for('main.index'))
    
    # إضافة أدوات كالي لينكس
    kali_tools = [
        {
            'name': 'Nmap',
            'description': 'أداة مسح الشبكات وفحص المنافذ المفتوحة',
            'command': 'nmap -sV -p 1-1000 [IP_ADDRESS]',
            'category': 'kali'
        },
        {
            'name': 'Metasploit Framework',
            'description': 'إطار عمل لاختبار الاختراق واستغلال الثغرات',
            'command': 'msfconsole',
            'category': 'kali'
        },
        {
            'name': 'Wireshark',
            'description': 'محلل حزم الشبكة لمراقبة وتحليل حركة المرور',
            'command': 'wireshark',
            'category': 'kali'
        },
        {
            'name': 'Aircrack-ng',
            'description': 'مجموعة أدوات لاختبار أمان شبكات WiFi',
            'command': 'aircrack-ng',
            'category': 'kali'
        }
    ]
    
    # إضافة أدوات تيرمكس
    termux_tools = [
        {
            'name': 'Nmap لتيرمكس',
            'description': 'أداة مسح الشبكات وفحص المنافذ المفتوحة على الأجهزة المحمولة',
            'command': 'pkg install nmap && nmap -sV [IP_ADDRESS]',
            'category': 'termux'
        },
        {
            'name': 'Metasploit لتيرمكس',
            'description': 'إطار عمل لاختبار الاختراق على الأجهزة المحمولة',
            'command': 'pkg install unstable-repo && pkg install metasploit',
            'category': 'termux'
        },
        {
            'name': 'Hydra لتيرمكس',
            'description': 'أداة كسر كلمات المرور بالقوة الغاشمة على الأجهزة المحمولة',
            'command': 'pkg install hydra && hydra -l username -P wordlist.txt ssh://[IP_ADDRESS]',
            'category': 'termux'
        }
    ]
    
    # إضافة نصائح أمنية
    security_tips = [
        {
            'title': 'استخدام كلمات مرور قوية',
            'content': 'استخدم كلمات مرور طويلة (12 حرف على الأقل) تحتوي على مزيج من الأحرف الكبيرة والصغيرة والأرقام والرموز. تجنب استخدام نفس كلمة المرور لحسابات متعددة.',
            'category': 'accounts'
        },
        {
            'title': 'تفعيل المصادقة الثنائية',
            'content': 'قم بتفعيل المصادقة الثنائية (2FA) على جميع حساباتك المهمة لإضافة طبقة إضافية من الحماية حتى لو تم اختراق كلمة المرور.',
            'category': 'accounts'
        },
        {
            'title': 'الحذر من هجمات التصيد',
            'content': 'كن حذراً من رسائل البريد الإلكتروني والرسائل النصية المشبوهة. لا تنقر على روابط أو تفتح مرفقات من مصادر غير موثوقة.',
            'category': 'attacks'
        }
    ]
    
    # إضافة دروس تعليمية
    tutorials = [
        {
            'title': 'مقدمة في Kali Linux',
            'content': 'تعرف على نظام كالي لينكس وكيفية تثبيته واستخدامه للاختبار الأمني.',
            'category': 'kali',
            'difficulty': 'beginner'
        },
        {
            'title': 'استخدام Nmap لفحص الشبكات',
            'content': 'تعلم كيفية استخدام أداة Nmap لفحص الشبكات واكتشاف الأجهزة والخدمات.',
            'category': 'kali',
            'difficulty': 'intermediate'
        },
        {
            'title': 'مقدمة في Termux',
            'content': 'تعرف على تطبيق Termux وكيفية استخدامه لتشغيل أدوات لينكس على هاتفك الأندرويد.',
            'category': 'termux',
            'difficulty': 'beginner'
        }
    ]
    
    # إضافة البيانات إلى قاعدة البيانات
    for tool in kali_tools + termux_tools:
        db_tool = Tool(
            name=tool['name'],
            description=tool['description'],
            category=tool['category'],
            command=tool.get('command', '')
        )
        db.session.add(db_tool)
    
    for tip in security_tips:
        db_tip = SecurityTip(
            title=tip['title'],
            content=tip['content'],
            category=tip['category']
        )
        db.session.add(db_tip)
    
    for tutorial in tutorials:
        db_tutorial = Tutorial(
            title=tutorial['title'],
            content=tutorial['content'],
            category=tutorial['category'],
            difficulty=tutorial['difficulty']
        )
        db.session.add(db_tutorial)
    
    db.session.commit()
    flash('تم تهيئة البيانات بنجاح', 'success')
    return redirect(url_for('main.index'))

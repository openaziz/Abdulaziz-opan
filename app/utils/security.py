import re
import secrets
import string
import hashlib
from datetime import datetime

def validate_password(password):
    """
    التحقق من قوة كلمة المرور
    يجب أن تحتوي على 8 أحرف على الأقل وتتضمن أحرف كبيرة وصغيرة وأرقام ورموز
    """
    if len(password) < 8:
        return False
    
    # التحقق من وجود حرف كبير
    if not re.search(r'[A-Z]', password):
        return False
    
    # التحقق من وجود حرف صغير
    if not re.search(r'[a-z]', password):
        return False
    
    # التحقق من وجود رقم
    if not re.search(r'[0-9]', password):
        return False
    
    # التحقق من وجود رمز
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    
    return True

def generate_secure_token(length=32):
    """
    توليد رمز آمن بطول محدد
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def hash_data(data):
    """
    تشفير البيانات باستخدام SHA-256
    """
    return hashlib.sha256(data.encode()).hexdigest()

def secure_filename(filename):
    """
    تأمين اسم الملف لمنع هجمات حقن الملفات
    """
    # إزالة المسارات
    filename = filename.replace('/', '_').replace('\\', '_')
    
    # إضافة طابع زمني للتفرد
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
    
    # تنظيف الاسم
    name = re.sub(r'[^a-zA-Z0-9_-]', '', name)
    
    # إعادة تكوين اسم الملف
    if ext:
        return f"{name}_{timestamp}.{ext}"
    return f"{name}_{timestamp}"

def sanitize_input(text):
    """
    تنظيف المدخلات لمنع هجمات XSS
    """
    if text is None:
        return ''
    
    # استبدال الرموز الخاصة
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&#x27;')
    
    return text

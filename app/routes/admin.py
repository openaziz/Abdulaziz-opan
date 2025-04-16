from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import User, SecurityTip, Tool, Tutorial
from app import db
from functools import wraps

admin = Blueprint('admin', __name__, url_prefix='/admin')

# دالة للتحقق من صلاحيات المدير
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('غير مصرح لك بالوصول إلى هذه الصفحة', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/')
@login_required
@admin_required
def dashboard():
    users_count = User.query.count()
    tips_count = SecurityTip.query.count()
    tools_count = Tool.query.count()
    tutorials_count = Tutorial.query.count()
    
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                          users_count=users_count,
                          tips_count=tips_count,
                          tools_count=tools_count,
                          tutorials_count=tutorials_count,
                          recent_users=recent_users)

@admin.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin.route('/users/<int:user_id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    
    # منع تغيير صلاحيات المستخدم الحالي
    if user.id == current_user.id:
        flash('لا يمكنك تغيير صلاحياتك الخاصة', 'danger')
        return redirect(url_for('admin.users'))
    
    user.is_admin = not user.is_admin
    db.session.commit()
    
    flash(f'تم تحديث صلاحيات المستخدم {user.username}', 'success')
    return redirect(url_for('admin.users'))

@admin.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # منع حذف المستخدم الحالي
    if user.id == current_user.id:
        flash('لا يمكنك حذف حسابك الخاص من هنا', 'danger')
        return redirect(url_for('admin.users'))
    
    db.session.delete(user)
    db.session.commit()
    
    flash(f'تم حذف المستخدم {user.username}', 'success')
    return redirect(url_for('admin.users'))

@admin.route('/security-tips')
@login_required
@admin_required
def security_tips():
    tips = SecurityTip.query.all()
    return render_template('admin/security_tips.html', tips=tips)

@admin.route('/security-tips/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_security_tip():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        
        if not title or not content or not category:
            flash('جميع الحقول مطلوبة', 'danger')
            return redirect(url_for('admin.add_security_tip'))
        
        tip = SecurityTip(title=title, content=content, category=category)
        db.session.add(tip)
        db.session.commit()
        
        flash('تمت إضافة النصيحة الأمنية بنجاح', 'success')
        return redirect(url_for('admin.security_tips'))
    
    return render_template('admin/add_security_tip.html')

@admin.route('/tools')
@login_required
@admin_required
def tools():
    tools = Tool.query.all()
    return render_template('admin/tools.html', tools=tools)

@admin.route('/tools/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_tool():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        category = request.form.get('category')
        command = request.form.get('command')
        
        if not name or not description or not category:
            flash('الاسم والوصف والفئة مطلوبة', 'danger')
            return redirect(url_for('admin.add_tool'))
        
        tool = Tool(
            name=name,
            description=description,
            category=category,
            command=command
        )
        db.session.add(tool)
        db.session.commit()
        
        flash('تمت إضافة الأداة بنجاح', 'success')
        return redirect(url_for('admin.tools'))
    
    return render_template('admin/add_tool.html')

@admin.route('/tutorials')
@login_required
@admin_required
def tutorials():
    tutorials = Tutorial.query.all()
    return render_template('admin/tutorials.html', tutorials=tutorials)

@admin.route('/tutorials/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_tutorial():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        difficulty = request.form.get('difficulty')
        
        if not title or not content or not category or not difficulty:
            flash('جميع الحقول مطلوبة', 'danger')
            return redirect(url_for('admin.add_tutorial'))
        
        tutorial = Tutorial(
            title=title,
            content=content,
            category=category,
            difficulty=difficulty
        )
        db.session.add(tutorial)
        db.session.commit()
        
        flash('تمت إضافة الدرس التعليمي بنجاح', 'success')
        return redirect(url_for('admin.tutorials'))
    
    return render_template('admin/add_tutorial.html')

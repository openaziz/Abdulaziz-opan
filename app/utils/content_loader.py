def get_kali_tools():
    """
    قائمة بأدوات كالي لينكس الشائعة
    """
    return [
        {
            'name': 'Nmap',
            'description': 'أداة مسح الشبكات وفحص المنافذ المفتوحة',
            'command': 'nmap -sV -p 1-1000 [IP_ADDRESS]',
            'image_url': '/static/images/tools/nmap.png'
        },
        {
            'name': 'Metasploit Framework',
            'description': 'إطار عمل لاختبار الاختراق واستغلال الثغرات',
            'command': 'msfconsole',
            'image_url': '/static/images/tools/metasploit.png'
        },
        {
            'name': 'Wireshark',
            'description': 'محلل حزم الشبكة لمراقبة وتحليل حركة المرور',
            'command': 'wireshark',
            'image_url': '/static/images/tools/wireshark.png'
        },
        {
            'name': 'Aircrack-ng',
            'description': 'مجموعة أدوات لاختبار أمان شبكات WiFi',
            'command': 'aircrack-ng',
            'image_url': '/static/images/tools/aircrack.png'
        },
        {
            'name': 'Hydra',
            'description': 'أداة كسر كلمات المرور بالقوة الغاشمة',
            'command': 'hydra -l username -P wordlist.txt ssh://[IP_ADDRESS]',
            'image_url': '/static/images/tools/hydra.png'
        },
        {
            'name': 'John the Ripper',
            'description': 'أداة كسر تشفير كلمات المرور',
            'command': 'john --format=raw-md5 hashes.txt',
            'image_url': '/static/images/tools/john.png'
        },
        {
            'name': 'Burp Suite',
            'description': 'أداة اختبار أمان تطبيقات الويب',
            'command': 'burpsuite',
            'image_url': '/static/images/tools/burp.png'
        },
        {
            'name': 'SQLmap',
            'description': 'أداة اكتشاف واستغلال ثغرات حقن SQL',
            'command': 'sqlmap -u "http://example.com/page.php?id=1" --dbs',
            'image_url': '/static/images/tools/sqlmap.png'
        }
    ]

def get_termux_tools():
    """
    قائمة بأدوات تيرمكس الشائعة
    """
    return [
        {
            'name': 'Nmap لتيرمكس',
            'description': 'أداة مسح الشبكات وفحص المنافذ المفتوحة على الأجهزة المحمولة',
            'command': 'pkg install nmap && nmap -sV [IP_ADDRESS]',
            'image_url': '/static/images/tools/nmap_termux.png'
        },
        {
            'name': 'Metasploit لتيرمكس',
            'description': 'إطار عمل لاختبار الاختراق على الأجهزة المحمولة',
            'command': 'pkg install unstable-repo && pkg install metasploit',
            'image_url': '/static/images/tools/metasploit_termux.png'
        },
        {
            'name': 'Hydra لتيرمكس',
            'description': 'أداة كسر كلمات المرور بالقوة الغاشمة على الأجهزة المحمولة',
            'command': 'pkg install hydra && hydra -l username -P wordlist.txt ssh://[IP_ADDRESS]',
            'image_url': '/static/images/tools/hydra_termux.png'
        },
        {
            'name': 'SQLmap لتيرمكس',
            'description': 'أداة اكتشاف واستغلال ثغرات حقن SQL على الأجهزة المحمولة',
            'command': 'pip install sqlmap && sqlmap -u "http://example.com/page.php?id=1" --dbs',
            'image_url': '/static/images/tools/sqlmap_termux.png'
        },
        {
            'name': 'Aircrack-ng لتيرمكس',
            'description': 'مجموعة أدوات لاختبار أمان شبكات WiFi على الأجهزة المحمولة',
            'command': 'pkg install root-repo && pkg install aircrack-ng',
            'image_url': '/static/images/tools/aircrack_termux.png'
        },
        {
            'name': 'Nikto لتيرمكس',
            'description': 'ماسح ثغرات خوادم الويب للأجهزة المحمولة',
            'command': 'pkg install perl && cpan install Bundle::LWP && git clone https://github.com/sullo/nikto',
            'image_url': '/static/images/tools/nikto_termux.png'
        }
    ]

def get_security_tips():
    """
    قائمة بنصائح الأمن السيبراني
    """
    return [
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
            'title': 'تحديث البرامج باستمرار',
            'content': 'قم بتحديث نظام التشغيل والتطبيقات بانتظام للحصول على إصلاحات الأمان الأخيرة وسد الثغرات المعروفة.',
            'category': 'general'
        },
        {
            'title': 'الحذر من هجمات التصيد',
            'content': 'كن حذراً من رسائل البريد الإلكتروني والرسائل النصية المشبوهة. لا تنقر على روابط أو تفتح مرفقات من مصادر غير موثوقة.',
            'category': 'attacks'
        },
        {
            'title': 'استخدام شبكات VPN',
            'content': 'استخدم شبكات VPN موثوقة عند الاتصال بشبكات WiFi عامة لتشفير اتصالك وحماية بياناتك من المتطفلين.',
            'category': 'general'
        },
        {
            'title': 'النسخ الاحتياطي المنتظم',
            'content': 'قم بعمل نسخ احتياطية منتظمة لبياناتك المهمة واختبر استعادتها. يفضل اتباع قاعدة 3-2-1: ثلاث نسخ، على وسيطين مختلفين، مع نسخة واحدة خارج الموقع.',
            'category': 'general'
        },
        {
            'title': 'مراقبة تصاريح التطبيقات',
            'content': 'راجع وقيد تصاريح التطبيقات على هاتفك وحاسوبك. امنح التطبيقات فقط التصاريح التي تحتاجها للعمل.',
            'category': 'general'
        },
        {
            'title': 'الحماية من هجمات حقن SQL',
            'content': 'استخدم الاستعلامات المعدة مسبقاً وتحقق من صحة جميع مدخلات المستخدم لمنع هجمات حقن SQL في تطبيقات الويب.',
            'category': 'attacks'
        }
    ]

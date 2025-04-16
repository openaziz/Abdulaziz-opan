#!/usr/bin/env python3
"""
أداة تحويل تطبيق الويب إلى تطبيق أندرويد APK
تعمل على Termux وأنظمة لينكس
"""

import os
import sys
import argparse
import subprocess
import shutil
import time
import json
from pathlib import Path

# الألوان للطرفية
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_banner():
    banner = f"""
    {Colors.RED}{Colors.BOLD}
    ╔═══════════════════════════════════════════════════╗
    ║                                                   ║
    ║   █████╗ ██████╗ ██╗  ██╗    ██████╗ ██╗   ██╗   ║
    ║  ██╔══██╗██╔══██╗██║ ██╔╝    ██╔══██╗██║   ██║   ║
    ║  ███████║██████╔╝█████╔╝     ██████╔╝██║   ██║   ║
    ║  ██╔══██║██╔═══╝ ██╔═██╗     ██╔══██╗██║   ██║   ║
    ║  ██║  ██║██║     ██║  ██╗    ██████╔╝╚██████╔╝   ║
    ║  ╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝    ╚═════╝  ╚═════╝    ║
    ║                                                   ║
    ║   عبدالعزيز للأمن السيبراني - أداة بناء التطبيقات   ║
    ║                                                   ║
    ╚═══════════════════════════════════════════════════╝
    {Colors.END}
    """
    print(banner)

def check_requirements():
    """التحقق من وجود المتطلبات الأساسية"""
    print(f"{Colors.BLUE}[*] التحقق من المتطلبات الأساسية...{Colors.END}")
    
    requirements = {
        "java": "Java Development Kit",
        "gradle": "Gradle Build Tool",
        "npm": "Node Package Manager",
        "cordova": "Apache Cordova"
    }
    
    missing = []
    
    for cmd, name in requirements.items():
        try:
            subprocess.run([cmd, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            print(f"{Colors.GREEN}[✓] تم العثور على {name}{Colors.END}")
        except FileNotFoundError:
            print(f"{Colors.RED}[✗] لم يتم العثور على {name}{Colors.END}")
            missing.append(cmd)
    
    if missing:
        print(f"\n{Colors.YELLOW}[!] يجب تثبيت الحزم التالية:{Colors.END}")
        
        if "java" in missing:
            print(f"{Colors.YELLOW}    - JDK: pkg install openjdk-17{Colors.END}")
        
        if "gradle" in missing:
            print(f"{Colors.YELLOW}    - Gradle: pkg install gradle{Colors.END}")
        
        if "npm" in missing:
            print(f"{Colors.YELLOW}    - NPM: pkg install nodejs{Colors.END}")
        
        if "cordova" in missing:
            print(f"{Colors.YELLOW}    - Cordova: npm install -g cordova{Colors.END}")
        
        print(f"\n{Colors.RED}[!] يرجى تثبيت المتطلبات المفقودة ثم إعادة تشغيل الأداة{Colors.END}")
        sys.exit(1)
    
    print(f"{Colors.GREEN}[✓] جميع المتطلبات متوفرة{Colors.END}")

def create_cordova_project(project_name, output_dir):
    """إنشاء مشروع كوردوفا جديد"""
    print(f"\n{Colors.BLUE}[*] إنشاء مشروع كوردوفا جديد...{Colors.END}")
    
    project_path = os.path.join(output_dir, project_name)
    
    # إنشاء مشروع كوردوفا جديد
    try:
        subprocess.run(["cordova", "create", project_path, f"com.abdulaziz.{project_name.lower()}", project_name], 
                      check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}[✗] فشل إنشاء مشروع كوردوفا: {e}{Colors.END}")
        sys.exit(1)
    
    # إضافة منصة أندرويد
    try:
        os.chdir(project_path)
        subprocess.run(["cordova", "platform", "add", "android"], 
                      check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}[✗] فشل إضافة منصة أندرويد: {e}{Colors.END}")
        sys.exit(1)
    
    print(f"{Colors.GREEN}[✓] تم إنشاء مشروع كوردوفا بنجاح{Colors.END}")
    return project_path

def copy_web_files(web_dir, cordova_dir):
    """نسخ ملفات الويب إلى مشروع كوردوفا"""
    print(f"\n{Colors.BLUE}[*] نسخ ملفات الويب إلى مشروع كوردوفا...{Colors.END}")
    
    www_dir = os.path.join(cordova_dir, "www")
    
    # حذف الملفات الافتراضية
    for item in os.listdir(www_dir):
        item_path = os.path.join(www_dir, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
    
    # نسخ ملفات الويب
    for item in os.listdir(web_dir):
        src_path = os.path.join(web_dir, item)
        dst_path = os.path.join(www_dir, item)
        
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)
        elif os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path)
    
    print(f"{Colors.GREEN}[✓] تم نسخ ملفات الويب بنجاح{Colors.END}")

def update_config_xml(cordova_dir, app_name, app_description, app_author):
    """تحديث ملف config.xml"""
    print(f"\n{Colors.BLUE}[*] تحديث ملف التكوين...{Colors.END}")
    
    config_path = os.path.join(cordova_dir, "config.xml")
    
    try:
        import xml.etree.ElementTree as ET
        
        tree = ET.parse(config_path)
        root = tree.getroot()
        
        # تحديث اسم التطبيق
        name_elem = root.find("name")
        if name_elem is not None:
            name_elem.text = app_name
        
        # تحديث وصف التطبيق
        desc_elem = root.find("description")
        if desc_elem is not None:
            desc_elem.text = app_description
        
        # تحديث معلومات المؤلف
        author_elem = root.find("author")
        if author_elem is not None:
            author_elem.text = app_author
            author_elem.set("email", "sa6aa6116@gmail.com")
            author_elem.set("href", "https://github.com/openaziz")
        
        # إضافة أذونات أندرويد
        android_elem = root.find("./platform[@name='android']")
        if android_elem is None:
            android_elem = ET.SubElement(root, "platform", {"name": "android"})
        
        permissions = [
            "android.permission.INTERNET",
            "android.permission.ACCESS_NETWORK_STATE",
            "android.permission.WRITE_EXTERNAL_STORAGE",
            "android.permission.READ_EXTERNAL_STORAGE"
        ]
        
        for permission in permissions:
            perm_elem = ET.SubElement(android_elem, "config-file", {
                "parent": "/manifest",
                "target": "AndroidManifest.xml"
            })
            uses_perm = ET.SubElement(perm_elem, "uses-permission", {
                "android:name": permission
            })
        
        # حفظ التغييرات
        tree.write(config_path, encoding="utf-8", xml_declaration=True)
        
        print(f"{Colors.GREEN}[✓] تم تحديث ملف التكوين بنجاح{Colors.END}")
    
    except Exception as e:
        print(f"{Colors.RED}[✗] فشل تحديث ملف التكوين: {e}{Colors.END}")
        sys.exit(1)

def build_apk(cordova_dir, output_dir):
    """بناء ملف APK"""
    print(f"\n{Colors.BLUE}[*] بناء ملف APK...{Colors.END}")
    
    try:
        os.chdir(cordova_dir)
        subprocess.run(["cordova", "build", "android", "--release"], 
                      check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # نسخ ملف APK إلى مجلد الإخراج
        apk_path = os.path.join(cordova_dir, "platforms/android/app/build/outputs/apk/release/app-release-unsigned.apk")
        output_apk = os.path.join(output_dir, "abdulaziz-cybersecurity.apk")
        shutil.copy2(apk_path, output_apk)
        
        print(f"{Colors.GREEN}[✓] تم بناء ملف APK بنجاح{Colors.END}")
        print(f"{Colors.GREEN}[✓] مسار ملف APK: {output_apk}{Colors.END}")
        
        return output_apk
    
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}[✗] فشل بناء ملف APK: {e}{Colors.END}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="أداة تحويل تطبيق الويب إلى تطبيق أندرويد APK")
    parser.add_argument("--web-dir", required=True,

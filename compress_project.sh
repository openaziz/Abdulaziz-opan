#!/bin/bash

echo "ضغط مجلد المشروع بالكامل..."
ZIP_NAME="abdulaziz-ai-ready.zip"
zip -r $ZIP_NAME . -x "*.env" "*.git*" "__pycache__/*" "*.zip"

echo "تم إنشاء الملف المضغوط: $ZIP_NAME"

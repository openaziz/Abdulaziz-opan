#!/bin/bash

# سكربت تثبيت شامل لأدوات الذكاء الاصطناعي والتعلم العميق
# تأكد من تشغيله كـ sudo أو كمستخدم عادي (يفضل مع وصول sudo)

echo "╔════════════════════════════════════╗"
echo "║   بدء تثبيت أدوات الذكاء الاصطناعي   ║"
echo "╚════════════════════════════════════╝"

# 1. تثبيت المتطلبات الأساسية
echo "▶ تثبيت المتطلبات الأساسية..."
sudo apt-get update && sudo apt-get install -y \
    python3-pip \
    python3-dev \
    python3-venv \
    build-essential \
    cmake \
    git \
    wget \
    curl \
    nvidia-cuda-toolkit  # إذا كنت تستخدم GPU من NVIDIA

# 2. إنشاء بيئة بايثون افتراضية
echo "▶ إنشاء بيئة بايثون افتراضية..."
python3 -m venv ai_env
source ai_env/bin/activate

# 3. تثبيت أدوات الذكاء الاصطناعي الأساسية
echo "▶ تثبيت أدوات الذكاء الاصطناعي الأساسية..."
pip install --upgrade pip
pip install numpy scipy pandas matplotlib seaborn jupyterlab

# 4. تثبيت أدوات تعلم الآلة
echo "▶ تثبيت أدوات تعلم الآلة..."
pip install scikit-learn xgboost lightgbm catboost statsmodels

# 5. تثبيت أدوات التعلم العميق
echo "▶ تثبيت أدوات التعلم العميق..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118  # لـ CUDA 11.8
pip install tensorflow keras
pip install transformers sentence-transformers datasets evaluate
pip install diffusers accelerate safetensors

# 6. تثبيت أدوات معالجة اللغة الطبيعية
echo "▶ تثبيت أدوات NLP..."
pip install spacy nltk gensim stanza
python -m spacy download en_core_web_lg
python -m nltk.downloader popular

# 7. تثبيت أدوات البحث والويب
echo "▶ تثبيت أدوات البحث والويب..."
pip install beautifulsoup4 scrapy selenium requests requests-html playwright
playwright install  # لتثبيت متصفحات للويب سكرابينغ

# 8. تثبيت أدوات التكامل مع APIs
echo "▶ تثبيت أدوات APIs..."
pip install openai google-generativeai langchain llama-index anthropic

# 9. تثبيت أدوات التصور والتفاعل
echo "▶ تثبيت أدوات التصور..."
pip install plotly dash streamlit gradio

# 10. تثبيت أدوات مساعدة
echo "▶ تثبيت أدوات مساعدة..."
pip install tqdm ipywidgets joblib psutil memory_profiler

# 11. تثبيت أدوات التطوير
echo "▶ تثبيت أدوات التطوير..."
pip install black flake8 pylint pytest notebook lab

echo "╔════════════════════════════════════╗"
echo "║   اكتمل التثبيت بنجاح!            ║"
echo "╚════════════════════════════════════╝"

# تعليمات التشغيل
echo -e "\nلتشغيل البيئة الافتراضية:"
echo "source ai_env/bin/activate"

echo -e "\nلبدء Jupyter Lab:"
echo "jupyter lab"

echo -e "\nلاختبار PyTorch (GPU):"
echo "python -c \"import torch; print(torch.cuda.is_available())\""

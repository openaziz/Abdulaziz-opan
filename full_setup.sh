#!/bin/bash

# ألوان متقدمة للواجهة
BOLD=$(tput bold)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color


# التحقق من صلاحيات root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}${BOLD}[!] يرجى التشغيل بصلاحيات root (sudo)!${NC}"
    exit 1
fi

# دالة لتركيب الحزم مع معالجة الأخطاء
install_packages() {
    local packages=("$@")
    for pkg in "${packages[@]}"; do
        echo -e "${YELLOW}${BOLD}[~] جاري تثبيت ${pkg}...${NC}"
        if apt install -y $pkg 2>/dev/null; then
            echo -e "${GREEN}${BOLD}[✓] ${pkg} تم التثبيت بنجاح${NC}"
        else
            echo -e "${RED}${BOLD}[X] فشل تثبيت ${pkg}${NC}"
            echo -e "${CYAN}محاولة البحث في المستودعات الأخرى...${NC}"
            apt search $pkg 2>/dev/null || echo -e "${RED}الحزمة غير متوفرة${NC}"
        fi
    done
}

# ======== المرحلة 1: التحديثات الأساسية ========
echo -e "${CYAN}${BOLD}[+] تحديث النظام الأساسي...${NC}"
apt update -y && apt full-upgrade -y
apt install -y software-properties-common apt-transport-https ca-certificates \
curl gnupg dirmngr gnupg-curl

# ======== المرحلة 2: إضافة المستودعات والمفاتيح ========
echo -e "\n${MAGENTA}${BOLD}[+] إضافة مستودعات متخصصة...${NC}"

# المستودعات من السكربت الأول
sources1=(
    "deb https://deb.debian.org/debian bookworm-backports main contrib non-free"
    "deb [arch=amd64] https://download.docker.com/linux/debian bookworm stable"
    "deb https://packages.cloud.google.com/apt cloud-sdk main"
    "deb https://dl.yarnpkg.com/debian/ stable main"
)

# المستودعات من السكربت الثاني
sources2=(
    "deb http://ppa.launchpad.net/ethereum/ethereum/ubuntu jammy main"
    "deb http://ppa.launchpad.net/linuxuprising/java/ubuntu jammy main"
)

for src in "${sources1[@]}" "${sources2[@]}"; do
    echo $src >> /etc/apt/sources.list.d/extras.list
done

# إضافة مفاتيح APT
echo -e "\n${BLUE}${BOLD}[+] إضافة مفاتيح مصادقة...${NC}"

keys1=(
    "https://download.docker.com/linux/debian/gpg"
    "https://packages.cloud.google.com/apt/doc/apt-key.gpg"
    "https://dl.yarnpkg.com/debian/pubkey.gpg"
)

keys2=(
    "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0xEEA14886"
    "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x73C3DB2A"
)

for key in "${keys1[@]}" "${keys2[@]}"; do
    curl -fsSL $key | gpg --dearmor -o /usr/share/keyrings/$(basename $key).gpg
done

# التحديث بعد إضافة المستودعات
apt update -y

# ======== المرحلة 3: تثبيت الحزم الأساسية ========
categories=(
    # من السكربت الأول
    "التطوير النظامي:build-essential cmake ninja-build gcc-12 g++-12 clang-15 llvm lldb"
    "بايثون:python3.11 python3.11-dev python3.11-venv python3-pip python3.11-full"
    "جافا:openjdk-19-jdk openjdk-19-jre maven gradle"
    "تطوير الويب:nodejs npm yarn typescript deno"
    "الأدوات الأساسية:git git-lfs curl wget2 axel aria2"
    "المحررات:neovim emacs nano micro vim-athena"
    "الإدارة:htop btop gotop nmon ncdu"
    "الشبكات:nmap tcpdump iperf3 netcat-openbsd socat"
    
    # من السكربت الثاني
    "أدوات متقدمة:golang-1.20 rustc cargo tmux screen byobu"
    "الشبكات المتقدمة:net-tools inetutils-traceroute mtr iperf3 nload"
    "التخزين:rsync rclone"
)

for category in "${categories[@]}"; do
    name=$(echo $category | cut -d':' -f1)
    packages=$(echo $category | cut -d':' -f2)
    echo -e "\n${GREEN}${BOLD}[+] تثبيت فئة ${name}...${NC}"
    install_packages $packages
done

# ======== المرحلة 4: أدوات الأمان المتقدمة ========
echo -e "\n${RED}${BOLD}[+] تثبيت أدوات الأمان...${NC}"
security_tools=(
    # من السكربت الأول
    "kali-tools-top10 kali-tools-forensics snort suricata"
    
    # من السكربت الثاني
    "masscan zmap thc-ipv6 dnsenum dnsrecon zeek ossec-hids wazuh-agent"
    "volatility rekall autopsy sleuthkit cuckoo-sandbox joomscan wpscan"
    "droopescan rustscan nuclei nexposer wfuzz gauff nuclei-templates"
    "exploitdb payloadsallthethings king-phisher evilginx2 gophish social-engineer-toolkit"
)

install_packages "${security_tools[@]}"

# ======== المرحلة 5: الذكاء الاصطناعي والبيانات ========
echo -e "\n${BLUE}${BOLD}[+] تثبيت أدوات الذكاء الاصطناعي...${NC}"
ai_tools=(
    "python3-tensorflow python3-keras python3-torch"
    "python3-transformers python3-datasets python3-huggingface-hub"
    "jupyterlab jupyter-rsession-proxy r-base rstudio-server spark-master"
    "spark-worker octave julia scala sbt apache-arrow apache-parquet"
    "libcudnn8 libnccl2"
)

install_packages "${ai_tools[@]}"

# ======== المرحلة 6: البلوك تشين والتشفير ========
echo -e "\n${GREEN}${BOLD}[+] تثبيت أدوات البلوك تشين...${NC}"
blockchain_tools=(
    "geth solc truffle ganache hardhat brownie web3.py ethers.js"
    "cryptocurrency-arbitrage defi-bots lightning-network lnd bitcoind monero"
)

install_packages "${blockchain_tools[@]}"

# ======== المرحلة 7: الحاويات والسحابة ========
echo -e "\n${YELLOW}${BOLD}[+] تثبيت أدوات الحاويات...${NC}"
cloud_tools=(
    "docker-ce docker-compose podman kubectl helm terraform packer ansible"
    "kubernetes-client kubernetes-server helm terraform packer ansible"
    "awscli google-cloud-sdk azure-cli kubectx k9s lens rancher minikube kind k3s linkerd"
)

install_packages "${cloud_tools[@]}"

# ======== المرحلة 8: إدارة الحزم الخارجية ========
echo -e "\n${MAGENTA}${BOLD}[+] إعداد Snapd...${NC}"
apt install -y snapd
ln -s /var/lib/snapd/snap /snap
systemctl enable --now snapd

# تطبيقات Snap من كلا السكربتين
snap_apps=(
    "code --classic"
    "intellij-idea-ultimate --classic"
    "pycharm-professional --classic"
    "clion --classic"
    "postman"
    "chromium"
    "brave"
    "dbeaver-ce"
    "kubectl --classic"
    "ngrok"
    "spotify"
    "discord"
    "slack"
)

for app in "${snap_apps[@]}"; do
    snap install $app
done

echo -e "\n${BLUE}${BOLD}[+] إعداد Flatpak...${NC}"
apt install -y flatpak
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

flatpak_apps=(
    "com.jetbrains.PyCharm-Professional"
    "com.visualstudio.code"
    "org.mozilla.firefox"
)

for app in "${flatpak_apps[@]}"; do
    flatpak install -y flathub $app
done

# ======== المرحلة 9: أدوات من GitHub ========
echo -e "\n${GREEN}${BOLD}[+] تثبيت أدوات من GitHub...${NC}"
gh_tools=(
    "https://github.com/aristocratos/bpytop.git"
    "https://github.com/SecureAuthCorp/impacket.git"
    "https://github.com/carlospolop/PEASS-ng.git"
)

mkdir -p ~/Tools
for repo in "${gh_tools[@]}"; do
    git clone ${repo} ~/Tools/$(basename ${repo} .git)
done

# ======== المرحلة 10: إعدادات ما بعد التثبيت ========
echo -e "\n${CYAN}${BOLD}[+] تهيئة البيئة...${NC}"
usermod -aG docker $SUDO_USER
systemctl enable docker postgresql mysql mongod redis
sudo -u $SUDO_USER mkdir -p /home/$SUDO_USER/{Projects,Wordlists,ML_Models}

# تحميل قواعد البيانات
wget https://github.com/danielmiessler/SecLists/archive/master.zip -O ~/Wordlists/SecLists.zip
wget https://github.com/explosion-ai/spacy-models/raw/master/en_core_web_lg/en_core_web_lg-3.5.0.tar.gz -O ~/ML_Models/spacy-model.tar.gz

# إعداد Zsh
apt install -y zsh fonts-powerline
sudo -u $SUDO_USER sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
sudo -u $SUDO_USER git clone https://github.com/zsh-users/zsh-autosuggestions /home/$SUDO_USER/.oh-my-zsh/custom/plugins/zsh-autosuggestions
sudo -u $SUDO_USER git clone https://github.com/zsh-users/zsh-syntax-highlighting /home/$SUDO_USER/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting

# ملف .zshrc مخصص
cat <<EOF > /home/$SUDO_USER/.zshrc
export ZSH="/home/$SUDO_USER/.oh-my-zsh"
ZSH_THEME="agnoster"
plugins=(git docker zsh-autosuggestions zsh-syntax-highlighting)
source \$ZSH/oh-my-zsh.sh
export PATH=\$PATH:/home/$SUDO_USER/.local/bin
neofetch
EOF

# التنظيف النهائي
echo -e "\n${CYAN}${BOLD}[+] تنظيف النظام...${NC}"
apt autoremove -y
apt clean
rm -rf /var/lib/apt/lists/*

#gathhp
git add .gitignore
git commit -m "إضافة ملف env.local إلى gitignore"
git add app/page.tsx app/styles.module.css legacy_pages/ wid.sh y
git commit -m "إضافة ملفات جديدة"
git push origin main



# النتيجة النهائية
echo -e "\n${GREEN}${BOLD}[✔] اكتمل التثبيت بنجاح!${NC}"
echo -e "${BLUE}يحتاج النظام إلى إعادة التشغيل. هل تريد إعادة التشغيل الآن؟ (y/n)${NC}"
read answer
if [ "$answer" != "${answer#[Yy]}" ]; then
    reboot
fi

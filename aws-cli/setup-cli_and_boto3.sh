#!/bin/bash
## setup-cli_and_boto3.sh
# -----------------------------------------------------------------------------
# AWS Tools Setup Script
# Works on: Ubuntu, Amazon Linux 2023, RHEL / CentOS / Rocky / AlmaLinux
# Installs or removes: AWS CLI v2 and Boto3 (Python)
# Usage:
#   ./aws_tools_setup.sh install   -> Install AWS CLI & Boto3
#   ./aws_tools_setup.sh remove    -> Uninstall AWS CLI & Boto3
# -----------------------------------------------------------------------------

set -e

# Detect OS type
detect_os() {
    if grep -qi "amazon linux" /etc/os-release; then
        echo "amazon"
    elif grep -qi "ubuntu" /etc/os-release; then
        echo "ubuntu"
    elif grep -Eqi "rhel|red hat|centos|rocky|alma" /etc/os-release; then
        echo "rhel"
    else
        echo "unknown"
    fi
}

# Install AWS CLI v2
install_aws_cli() {
    echo "🚀 Installing AWS CLI v2..."
    cd /tmp
    curl -s "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip -q awscliv2.zip
    sudo ./aws/install
    rm -rf aws awscliv2.zip
    echo "✅ AWS CLI installed successfully."
    aws --version
}

# Remove AWS CLI
remove_aws_cli() {
    echo "🧹 Removing AWS CLI..."
    sudo rm -rf /usr/local/aws-cli /usr/local/bin/aws /usr/bin/aws
    echo "✅ AWS CLI removed."
}

# Install Boto3
install_boto3() {
    echo "🐍 Installing Python3 & Boto3..."
    OS=$(detect_os)

    if [ "$OS" = "amazon" ]; then
        sudo dnf install -y python3 python3-pip unzip curl
        pip3 install --upgrade pip boto3 botocore

    elif [ "$OS" = "ubuntu" ]; then
        sudo apt update -y
        sudo apt install -y python3-boto3 python3-botocore python3-pip unzip curl

    elif [ "$OS" = "rhel" ]; then
        if command -v dnf &> /dev/null; then
            sudo dnf install -y python3 python3-pip unzip curl
        else
            sudo yum install -y python3 python3-pip unzip curl
        fi
        pip3 install --upgrade pip boto3 botocore

    else
        echo "❌ Unsupported OS."
        exit 1
    fi

    echo "✅ Boto3 installed successfully."
    python3 -m boto3.__version__ 2>/dev/null || python3 -m pip show boto3 | grep Version
}

# Remove Boto3
remove_boto3() {
    echo "🧹 Removing Boto3..."
    OS=$(detect_os)

    if [ "$OS" = "ubuntu" ]; then
        sudo apt remove -y python3-boto3 python3-botocore python3-pip || true
    elif [ "$OS" = "amazon" ] || [ "$OS" = "rhel" ]; then
        pip3 uninstall -y boto3 botocore || true
    else
        echo "❌ Unsupported OS."
        exit 1
    fi

    echo "✅ Boto3 removed."
}

# Main logic
ACTION=$1

if [ "$ACTION" = "install" ]; then
    echo "🔧 Starting installation..."
    install_boto3
    install_aws_cli
    echo "✅ All tools installed successfully."

elif [ "$ACTION" = "remove" ]; then
    echo "🔧 Starting removal..."
    remove_boto3
    remove_aws_cli
    echo "✅ All tools removed successfully."

else
    echo "Usage: $0 {install|remove}"
    exit 1
fi

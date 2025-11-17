# Install code-server, other utilities


```bash
curl -fsSL https://code-server.dev/install.sh | sh
sudo systemctl enable --now code-server@$USER
sleep 5
# add following lines to ~/.config/code-server/config.yaml
cat << EOF > ~/.config/code-server/config.yaml
# ------------------------------
# code-server configuration
bind-addr: 0.0.0.0:8080
auth: password
password: Ravi@123
cert: false
EOF
sudo systemctl restart code-server@$USER

## Install awscli, eksctl, kubectl, helm, jq, yq

# awscli
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version
rm -rf awscliv2.zip aws

#----------------------------------------------------------

# eksctl
# for ARM systems, set ARCH to: `arm64`, `armv6` or `armv7`
ARCH=amd64
PLATFORM=$(uname -s)_$ARCH

curl -sLO "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_$PLATFORM.tar.gz"

# (Optional) Verify checksum
curl -sL "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_checksums.txt" | grep $PLATFORM | sha256sum --check

tar -xzf eksctl_$PLATFORM.tar.gz -C /tmp && rm eksctl_$PLATFORM.tar.gz

sudo install -m 0755 /tmp/eksctl /usr/local/bin && rm /tmp/eksctl

#----------------------------------------------------------

#kubectl 1.34 version 
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.34.1/2025-09-19/bin/linux/amd64/kubectl
chmod +x ./kubectl
mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$HOME/bin:$PATH
echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc

#----------------------------------------------------------

# Helm
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
helm version
rm -f get_helm.sh
#----------------------------------------------------------

# eksctl and kubectl autocompletion
echo "
# Enable kubectl & eksctl autocomplete
source <(kubectl completion bash)
source <(eksctl completion bash)
source <(helm completion bash)
export AWS_CLI_AUTO_PROMPT=on-partial

# Optional: add kubectl alias with autocomplete support
alias k=kubectl
complete -o default -F __start_kubectl k
complete -C "$(which aws_completer)" aws
" >> ~/.bashrc
source ~/.bashrc


# jq and yq
mkdir -p ~/.local/bin
curl -L -o ~/.local/bin/jq https://github.com/jqlang/jq/releases/latest/download/jq-linux-amd64
curl -L -o ~/.local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
chmod +x ~/.local/bin/jq ~/.local/bin/yq
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
jq --version
yq --version
```


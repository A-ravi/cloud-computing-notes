## Using the KMS to encrypt and decrypt data on EC2

```bash
# create a sample text file
echo "Let's encrypt these file contents. Sensitive data here." > data_unencrypted.txt
cat data_unencrypted.txt

# List the KMS keys
aws kms list-keys

# Check the key data
result=$(aws kms generate-data-key --key-id alias/MyKMSKey --key-spec AES_256)
echo $result | python3 -m json.tool

# Extract the plaintext data key and save it to a file

dk_cipher=$(echo $result| jq '.CiphertextBlob' | cut -d '"' -f2)
echo $dk_cipher
echo $dk_cipher | base64 --decode > data_key_ciphertext

# Save the plaintext data key to a file (for demonstration purposes only; do not do this in production)
aws kms decrypt --ciphertext-blob fileb://./data_key_ciphertext --query Plaintext --output text

aws kms decrypt --ciphertext-blob fileb://./data_key_ciphertext --query Plaintext --output text | base64 --decode > data_key_plaintext_encrypted

# Encrypt the data file using the plaintext data key
openssl enc -aes-256-cbc -salt -pbkdf2 -in data_unencrypted.txt -out data_encrypted -pass file:data_key_plaintext_encrypted

cat data_encrypted

rm data_unencrypted.txt

# Decrypt the data file using the plaintext data key
openssl enc -d -aes-256-cbc -pbkdf2 -in data_encrypted -out data_decrypted.txt -pass file:./data_key_plaintext_encrypted

cat data_decrypted.txt
```
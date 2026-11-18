# File Encryption Demo

A Streamlit learning project that shows how password-based file encryption works. Upload a small `.txt` file, encrypt it, and view the encrypted data on the page. Enter the same password to reveal the original text.

## Features

- AES-GCM encryption and decryption
- Scrypt password-based key derivation
- Encrypted and decrypted views on the same page
- Wrong-password and modified-data detection
- No output files saved or downloaded

## Run locally

```powershell
pip install streamlit cryptography
streamlit run app.py --server.port 6541
```

Open `http://localhost:6541`, upload a small `.txt` file, and enter a test password.

## Note

This is an in-memory learning demo. The encrypted result is lost when the Streamlit session ends. Test with sample text rather than important files.
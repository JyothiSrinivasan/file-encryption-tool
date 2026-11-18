import base64
import os

import streamlit as st
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


def make_key(password, salt):
    """Turn a password into a 32-byte AES key."""
    return Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
    ).derive(password.encode("utf-8"))


st.set_page_config(page_title="AES Encryption Demo", page_icon="🔐")
st.title("🔐 File Encryption Demo")
st.write("See a text file encrypted and decrypted on this page.")

uploaded_file = st.file_uploader("Choose a small .txt file", type=["txt"])
password = st.text_input("Password", type="password")

if uploaded_file is not None:
    st.caption(f"Selected file: {uploaded_file.name}")

if st.button("🔒 Encrypt"):
    if uploaded_file is None or not password:
        st.warning("Choose a text file and enter a password.")
    elif uploaded_file.size > 100_000:
        st.warning("Choose a text file smaller than 100 KB for this demo.")
    else:
        plaintext = uploaded_file.getvalue()

        salt = os.urandom(16)
        nonce = os.urandom(12)
        key = make_key(password, salt)
        ciphertext = AESGCM(key).encrypt(nonce, plaintext, None)

        # Keep these in the current Streamlit session, not in a file.
        st.session_state.salt = salt
        st.session_state.nonce = nonce
        st.session_state.ciphertext = ciphertext
        st.session_state.filename = uploaded_file.name
        st.session_state.pop("decrypted_text", None)

        st.success("File encrypted in memory.")

if "ciphertext" in st.session_state:
    encrypted_display = base64.b64encode(
        st.session_state.ciphertext
    ).decode("ascii")

    st.subheader("🔒 Encrypted view")
    st.text_area(
        "Unreadable encrypted data (Base64 display)",
        encrypted_display,
        height=140,
        disabled=True,
    )

    if st.button("🔓 Decrypt"):
        if not password:
            st.warning("Enter the password used for encryption.")
        else:
            try:
                key = make_key(password, st.session_state.salt)
                original_bytes = AESGCM(key).decrypt(
                    st.session_state.nonce,
                    st.session_state.ciphertext,
                    None,
                )
                st.session_state.decrypted_text = original_bytes.decode("utf-8")
                st.success("Decryption successful!")
            except InvalidTag:
                st.error("Wrong password or encrypted data was changed.")
            except UnicodeDecodeError:
                st.error("The recovered file is not valid UTF-8 text.")

if "decrypted_text" in st.session_state:
    st.subheader("📄 Decrypted view")
    st.text_area(
        f"Original contents of {st.session_state.filename}",
        st.session_state.decrypted_text,
        height=180,
        disabled=True,
    )

st.caption(
    "Learning demo: data stays in this browser session. "
    "Closing or resetting the session loses the encrypted result."
)
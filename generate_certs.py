#!/usr/bin/env python3
"""
Generate self-signed SSL certificates for the garage door web app
"""
import os
import subprocess

def main():
    print("Generating SSL certificates for the garage door web app...")
    
    # Create ssl directory if it doesn't exist
    ssl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ssl')
    if not os.path.exists(ssl_dir):
        os.makedirs(ssl_dir)
    
    # Path to certificate files
    cert_path = os.path.join(ssl_dir, 'cert.pem')
    key_path = os.path.join(ssl_dir, 'key.pem')
    
    # Generate a self-signed certificate valid for 10 years
    cmd = [
        'openssl', 'req', '-x509', '-newkey', 'rsa:2048',
        '-keyout', key_path, 
        '-out', cert_path,
        '-days', '3650',
        '-nodes',
        '-subj', '/CN=garagedoor.local'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"SSL certificates generated successfully!")
        print(f"Certificate: {cert_path}")
        print(f"Private key: {key_path}")
        print("\nYour garage door web app is now ready to run with HTTPS support.")
        print("Run 'python3 web.py' to start the server.")
    except subprocess.CalledProcessError as e:
        print(f"Error generating certificates: {e}")
        print("Make sure OpenSSL is installed on your Raspberry Pi.")
        print("You can install it with: sudo apt-get install openssl")

if __name__ == "__main__":
    main()

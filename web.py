import time
from datetime import datetime
from flask import Flask, render_template, request
import os
from OpenSSL import crypto
from flask_cors import CORS

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)  # the pin numbers refer to the board connector not the chip
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.IN, GPIO.PUD_UP) # set up pin ?? (one of the above listed pins) as an input with a pull-up resistor
GPIO.setup(18, GPIO.IN, GPIO.PUD_UP) # set up pin ?? (one of the above listed pins) as an input with a pull-up resistor
GPIO.setup(7, GPIO.OUT)
GPIO.output(7, GPIO.HIGH)
#GPIO.setup(11, GPIO.OUT)
#GPIO.output(11, GPIO.HIGH)
#GPIO.setup(13, GPIO.OUT)
#GPIO.output(13, GPIO.HIGH)
#GPIO.setup(15, GPIO.OUT)
#GPIO.output(15, GPIO.HIGH)

# Function to create self-signed SSL certificates if they don't exist
def create_self_signed_cert():
    cert_dir = os.path.dirname(os.path.abspath(__file__))
    cert_file = os.path.join(cert_dir, "cert.pem")
    key_file = os.path.join(cert_dir, "key.pem")
    
    # Only generate if certificates don't exist
    if os.path.exists(cert_file) and os.path.exists(key_file):
        return cert_file, key_file
        
    # Create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)
    
    # Create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = "US"
    cert.get_subject().ST = "State"
    cert.get_subject().L = "City"
    cert.get_subject().O = "Organization"
    cert.get_subject().OU = "Organizational Unit"
    cert.get_subject().CN = "localhost"
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)  # 10 years
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')
    
    # Save certificate
    with open(cert_file, "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    
    # Save private key
    with open(key_file, "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
    
    return cert_file, key_file

app = Flask(__name__)
# Enable CORS for all routes
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
        return app.send_static_file('Open.html')
        """
        if GPIO.input(16) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH:
             print("Garage is Opening/Closing")
             return app.send_static_file('Question.html')
        else:  
             if GPIO.input(16) == GPIO.LOW:
                   print ("Garage is Closed")
                   return app.send_static_file('Closed.html')
             if GPIO.input(18) == GPIO.LOW:
                   print ("Garage is Open")
                   return app.send_static_file('Open.html')
        """

@app.route('/Gates', methods=['GET', 'POST'])
def Gates():
        # Get the code from the form if it exists
        name = request.form.get('gatescode', '')
        
        # Check if the password is correct
        if name == '12345678':  # 12345678 is the Password that Opens Garage Door
                print("Correct code entered - activating garage door")
                GPIO.output(7, GPIO.LOW)
                time.sleep(1)
                GPIO.output(7, GPIO.HIGH)
                time.sleep(2)
                return app.send_static_file('Open.html')
        else:
                # Handle incorrect or missing password
                if name == "":
                        name = "NULL"
                print("Garage Code Entered: " + name)
                
                # Check door status
                if GPIO.input(16) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH:
                        print("Garage is Opening/Closing")
                        return app.send_static_file('Question.html')
                elif GPIO.input(16) == GPIO.LOW:
                        print("Garage is Closed")
                        return app.send_static_file('Closed.html')
                elif GPIO.input(18) == GPIO.LOW:
                        print("Garage is Open")
                        return app.send_static_file('Open.html')
                
                # Default response if no conditions match
                return app.send_static_file('Question.html')

@app.route('/stylesheet.css')
def stylesheet():
        return app.send_static_file('stylesheet.css')

"""
@app.route('/Log')
def logfile():
        return app.send_static_file('log.txt')
"""

@app.route('/images/<picture>')
def images(picture):
        return app.send_static_file('images/' + picture)

if __name__ == '__main__':
        cert_file, key_file = create_self_signed_cert()
        app.run(ssl_context=(cert_file, key_file), debug=True, host='0.0.0.0', port=5000)

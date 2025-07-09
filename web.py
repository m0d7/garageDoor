import time
from datetime import datetime
from flask import Flask, render_template, request
import os

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)  # the pin numbers refer to the board connector not the chip
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.IN, GPIO.PUD_UP) # set up pin 16 as an input with a pull-up resistor
GPIO.setup(18, GPIO.IN, GPIO.PUD_UP) # set up pin 18 as an input with a pull-up resistor
GPIO.setup(7, GPIO.OUT)
GPIO.output(7, GPIO.HIGH)
#GPIO.setup(11, GPIO.OUT)
#GPIO.output(11, GPIO.HIGH)
#GPIO.setup(13, GPIO.OUT)
#GPIO.output(13, GPIO.HIGH)
#GPIO.setup(15, GPIO.OUT)
#GPIO.output(15, GPIO.HIGH)

app = Flask(__name__)

# Add a route to handle both HTTP and HTTPS requests
@app.route('/', methods=['GET', 'POST'])
def index():
        # This commented out block checks the status of two GPIO pins
        # to determine if the garage is open, closed, or in between.
        """
        if GPIO.input(16) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH:
             print("Garage is Opening/Closing")
             return app.send_static_file('Question.html')
        else:
             if GPIO.input(16) == GPIO.LOW:
                   print("Garage is Closed")
                   return app.send_static_file('Closed.html')
             if GPIO.input(18) == GPIO.LOW:
                   print("Garage is Open")
                   return app.send_static_file('Open.html')
        """
        # For simplicity, the original file was set to always show 'Open.html'
        return app.send_static_file('Open.html')


@app.route('/Gates', methods=['POST'])
def Gates():
        # The password check was commented out in the original file.
        # To re-enable it, uncomment the line below and the if/else blocks.
        # name = request.form['gatescode']

        # This section activates the relay to open the garage.
        GPIO.output(7, GPIO.LOW)
        time.sleep(1)
        GPIO.output(7, GPIO.HIGH)
        time.sleep(2)
        
        # Return a simple JSON response instead of redirecting
        from flask import jsonify
        return jsonify({"success": True})

        # This logic would handle the password check.
        # if name == '12345678':  # 12345678 is the Password that Opens Garage Door (Code if Password is Correct)
        #         GPIO.output(7, GPIO.LOW)
        #         time.sleep(1)
        #         GPIO.output(7, GPIO.HIGH)
        #         time.sleep(2)
        #         if GPIO.input(16) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH:
        #           print("Garage is Opening/Closing")
        #           return app.send_static_file('Question.html')
        #         else:
        #           if GPIO.input(16) == GPIO.LOW:
        #                 print("Garage is Closed")
        #                 return app.send_static_file('Closed.html')
        #           if GPIO.input(18) == GPIO.LOW:
        #                 print("Garage is Open")
        #                 return app.send_static_file('Open.html')

        # if name != '12345678':  # Code if Password is Incorrect
        #         if name == "":
        #                 name = "NULL"
        #         print("Incorrect Garage Code Entered: " + name)
        #         if GPIO.input(16) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH:
        #           print("Garage is Opening/Closing")
        #           return app.send_static_file('Question.html')
        #         else:
        #           if GPIO.input(16) == GPIO.LOW:
        #                 print("Garage is Closed")
        #                 return app.send_static_file('Closed.html')
        #           if GPIO.input(18) == GPIO.LOW:
        #                 print("Garage is Open")
        #                 return app.send_static_file('Open.html')

@app.route('/stylesheet.css')
def stylesheet():
        return app.send_static_file('stylesheet.css')

# The log file route was also commented out.
# @app.route('/Log')
# def logfile():
#        return app.send_static_file('log.txt')


@app.route('/images/<picture>')
def images(picture):
        return app.send_static_file('images/' + picture)

if __name__ == '__main__':
        # Path to the SSL certificate and key files
        cert_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ssl', 'cert.pem')
        key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ssl', 'key.pem')
        
        # Check if SSL certificates exist
        if os.path.exists(cert_path) and os.path.exists(key_path):
                # Run with HTTPS
                app.run(debug=True, host='0.0.0.0', port=443, ssl_context=(cert_path, key_path))
        else:
                print("SSL certificates not found. Running in HTTP mode only.")
                print("For HTTPS support, create an 'ssl' folder and generate cert.pem and key.pem files.")
                # Fall back to HTTP
                app.run(debug=True, host='0.0.0.0', port=5000)
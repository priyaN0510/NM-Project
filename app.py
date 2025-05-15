from flask import Flask, render_template, request, jsonify
import time
from sklearn.linear_model import LogisticRegression

# Try to import GPIO; if not available (e.g., on non-RPi systems), create a fake one
try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    gpio_available = True
except ImportError:
    gpio_available = False
    class FakeGPIO:
        def output(self, pin, value): print(f"[FakeGPIO] Set pin {pin} to {value}")
        def setmode(self, mode): pass
        def setup(self, pin, mode): pass
    GPIO = FakeGPIO()

# App initialization
app = Flask(__name__)
status_state = {'status': 'OFF'}
usage_data = {'usage': 2.5, 'duration': 15}

X_train=[[1.5,20],[2.0,30],[3.5,45],[6.0,90],[7.0,120]]
y_train=[1,1,1,0,0]
model=LogisticRegression()
model.fit(X_train,y_train)


# Serve the frontend
@app.route('/')
def index():
    return render_template('index.html')
# Device status route
@app.route('/status')
def status():
    return jsonify({'status': status_state['status']})

# Simulated usage data route
@app.route('/usage')
def usage():
    usage_data['usage'] += 0.1
    usage_data['duration'] += 3
    return jsonify(usage_data)

# AI Chatbot and Device Control route
@app.route('/chat', methods=['POST'])
def chat():
    msg = request.json.get('message', '').lower()

    # Simple rule-based response
    if "turn on" in msg:
        status_state['status'] = 'ON'
        if gpio_available:
            GPIO.output(18, True)
        return jsonify({'reply': "Device turned ON."})
    elif "turn off" in msg:
        status_state['status'] = 'OFF'
        if gpio_available:
            GPIO.output(18, False)
        return jsonify({'reply': "Device turned OFF."})
    elif "status" in msg:
        return jsonify({'reply': f"The device is currently {status_state['status']}."})
    elif "usage" in msg:
        return jsonify({'reply': f"Current usage is {usage_data['usage']} kWh for {usage_data['duration']} min."})
    else:
        return jsonify({'reply': "I'm an AI assistant for your IoT device. You can say 'turn on', 'turn off', or ask about usage."})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
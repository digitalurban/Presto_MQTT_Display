import time
from presto import Presto
from umqtt.simple import MQTTClient

# Setup for the Presto display
presto = Presto()
display = presto.display
WIDTH, HEIGHT = display.get_bounds()

# MQTT setup
BROKER = "mqtt.cetools.org"  # Replace with your broker
PORT = 1883  # Port for MQTT broker
TOPIC = b"personal/ucfnaps/led/#"  # Replace with your topic
CLIENT_ID = b"PrestoMQTTClient"  # Unique ID for the client

# Initialize the default message
message_string = "Waiting for Messages..."
last_update_time = time.time()
MESSAGE_DISPLAY_DURATION = 20  # Duration to display each message in seconds

# WiFi setup
print("Connecting to WiFi...")
wifi = presto.connect()  # Ensure this is configured for your network
print("WiFi connected.")

# MQTT callback function
def mqtt_callback(topic, msg):
    global message_string, last_update_time
    message_string = msg.decode('utf-8')  # Decode the MQTT message
    last_update_time = time.time()  # Reset the update timer
    print(f"Received message on topic {topic.decode()}: {message_string}")

# MQTT client setup
print(f"Connecting to MQTT broker at {BROKER} on port {PORT}...")
client = MQTTClient(CLIENT_ID, BROKER, port=PORT)
client.set_callback(mqtt_callback)
try:
    client.connect()
    print(f"Successfully connected to MQTT broker at {BROKER}.")
    client.subscribe(TOPIC)
    print(f"Subscribed to topic: {TOPIC.decode()}")
except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")

def draw():
    global message_string
    display.set_font("bitmap8")
    display.set_layer(1)

    # Clear the screen with a black background
    display.set_pen(display.create_pen(0, 0, 0))  # Black background
    display.clear()

    # Display the message
    display.set_pen(display.create_pen(255, 255, 255))  # White text
    x = 10
    y = 35
    line_space = 20
    margin = 10

    # Word wrapping logic
    words = message_string.split()  # Split the message into words
    current_line = ""  # Start with an empty line

    for word in words:
        test_line = current_line + (word + " ")
        line_width = display.measure_text(test_line)

        if line_width > WIDTH - margin:
            display.text(current_line.strip(), x, y, WIDTH)
            y += line_space
            current_line = word + " "  # Start a new line with the current word
        else:
            current_line = test_line

    if current_line:
        display.text(current_line.strip(), x, y, WIDTH)

    presto.update()

# Initialize the background as black and display "Waiting for Messages..."
display.set_layer(0)
display.set_pen(display.create_pen(0, 0, 0))  # Black background
display.clear()
presto.update()

# Draw the initial message
draw()  # Ensure the default message "Waiting for Messages..." is displayed

while True:
    try:
        # Wait for MQTT messages (non-blocking check)
        client.check_msg()

        # Refresh the display periodically
        if time.time() - last_update_time > MESSAGE_DISPLAY_DURATION:
            draw()  # Refresh the screen with the current message
            last_update_time = time.time()

    except Exception as e:
        print(f"Error while waiting for MQTT messages: {e}")

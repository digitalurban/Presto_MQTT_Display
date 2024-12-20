import time
from presto import Presto
from umqtt.simple import MQTTClient

# Setup for the Presto display
presto = Presto()
display = presto.display
WIDTH, HEIGHT = display.get_bounds()

#Make sure you have the Secrets file with wifi details as per the Presto Github Examples

# MQTT setup
BROKER = "mqtt.cetools.org"  # Replace with your broker
PORT = 1883  # Port for MQTT broker
TOPIC = b"personal/ucfnaps/led/#"  # Replace with your topic
CLIENT_ID = b"PrestoMQTTClient"  # Unique ID for the client

message_string = "Waiting for message..."
last_message_time = 0  # Timestamp for when the message was last updated
MESSAGE_DISPLAY_DURATION = 20  # Duration to display each message in seconds
pending_message = None  # Holds new incoming messages until it's time to display them

# WiFi setup
print("Connecting to WiFi...")
wifi = presto.connect()  # Ensure this is configured for your network
print("WiFi connected.")

# MQTT callback function
def mqtt_callback(topic, msg):
    global pending_message
    new_message = msg.decode('utf-8')  # Decode the MQTT message
    print(f"Received message on topic {topic.decode()}: {new_message}")
    pending_message = new_message  # Store the new message to be displayed after 20 seconds

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

def update():
    global message_string, last_message_time, pending_message
    # Poll MQTT messages
    try:
        client.check_msg()  # Non-blocking
    except Exception as e:
        print(f"MQTT error: {e}")

    # Update the message only if 20 seconds have passed since the last update
    current_time = time.time()
    if pending_message and current_time - last_message_time >= MESSAGE_DISPLAY_DURATION:
        message_string = pending_message  # Update the message to the pending one
        pending_message = None  # Clear the pending message
        last_message_time = current_time  # Update the last message time
        print(f"Displayed new message: {message_string}")

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
    line_space = 22
    margin = 10

    # Word wrapping logic
    words = message_string.split()  # Split the message into words
    current_line = ""  # Start with an empty line

    for word in words:
        # Measure the current line with the new word added
        test_line = current_line + (word + " ")
        line_width = display.measure_text(test_line)

        if line_width > WIDTH - margin:
            # If the line exceeds the display width, render the current line and start a new one
            display.text(current_line.strip(), x, y, WIDTH)
            y += line_space
            current_line = word + " "  # Start a new line with the current word
        else:
            # Otherwise, add the word to the current line
            current_line = test_line

    # Render any remaining text in the current line
    if current_line:
        display.text(current_line.strip(), x, y, WIDTH)

    presto.update()

# Initialize the background as black
display.set_layer(0)
display.set_pen(display.create_pen(0, 0, 0))  # Black background
display.clear()
presto.update()

while True:
    print("Checking for MQTT messages and updating display...")
    update()
    draw()
    print("Update complete. Waiting...")
    time.sleep(1)  # Check for messages and update every second

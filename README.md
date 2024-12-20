
# MQTT Message Display with Word Wrapping on Presto Display


This repository contains Python code designed to display messages received via MQTT on a [Beta Presto Display](https://shop.pimoroni.com/products/presto?variant=54894104019323). It includes a feature to word-wrap messages, ensuring text stays within the screen boundaries.

## Features

- **MQTT Integration**: Subscribes to an MQTT topic and displays received messages on the screen.
- **Word Wrapping**: Automatically wraps text to fit within the display width.
- **Customizable Display**: Messages are shown in white text on a black background.
- **Message Timing**: Ensures each message is displayed for at least 20 seconds.

## Requirements

- **Hardware**:
  - Presto Display
  - Microcontroller compatible with Presto Display (e.g., Raspberry Pi Pico W)
- **Software**:
  - MicroPython firmware
  - `umqtt.simple` library for MQTT communication

## Installation

1. Clone or download this repository:
   ```bash
   git clone https://github.com/your-username/presto-mqtt-display.git
   ```
   Or download the ZIP file directly from GitHub.

2. Upload the files to your device using a tool like [Thonny](https://thonny.org/), [ampy](https://github.com/scientifichackers/ampy), or [rshell](https://github.com/dhylands/rshell).

3. Customize the MQTT broker, port, and topic in the code (our example code points to our own broker with messages displayed every 3 minutes).
   ```python
   BROKER = "your-mqtt-broker-address"
   PORT = 1883  # Port number
   TOPIC = b"your/topic/#"  # MQTT topic
   ```

4. Run the code on your device.

## Usage

1. Connect your device to Wi-Fi. Ensure the Presto Display is properly connected and configured.
2. The device will connect to the specified MQTT broker and subscribe to the defined topic.
3. Incoming messages will be displayed on the screen for 20 seconds each. Text will be word-wrapped if it exceeds the display width.

## Example

Below is an example of the output for a message that is too long to fit on one line:

```
Hello world this is
a long message that
wraps nicely!
```

## Code Highlights

The key feature of this repository is the `draw()` function, which handles word wrapping and rendering messages on the Presto Display:

```python
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
```

## Contributing

Feel free to fork the repository, open issues, or submit pull requests to improve functionality or add features.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

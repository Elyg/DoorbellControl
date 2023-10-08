from gpiozero import Button, DigitalOutputDevice
from signal import pause


GPIO_RELAY = 17
GPIO_BUTTON = 2
DEVICE_RELAY = DigitalOutputDevice(pin=GPIO_RELAY)

def relay_turn_on():
    DEVICE_RELAY.on()
    print("Relay ON!")
    
def relay_turn_off(relay=None):
    DEVICE_RELAY.off()
    print("Relay OFF!")
    
button = Button(GPIO_BUTTON)

button.when_pressed = relay_turn_on
button.when_released = relay_turn_off

pause()
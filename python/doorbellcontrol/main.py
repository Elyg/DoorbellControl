from gpiozero import Button, DigitalOutputDevice
from signal import pause

GPIO_BUTTON = 2
GPIO_RELAY = 17
DEVICE_RELAY = DigitalOutputDevice(pin=GPIO_RELAY, active_high=False)

def relay_turn_on():
    DEVICE_RELAY.on()
    print("Relay ON! {}".format(DEVICE_RELAY.value))
    
def relay_turn_off():
    DEVICE_RELAY.off()
    print("Relay OFF! {}".format(DEVICE_RELAY.value))
    
button = Button(GPIO_BUTTON)

button.when_pressed = relay_turn_on
button.when_released = relay_turn_off

pause()
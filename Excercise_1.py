from tkgpio import TkCircuit

configuration = {
    "width": 300,
    "height": 200,
    "leds": [
        {"x": 50, "y": 40, "name": "LED 1", "pin": 21},
        {"x": 100, "y": 40, "name": "LED 2", "pin": 22},
        {"x": 150, "y": 40, "name": "LED 3", "pin": 23},
    ],
    "buttons": [
        {"x": 50, "y": 130, "name": "BT1", "pin": 11},
        {"x": 100, "y": 130, "name": "BT2", "pin": 12},
        {"x": 150, "y": 130, "name": "STOP!", "pin": 13},
    ]
}
circuit = TkCircuit(configuration)


@circuit.run
def main():
###################################################### Import ##########################################################

    from gpiozero import LED, Button, PWMLED
    from time import sleep
####################################################### Setup ##########################################################

    def setup_led() -> tuple:
        """
        Set Up all LEDs
        :return: led1, led2, led3
        """
        led1 = LED(21)
        led2 = LED(22)
        led3 = PWMLED(23)
        return led1, led2, led3

    def setup_button() -> tuple:
        """
        Set Up all Buttons
        :return: button1, button2, stop_button
        """

        button1 = Button(pin=11)
        button2 = Button(pin=12, hold_time=1)
        stop_button = Button(pin=13, hold_time=1)
        return button1, button2, stop_button

######################################################### Run ##########################################################
    led1, led2, led3 = setup_led()
    button1, button2, stop_button = setup_button()

    def button_1_pressed() -> None:
        """
        LED1 on/off and blink
        :return:  None
        """
        print("LED1!")
        led1.off() if led1.is_lit else led1.blink(on_time=0.1, off_time=0.1)

    def button_2_held() -> None:
        """
        LED2 on/off
        :return: None
        """
        print("button 2 held!")
        led2.off() if led2.is_lit else led2.on()

    def stop_3_held():
        """
        Turn of LED1, LED2,
        LED3 on/off and pulse
        :return: None
        """
        led1.off()
        led2.off()
        led3.off() if led3.is_lit else led3.pulse(fade_in_time=0.5, fade_out_time=0.5),print("Stop!")

    button1.when_pressed = button_1_pressed
    button2.when_held = button_2_held
    stop_button.when_held = stop_3_held

    while True:
        sleep(0.1)

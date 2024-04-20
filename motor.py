from machine import Pin
import utime


class Motor28BYJ:
    def __init__(self,step_index=0,step_sequence=None,stepper_pins=None):
        # Define the sequence of steps for the motor to take
        if step_sequence:
            self.step_sequence=step_sequence
        else:
            self.step_sequence = [
                [1, 0, 0, 0],
                [1, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 1],
                [0, 0, 0, 1],
                [1, 0, 0, 1]
                ]
        if stepper_pins:
            self.stepper_pins=stepper_pins
        else:
            self.stepper_pins = [Pin(12, Pin.OUT), Pin(13, Pin.OUT), Pin(14, Pin.OUT), Pin(15, Pin.OUT)]
        self.step_index = step_index
    def step(self,direction, steps, delay):
        # Use the global step_index variable so that it can be modified by this function
        # Loop through the specified number of steps in the specified direction
        for i in range(steps):
            # Add the specified direction to the current step index to get the new step index
            self.step_index = (self.step_index + direction) % len(self.step_sequence)
        # Loop through each pin in the motor
            for pin_index in range(len(self.stepper_pins)):
                # Get the value for this pin from the step sequence using the current step index
                pin_value = self.step_sequence[self.step_index][pin_index] 
                # Set the pin to this value
                self.stepper_pins[pin_index].value(pin_value)
            # Delay for the specified amount of time before taking the next step
            utime.sleep(delay)
    def clean(self):
        for pin in self.stepper_pins:
            pin.value(0)

if __name__=='__main__':
    m = Motor28BYJ()
    # Take the specified number of steps in the anti-clockwise direction with a delay of 0.01 seconds between steps
    m.step(1, 4100, 0.001)
    # Set the out pins of motor to 0
    m.clean()


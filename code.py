import board
import neopixel
import digitalio
from analogio import AnalogIn, AnalogOut
import lib.seeed_xiao_nrf52840
import ew_uart as ua
from LED_Control import LED_Control
from trueClock import trueClock
import time

ua.setup("NLighten")

ldr = AnalogIn(board.A1)

ldrOut = digitalio.DigitalInOut(board.D9)
ldrOut.direction = digitalio.Direction.OUTPUT
ldrOut.value =  True

led = neopixel.NeoPixel(board.D10, 7, auto_write = False, bpp=4)
led.brightness = 0.1
# imu = seeed_xiao_nrf52840.IMU()
# bat = lib.seeed_xiao_nrf52840.Battery()
# print(f"Charge complete: {bat.charge_status}")
# print(f"Voltage: {bat.voltage}")
# print(f"Charge_current high?: {bat.charge_current}")
# print("Setting charge current to high")
# bat.charge_current = bat.CHARGE_100MA
# print(f"Charge_current high?: {bat.charge_current}")

# for i in range(7):
#     led[i] = (0,255,0,0)
#     time.sleep(0.5)
#     led[i] = (255,0,0,0)
#     time.sleep(0.5)
#     led[i] = (0,0,255,0)
#     time.sleep(0.5)
#     led[i] = (0,0,0,255)
#     time.sleep(0.5)
    
ONE_THIRD = 1.0 / 3.0
ONE_SIXTH = 1.0 / 6.0
TWO_THIRD = 2.0 / 3.0

LED_Controls = LED_Control(led, ldr)
clock = trueClock("2026-06-02T06:56:40.127")
counter = 0
bleOff = False

while True:
    if not ua.connected() and not bleOff:
        ua.start_advertising()
    if ua.connected():
        counter += 1
        # print(ldr.value, LED_Controls.ldrAverageVal)
        if counter > 250000: 
            ua.disconnect()
            counter = 0
            continue
        if counter % 1000 == 0:
            ua.write(f"LDR Val: {round(ldr.value/65535, 2)}%, {ldr.value}, avg: {LED_Controls.ldrAverageVal}")
            # ua.write(f"Battery:{bat.voltage}v")
            # ua.write(f"Charge Complete: {bat.charge_status}")
        if ua.in_waiting():
            data = ua.read(ua.in_waiting())
            if data:
                text = data.decode("utf-8").strip()
                # print("Text Sent: ", text)
                button = ua.button_press(data)
                
                # Handle brightness controls
                if button == "DOWN":
                    LED_Controls.brightness = max(0, LED_Controls.brightness - 0.05)
                    ua.write(f"Brightness: {LED_Controls.brightness}")
                elif button == "UP":
                    LED_Controls.brightness = min(1, LED_Controls.brightness + 0.05)
                    ua.write(f"Brightness: {LED_Controls.brightness}")
                # Handle mode navigation
                elif button == "LEFT":
                    LED_Controls.previousMode()
                elif button == "RIGHT":
                    LED_Controls.nextMode()
                
                # Handle manual controls
                elif button == "1":
                    # Button 1: Decrease hue in color modes / Decrease white_balance in white modes
                    current_mode = LED_Controls.currentMode
                    if current_mode == LED_Control.allWhite or current_mode == LED_Control.singleAllWhite:
                        LED_Controls.adjust_white_balance(-LED_Controls.white_step)
                        ua.write(f"White balance: {round(LED_Controls.white_balance * 100)}% W")
                    else:
                        LED_Controls.adjust_hue(-LED_Controls.hue_step)
                        ua.write(f"Hue: {round(LED_Controls.hsv[0] * 360)}°")
                        
                elif button == "2":
                    # Button 2: Increase hue in color modes / Increase white_balance in white modes
                    current_mode = LED_Controls.currentMode
                    if current_mode == LED_Control.allWhite or current_mode == LED_Control.singleAllWhite:
                        LED_Controls.adjust_white_balance(LED_Controls.white_step)
                        ua.write(f"White balance: {round(LED_Controls.white_balance * 100)}% W")
                    else:
                        LED_Controls.adjust_hue(LED_Controls.hue_step)
                        ua.write(f"Hue: {round(LED_Controls.hsv[0] * 360)}°")
                        
                elif button == "3":
                    # Button 3: Decrease saturation (color modes only)
                    LED_Controls.adjust_saturation(-LED_Controls.sat_step)
                    ua.write(f"Saturation: {round(LED_Controls.hsv[1] * 100)}%")
                    
                elif button == "4":
                    # Button 4: Increase saturation (color modes only)
                    LED_Controls.adjust_saturation(LED_Controls.sat_step)
                    ua.write(f"Saturation: {round(LED_Controls.hsv[1] * 100)}%")
                    
                elif text == "ble::disable":
                    ua.write("BLUETOOTH RECONNECTION DISABLED")
                    bleOff = True
                elif text == "ble::enable":
                    ua.write("BLUETOOTH RECONNECTION ENABLED")
                    bleOff = False
                elif text == "DC::T":
                    ua.disconnect()
                elif text[:14] == "setthreshold::":
                    LED_Controls.threshold = [int(i) for i in text[14:].split(",")]
                    ua.write(f"Thrshld: {LED_Controls.threshold}")
                elif text[:9] == "setmode::":
                    # print(text[9:]) 
                    LED_Controls.setMode(text[9:])
                elif text[:11] == "setbright::":
                    LED_Controls.brightness = min(max(0, float(text[11:])), 1)
                    ua.write(f"Brightness set to {LED_Controls.brightness*100}%")
                elif text[:8] == "sethue::":
                    LED_Controls.hsv[0] = max(0.0, min(1.0, float(text[8:])))
                    ua.write(f"Hue: {round(LED_Controls.hsv[0] * 360)}°")
                elif text[:15] == "setsaturation::":
                    LED_Controls.hsv[1] = max(0.0, min(1.0, float(text[15:])))
                    ua.write(f"Saturation: {round(LED_Controls.hsv[1] * 100)}%")
                elif text[:9] == "setvalue::":
                    LED_Controls.hsv[2] = float(text[9:])
                    ua.write(f"Value: {round(LED_Controls.hsv[2] * 100)}%")
                elif text[:17] == "setwhitebalance::":
                    LED_Controls.set_white_balance(text[17:])
                    ua.write(f"White balance: {round(LED_Controls.white_balance * 100)}% W")
                elif text[:9] == "settime::":
                    clock.storeTime(text[9:])
                    ua.write(f"Time set to: {clock.getTime()}")
                elif text not in ["!B705", "!B507", "!B804", "!B606", "!B10", "!B20", "!B309", "!B408"]:
                    ua.write("Invalid Command!")
                
    LED_Controls.runCurrentMode()
    led.show()
import time
import math
import random
import board
import neopixel
import digitalio
from analogio import AnalogIn, AnalogOut
import lib.seeed_xiao_nrf52840
import ew_uart as ua
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

class LED_Control:
    def __init__(self):
        self.hsv = [0,1,1]
        self.direction = 1
        self.brightness = 0.75
        self.counter = 0
        self.threshold = [100, 10000]
        self.onTime = time.time()
        self.ldrAverage = [1000]
        self.ldrAverageVal = 1000
        self.on = True
        
        self.white_balance = 0.5
        self.white_step = 0.025
        self.hue_step = 0.025
        self.sat_step = 0.025

        self.currentMode = LED_Control.singleAllWhite
        led.brightness = self.brightness
        self.modes = [LED_Control.rainbowHueFade, LED_Control.allWhite, 
                    LED_Control.singleWhite, LED_Control.rgbWhite, 
                    LED_Control.singleAllWhite, LED_Control.singleRainbowHueFade,
                    LED_Control.breathingEffect, LED_Control.sparkleEffect,
                    LED_Control.fireEffect, LED_Control.colorWipeEffect,
                    LED_Control.pulseEffect, LED_Control.rainbowCycle,
                    LED_Control.starburstEffect, LED_Control.meteorEffect,
                    LED_Control.waterEffect, LED_Control.multicolorStrobe,
                    LED_Control.gradientEffect, LED_Control.nightSkyEffect,
                    LED_Control.autumnEffect, LED_Control.heartbeatEffect,
                    LED_Control.auroraEffect, LED_Control.simpleColor,
                    LED_Control.singleSimpleColor]

    def hsv_to_rgb(self):
        h, s, v = self.hsv
        if s == 0.0:
            returnVal = v, v, v
        i = int(h*6.0) 
        f = (h*6.0) - i
        p = v*(1.0 - s)
        q = v*(1.0 - s*f)
        t = v*(1.0 - s*(1.0-f))
        i = i%6
        if i == 0:
            returnVal = (v, t, p)
        if i == 1:
            returnVal = (q, v, p)
        if i == 2:
            returnVal = (p, v, t)
        if i == 3:
            returnVal = (p, q, v)
        if i == 4:
            returnVal = (t, p, v)
        if i == 5:
            returnVal = (v, p, q)
        return [x*255 for x in returnVal]

    def adjust_hue(self, increment):
        self.hsv[0] = (self.hsv[0] + increment) % 1.0
        
    def adjust_saturation(self, increment):
        self.hsv[1] = max(0.0, min(1.0, self.hsv[1] + increment))
        
    def adjust_white_balance(self, increment):
        self.white_balance = max(0.0, min(1.0, self.white_balance + increment))
        
    def runCurrentMode(self):
        self.ldrAverage.append(ldr.value)
        self.ldrAverage = self.ldrAverage[-100:]
        self.ldrAverageVal = sum(self.ldrAverage)/len(self.ldrAverage)
        if self.ldrAverageVal <= self.threshold[0] and self.brightness != 0:
            if led.brightness == 0: self.onTime = time.time()
            led.brightness = (1/99)*((100**self.brightness)-1)
            self.on = True
        elif self.ldrAverageVal >= self.threshold[1] and self.onTime+1 < time.time():
            led.brightness = 0 
            self.on = False
        elif self.threshold[0] <= self.ldrAverageVal <= self.threshold[1] and self.on:
            led.brightness = (1/99)*((100**self.brightness)-1)
        self.currentMode(self)
        
    def setMode(self, mode):
        try:
            if 0<= abs(int(mode)) < len(self.modes):
                self.currentMode = self.modes[int(mode)]
        except:
            try:
                for m in self.modes:
                    if m.__name__ == mode:
                        self.currentMode = m
            except:pass
        for i in range(7):
            led[i] = (0,0,0,0)
        
    def nextMode(self):
        currentIndex = self.modes.index(self.currentMode)
        if currentIndex+1 < len(self.modes):
            self.currentMode = self.modes[currentIndex+1]
        else:
            self.currentMode = self.modes[0]
        for i in range(7):
            led[i] = (0,0,0,0)
        
    def previousMode(self):
        currentIndex = self.modes.index(self.currentMode)
        if currentIndex-1 >= 0:
            self.currentMode = self.modes[currentIndex-1]
        else:
            self.currentMode = self.modes[len(self.modes)-1]
        for i in range(7):
            led[i] = (0,0,0,0)
   
    def rainbowHueFade(self):
        self.hsv[0] += 0.001*self.direction
        if self.hsv[0]>= 1:
            self.direction = -1
        elif self.hsv[0]<=0:
            self.direction = 1
        for i in range(7):
            led[i] = self.hsv_to_rgb()
        
    def singleRainbowHueFade(self):
        self.hsv[0] += 0.001*self.direction
        if self.hsv[0]>= 1:
            self.direction = -1
        elif self.hsv[0]<=0:
            self.direction = 1
        led[0] = self.hsv_to_rgb()

    def allWhite(self):
        rgb_intensity = int(255 * (1.0 - self.white_balance))
        w_intensity = int(255 * self.white_balance)
        if rgb_intensity == w_intensity: rgb_intensity, w_intensity = (255,255)
        for i in range(7):
            led[i] = (rgb_intensity, rgb_intensity, rgb_intensity, w_intensity)
    
    def singleWhite(self):
        for i in range(7):
            led[i] = (0,0,0,255)

    def rgbWhite(self):
        for i in range(7):
            led[i] = (255,255,255,0)

    def singleAllWhite(self):
        rgb_intensity = int(255 * (1.0 - self.white_balance))
        w_intensity = int(255 * self.white_balance)
        if rgb_intensity == w_intensity: rgb_intensity, w_intensity = (255,255)
        led[0] = (rgb_intensity, rgb_intensity, rgb_intensity, w_intensity)

    def simpleColor(self):
        for i in range(7):
            led[i] = self.hsv_to_rgb()
            
    def singleSimpleColor(self):
        led[0] = self.hsv_to_rgb()

    def basicTest(self):
        for i in range(7):
            led[i] = (0,255,0,0)
            time.sleep(0.5)
            led[i] = (255,0,0,0)
            time.sleep(0.5)
            led[i] = (0,0,255,0)
            time.sleep(0.5)
            led[i] = (0,0,0,255)
            time.sleep(0.5)
        
    # effects below made with Claude 3.7

    def breathingEffect(self):
        """Creates a breathing effect where all LEDs fade in and out together"""
        # Use counter as a timer
        self.counter += 1
        # Create a sine wave pattern for smooth breathing
        breath_value = (math.sin(self.counter / 50) + 1) / 2  # 0.0 to 1.0
        
        # Get the base color from HSV
        r, g, b = self.hsv_to_rgb()
        # Apply breathing intensity to RGB values
        for i in range(7):
            led[i] = (int(r * breath_value), int(g * breath_value), int(b * breath_value), 0)

    def sparkleEffect(self):
        """Random LEDs light up with twinkling effect"""
        # Dim all LEDs slightly each cycle
        for i in range(7):
            r, g, b, w = led[i]
            led[i] = (max(0, int(r*0.94)), max(0, int(g*0.94)), max(0, int(b*0.94)), max(0, int(w*0.94)))
        
        # Randomly light up 1-2 LEDs
        if random.random() < 0.2:  # 20% chance to add a sparkle
            # Pick a random LED
            pixel = random.randint(0, 6)
            # Pick a random color with more white for sparkle effect
            r, g, b = self.hsv_to_rgb()
            white = random.randint(70, 200)
            led[pixel] = (r, g, b, white)

    def fireEffect(self):
        """Creates a vivid red-orange fire effect with dynamic flames"""
        # Advance counter for time-based variations
        self.counter += 1
        
        # For each pixel
        for i in range(7):
            # Create a dynamic flicker effect with more variation
            # Use sine wave for additional movement + random flicker
            flicker_base = (math.sin(self.counter/20 + i*1.5) + 1) / 2  # 0.0 to 1.0, varies by position
            flicker_random = random.random() * 0.4  # Add randomness (0.0 to 0.4)
            flicker = min(1.0, flicker_base + flicker_random)  # Combined flicker effect
            
            # Full red base for all pixels
            r = 255
            
            # Significantly reduced green component for more orange-red appearance
            # Keep enough to create orange but not yellow
            g = int(70 * flicker + 10)  # 10-80 range, much lower than before
            
            # No blue for pure red-orange appearance
            b = 0
            
            # Add occasional red-orange embers
            w = random.randint(10, 60) if random.random() < 0.2 else 0
            
            # Use different intensities based on LED position
            # Center LED is the "hottest" part of the flame
            intensity_factor = 1.0 if i == 0 else 0.7 + (0.3 * random.random())
            
            # Heighten the effect with occasional bright flares
            if random.random() < 0.08:  # 8% chance of a bright flare
                intensity_factor = 1.3
                # For intense flares, add a tiny bit more green for visual impact
                g = int(g * 1.2)
            
            # Apply intensity factor to all components
            r = min(255, int(r * intensity_factor))
            g = min(255, int(g * intensity_factor))
            
            led[i] = (r, g, b, w)
            time.sleep(0.01)

    def colorWipeEffect(self):
        """Colors wipe across all LEDs with a trail effect"""
        # Advance counter
        self.counter += 1
        
        # Switch colors every full cycle
        if self.counter % 140 == 0:
            self.hsv[0] = (self.hsv[0] + 0.1) % 1.0
        
        # Get the base color from HSV
        r, g, b = self.hsv_to_rgb()
        
        # Create a trailing effect where multiple LEDs are lit with fading intensity
        for i in range(7):
            # Calculate position relative to the current active LED
            position = (i - (self.counter // 20) % 7)
            # Wrap around for continuous effect
            if position < 0:
                position += 7
            
            # Create trail with fading intensity
            if position <= 2:  # Length of trail (0 = active LED, 1 & 2 = trailing LEDs)
                intensity = 1.0 - (position * 0.4)  # Fade out in trail (100%, 60%, 20%)
                led[i] = (int(r * intensity), int(g * intensity), int(b * intensity), 0)
            else:
                led[i] = (0, 0, 0, 0)  # Off

    def pulseEffect(self):
        """Creates expanding circles of light from center outward"""
        # Advance counter
        self.counter += 1
        
        # Create waves that emanate from the center
        wave_position = (self.counter % 60) / 60.0  # 0.0 to 1.0
        
        # Generate color with slight variation based on time
        self.hsv[0] = (self.hsv[0] + 0.001) % 1.0
        r, g, b = self.hsv_to_rgb()
        
        # Center LED (position 0) always glows softly
        center_intensity = 0.3 + 0.2 * math.sin(self.counter / 30)  # Subtle breathing effect
        led[0] = (int(r * center_intensity), int(g * center_intensity), int(b * center_intensity), 0)
        
        # Outer LEDs (positions 1-6) show expanding wave
        for i in range(1, 7):
            # Calculate intensity based on wave position - this creates the expanding circle effect
            # When wave_position is between 0.0-0.3, the wave is expanding outward
            distance = wave_position * 2.0  # Scale to get appropriate wave width
            
            # Create a pulse that fades based on distance from the "wave front"
            intensity = max(0, 1.0 - abs(distance - 0.5))
            
            # Apply intensity to all outer LEDs simultaneously (creating an expanding circle)
            led[i] = (int(r * intensity), int(g * intensity), int(b * intensity), 0)
        time.sleep(0.01)
        
    def rainbowCycle(self):
        """Rainbow colors cycle around the outer ring, with a different color in the center"""
        # Advance counter
        self.counter += 1
        
        # Get the base hue and calculate offset
        base_hue = (self.counter / 500) % 1.0
        
        # Set center LED to complementary color
        center_hue = (base_hue + 0.5) % 1.0
        self.hsv[0] = center_hue
        r, g, b = self.hsv_to_rgb()
        led[0] = (r, g, b, 0)
        
        # Set outer LEDs in rainbow pattern
        for i in range(1, 7):
            # Calculate offset for this LED
            led_hue = (base_hue + ((i - 1) / 6.0)) % 1.0
            self.hsv[0] = led_hue
            r, g, b = self.hsv_to_rgb()
            led[i] = (r, g, b, 0)

    def starburstEffect(self):
        """Creates a starburst effect with rapid fade-out"""
        
        # Randomly trigger a new starburst
        if random.random() < 0.005 or self.counter == 0:  # 0.5% chance or first run
            # Reset counter for timing
            self.counter = 1
            # Set a new random hue
            self.hsv[0] = random.random()
            
        # Advance counter
        self.counter += 1
        
        # Calculate intensity based on counter (quick fade out)
        intensity = max(0, 1.0 - (self.counter / 30))
        
        if intensity > 0:
            # Get the base color from HSV
            r, g, b = self.hsv_to_rgb()
            
            # Set all LEDs to the color with calculated intensity
            for i in range(7):
                led[i] = (int(r * intensity), int(g * intensity), int(b * intensity), int(255 * intensity / 3))
        else:
            # Turn off all LEDs when effect ends
            for i in range(7):
                led[i] = (0, 0, 0, 0)
                
    def meteorEffect(self):
        """Creates a meteor shower effect with trails falling across the LEDs at a slower pace"""
        # Advance counter much more slowly
        if self.counter % 3 == 0:  # Only increment every 3rd frame
            self.counter += 1
        
        # Fade all LEDs slightly each cycle for trail effect
        # Use a much gentler fade rate for slower trails
        for i in range(7):
            r, g, b, w = led[i]
            led[i] = (max(0, int(r*0.95)), max(0, int(g*0.95)), max(0, int(b*0.95)), max(0, int(w*0.95)))
        
        # Create new meteor at much lower random intervals
        if random.random() < 0.02 or self.counter == 1:  # 2% chance (was 8%)
            # Select random LED for meteor head
            meteor_head = random.randint(1, 6)  # Excluding center LED
            
            # Generate random meteor color (white to blue-white)
            r = random.randint(180, 255)
            g = random.randint(180, 255)
            b = 255  # Full blue for all meteors
            w = random.randint(100, 255)  # White component
            
            # Apply meteor to selected LED
            led[meteor_head] = (r, g, b, w)

    def waterEffect(self):
        """Creates a flowing water/ocean wave effect with rich blues and occasional seafoam"""
        # Advance counter much more slowly for gentler waves
        self.counter += 1
        
        # Base wave frequency and amplitude (slowed down significantly)
        wave_freq = self.counter / 30  # Was /30
        
        for i in range(7):
            # Create different wave patterns for each LED
            wave1 = (math.sin(wave_freq + i * 0.3) + 1) / 2
            wave2 = (math.sin(wave_freq * 0.7 + i * 0.5) + 1) / 2
            wave3 = (math.cos(wave_freq * 0.4 + i * 0.6) + 1) / 2
            
            # Combine waves for more complex pattern
            combined_wave = (wave1 * 0.5 + wave2 * 0.3 + wave3 * 0.2)
            
            # More color variation in the blues and greens
            # Determine if this is a deep or shallow water area
            water_depth = random.random() if self.counter % 120 == 0 else (i % 3) / 3
            
            if water_depth < 0.3:  # Deep water - darker blue
                r = int(5 + 15 * combined_wave)
                g = int(20 + 60 * combined_wave)
                b = int(120 + 135 * combined_wave)
            elif water_depth < 0.6:  # Medium depth - blue-green
                r = int(5 + 10 * combined_wave)
                g = int(70 + 90 * combined_wave)
                b = int(100 + 120 * combined_wave)
            else:  # Shallow water - more teal/aqua
                r = int(10 + 20 * combined_wave)
                g = int(100 + 110 * combined_wave)
                b = int(120 + 100 * combined_wave)
            
            # Add white foam/sparkle occasionally with more variation
            foam_chance = 0.003 + (wave1 * 0.008)  # Higher chance during wave peaks
            if random.random() < foam_chance:
                foam_intensity = random.randint(20, 80)
                w = foam_intensity
                # Lighten the blue/green for foam areas
                g = min(255, g + int(foam_intensity * 0.5))
                b = min(255, b + int(foam_intensity * 0.3))
            else:
                w = 0
            
            led[i] = (r, g, b, w)

    def multicolorStrobe(self):
        """Creates a multicolored strobe effect with rapid color changes"""
        # Advance counter
        self.counter += 1
        
        # Determine if LEDs should be on or off (strobe effect)
        if self.counter % 5 < 2:  # 2 frames on, 3 frames off for strobe effect
            # Every 5 full cycles, change the color
            if (self.counter // 5) % 5 == 0:
                self.hsv[0] = (self.hsv[0] + 0.17) % 1.0  # Large hue jump for distinct colors
            
            # Get current color
            r, g, b = self.hsv_to_rgb()
            
            # Apply color to all LEDs
            for i in range(7):
                led[i] = (r, g, b, 0)
        else:
            # Turn all LEDs off for strobe effect
            for i in range(7):
                led[i] = (0, 0, 0, 0)

    def gradientEffect(self):
        """Creates a smooth gradient that rotates around the outer LEDs with center as accent"""
        # Advance counter more slowly
        self.counter += 1
        
        # Define gradient starting point that slowly rotates
        angle = (self.counter / 200) % (2 * math.pi)
        
        # For each LED, calculate a position in the gradient
        for i in range(7):
            if i == 0:  # Center LED
                # Make center LED pulse slowly with a contrasting color
                pulse = (math.sin(self.counter / 100) + 1) / 2
                # Use gold/amber for center to contrast with outer gradient
                r = int(255 * pulse)
                g = int(150 * pulse)
                b = int(20 * pulse)
                led[0] = (r, g, b, 0)
            else:
                # Calculate position around circle for outer LEDs (1-6)
                # Each outer LED is 60 degrees (π/3 radians) apart
                led_angle = ((i - 1) * math.pi / 3)
                
                # Calculate gradient position based on angle difference
                # This creates a smooth gradient that rotates around the circle
                angle_diff = (led_angle - angle) % (2 * math.pi)
                gradient_pos = angle_diff / (2 * math.pi)
                
                # Map gradient position to a color (using HSV for smooth transitions)
                # Use a limited color range for better visual effect (e.g., blues to purples)
                hue = (0.5 + gradient_pos * 0.5) % 1.0  # Limit to half the color wheel
                
                # Set hue and get RGB values
                self.hsv[0] = hue
                self.hsv[1] = 0.9  # High saturation
                r, g, b = self.hsv_to_rgb()
                
                led[i] = (r, g, b, 0)
            
    def nightSkyEffect(self):
        """Creates a night sky effect with slowly twinkling stars on deep blue background"""
        # Counter for occasional changes
        self.counter += 1
        
        # Slow down the twinkling rate by only updating some LEDs each frame
        r, g, b = 0, 0, 40
            
        if self.counter % 250 == 0 and len([False for i in range(7) if led[i][3] > 0]) == 0 : update_led = random.randint(0,6)
        else: update_led = None
        
        # Deep blue base for all LEDs (night sky)
        for i in range(7):
            # Get current values
            current_r, current_g, current_b, current_w = led[i]
            if self.counter % 10 == 0:
                w = max(0, min(50, int(current_w - 1)))
            else: w = current_w
            
            # Only process one LED per frame for slower changes
            if update_led and i == update_led:
                w = 50
                
            led[i] = (r, g, b, w)

    def autumnEffect(self):
        """Creates an autumn leaves effect with warm orange, red, and gold colors"""
        # Advance counter
        self.counter += 1
        
        # For each LED
        for i in range(7):
            # Determine a random autumn color for each LED, changing occasionally
            if self.counter % 60 == 0 or (i == self.counter % 7 and self.counter % 20 == 0):
                # Select from autumn palette (red, orange, gold, brown)
                color_choice = random.randint(0, 3)
                
                if color_choice == 0:  # Red
                    r, g, b = 255, 40, 0
                elif color_choice == 1:  # Orange
                    r, g, b = 255, 100, 0
                elif color_choice == 2:  # Gold/Yellow
                    r, g, b = 255, 180, 0
                else:  # Brown
                    r, g, b = 120, 60, 0
                    
                # Add subtle white glow
                w = random.randint(0, 30)
                
                # Apply subtle shimmer effect
                shimmer = 0.8 + (random.random() * 0.4)  # 0.8 to 1.2
                r = min(255, int(r * shimmer))
                g = min(255, int(g * shimmer))
                b = min(255, int(b * shimmer))
                
                led[i] = (r, g, b, w)

    def heartbeatEffect(self):
        """Creates a pulsing heartbeat effect with two quick pulses followed by pause"""
        # Advance counter
        self.counter += 1
        
        # Create heartbeat pattern (two quick pulses followed by pause)
        cycle_position = (self.counter % 100) / 100.0  # 0.0 to 1.0
        
        # First beat at 25%
        if cycle_position < 0.25:
            intensity = math.sin(cycle_position * 4 * math.pi)
        # Second beat at 40% (stronger)
        elif cycle_position < 0.4:
            intensity = 1.2 * math.sin((cycle_position - 0.25) * 8 * math.pi)
        # Rest period
        else:
            intensity = 0
        
        # Keep intensity in valid range and make it positive only
        intensity = max(0, min(1, intensity))
        
        # Use red for heart color
        r = int(255 * intensity)
        g = int(30 * intensity)
        b = int(40 * intensity)
        
        # Apply to all LEDs
        for i in range(7):
            # Center LED is brightest
            if i == 0:
                led[i] = (r, g, b, 0)
            # Outer LEDs at 70% intensity
            else:
                led[i] = (int(r * 0.7), int(g * 0.7), int(b * 0.7), 0)

    def auroraEffect(self):
        """Creates a flowing aurora borealis effect with greens and blues"""
        # Advance counter
        self.counter += 1
        
        # Base wave movement
        time_base = self.counter / 50
        
        # For each LED
        for i in range(7):
            # Create complex wave patterns
            wave1 = math.sin(time_base + i * 0.7)
            wave2 = math.sin(time_base * 1.5 + i * 0.4)
            wave3 = math.sin(time_base * 0.8 - i * 0.3)
            
            # Combine waves and normalize to 0-1
            combined = ((wave1 + wave2 + wave3) / 3 + 1) / 2
            
            # Aurora colors shift between teals, greens, and blues
            # Calculate color balance based on waves
            r = int(20 * combined)  # Minimal red
            g = int(70 + 180 * combined)  # Strong green component
            b = int(100 + 100 * wave2)  # Varying blue
            
            # Add subtle white highlights
            w = int(30 * combined) if random.random() < 0.3 else 0
            
            led[i] = (r, g, b, w)


LED_Controls = LED_Control()
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
                elif text not in ["!B705", "!B507", "!B804", "!B606", "!B10", "!B20", "!B309", "!B408"]:
                    ua.write("Invalid Command!")
                

    LED_Controls.runCurrentMode()
    led.show()
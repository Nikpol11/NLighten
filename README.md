# Nlighten Nightlight

Welcome to Nlighten, a project for a Seeed Studio XIAO NRF52840 powered nightlight. It is a versatile smart lighting device designed to give you a light in the dark and fun in the light. 
It is built around the powerful Seeed Studio XIAO nRF52840 microcontroller and features 
Bluetooth Low Energy (BLE) control for seamless interaction with your smartphone or computer.

Whether placed on your nightstand, desk, or shelf, this nightlight offers convenience through a combination of automatic sensor 
adjustments and remote web/mobile control. It is fully compatible with CircuitPython, allowing you to customize its behavior further 
using the extensive libraries available in the ecosystem.

## Key Features

- **Automatic Brightness:** The device includes an LDR (Light Dependent Resistor) sensor that automatically adjusts LED brightness based 
on ambient lighting conditions.
- **Full RGBW Lighting:** Utilizes a 7-LED RGBW NeoPixel Jewel for vibrant, colorful ambient lighting effects, as well as variable warmth true white
- **Power Flexibility:** Supports USB-C power input and internal battery charging for portability or permanent installation.
- **Web Interface:** Hosted via GitHub Pages to allow easy control from any device on the network, useable on all platforms. 
- **App Support:** Includes a backup control interface accessible through the Adafruit Connect app for mobile users.

## Board Support

This project targets the Seeed XIAO nRF52840. The board support library
(`lib/seeed_xiao_nrf52840.py`) is included directly from:
https://github.com/furbrain/CircuitPython_seeed_xiao_nRF52840

## Dependencies (via circup)

circup install -r requirements.txt

On iOS, a WebBLE capable browser like Bluefy is required to use the web interface. 

## AI Disclosure

Large portions of this project were made using generative AI, including Anthropic Claude, OpenAI ChatGPT, Qwen 3.5 (local), and others. All generated code 
has been reviewed and tested to the best of my ability, and is disclosed where used.

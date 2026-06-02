# Nlighten Nightlight

Welcome to Nlighten, a project for a Seeed Studio XIAO NRF52840 powered nightlight. It is a versatile smart lighting device designed to give you a light in the dark and fun in the light.
It is built around the powerful Seeed Studio XIAO nRF52840 microcontroller and features
Bluetooth Low Energy (BLE) control for seamless interaction with your smartphone or computer.
<img src="https://github.com/Nikpol11/NLighten/blob/main/img/IMG_0503.JPEG"width="300" height="200">
<img src="https://github.com/Nikpol11/NLighten/blob/main/img/IMG_9283.JPEG)"width="300" height="200">
<img src="https://github.com/Nikpol11/NLighten/blob/main/img/IMG_9282.JPEG)"width="300" height="200">
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

## Usage

**1. Web Interface:** <br>
Open the [web interface](https://nikpol11.github.io/NLighten) in a WebBLE compatible browser, hosted at: https://nikpol11.github.io/NLighten
WebBLE capable browsers include:

| OS               | WebBLE-capable browsers                                                                                                  | Notes                                                                                                                                                                                                                       |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Windows**      | **Chrome**, **Microsoft Edge**, likely other Chromium-based browsers with caveats                                        | Chrome supports Web Bluetooth on Windows; WebBluetoothCG notes Windows support requires **Windows 10 version 1703+**. Edge supports it from **Edge 79+**. ([GitHub][1])                                                     |
| **macOS**        | **Chrome**, **Microsoft Edge**, possibly Chromium-based browsers                                                         | Chrome ships the GATT Communication API on Mac without a flag. Safari does **not** support Web Bluetooth. ([GitHub][1])                                                                                                     |
| **Linux**        | **Chrome / Chromium**, but **flag required** and not officially fully supported                                          | WebBluetoothCG says Linux is “partially implemented and not supported” and requires `chrome://flags/#enable-experimental-web-platform-features`; Linux also needs **kernel 3.19+** and **BlueZ 5.41+**. ([GitHub][1])       |
| **Android**      | **Chrome for Android**, **Samsung Internet**, **Opera Mobile**, **UC Browser for Android**, some Chromium-based browsers | Can I Use lists Chrome for Android, Samsung Internet, Opera Mobile, UC Browser for Android, Baidu Browser, and Android Browser as supported; Firefox for Android is not supported. ([Can I Use][2])                         |
| **iOS / iPadOS** | **No mainstream browser support**; use specialty apps like **WebBLE** or **Bluefy**                                      | Safari on iOS is not supported, and Chromium on iOS cannot add its own implementation because it uses Apple’s WKWebView APIs. WebBluetoothCG mentions WebBLE and Bluefy as iOS alternatives. ([Can I Use][2]) ([GitHub][1]) |

[1]: https://github.com/WebBluetoothCG/web-bluetooth/blob/main/implementation-status.md "web-bluetooth/implementation-status.md at main · WebBluetoothCG/web-bluetooth · GitHub"
[2]: https://caniuse.com/web-bluetooth "Web Bluetooth | Can I use... Support tables for HTML5, CSS3, etc"

<br>

**2. Adafruit Connect**<br>
Open the [Adafruit Connect app](https://learn.adafruit.com/bluefruit-le-connect), available on [iOS](https://apps.apple.com/us/app/bluefruit-connect/id830125974) and [Android](https://play.google.com/store/apps/details?id=com.adafruit.bluefruit.le.connect.v4&hl=en-US)
<br>

Text commands generally follow the format "set{option}::{value}". There are exceptions. All current commands are:
| Command format | Value type / options | Effective range / behavior | Example |
| ---------------------------- | ----------------------------------------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------- |
| `ble::disable` | No value | Disables BLE reconnection by setting `bleOff = True` | `ble::disable` |
| `ble::enable` | No value | Enables BLE reconnection by setting `bleOff = False` | `ble::enable` |
| `DC::T` | No value | Disconnects current BLE connection | `DC::T` |
| `setthreshold::<low>,<high>` | Two comma-separated integers | No clamp in parser. Used as `[low, high]`; code expects at least two values LDR Values range from `0-65535`. | `setthreshold::100,10000` |
| `setmode::<mode>` | Integer index or exact mode function name | Valid normal indices: `0–22`. Exact function names also work, case-sensitive. Negative integers `-1` through `-22` also work due to Python's negative indexing. | `setmode::0` or `setmode::rainbowHueFade` |
| `setbright::<value>` | Float | Clamped to `0.0–1.0`; output reports percent. | `setbright::0.75` |
| `sethue::<value>` | Float | Clamped to `0.0–1.0`; output reports degrees as `value * 360`. | `sethue::0.5` |
| `setsaturation::<value>` | Float | Clamped to `0.0–1.0`; output reports percent. | `setsaturation::0.8` |
| `setvalue::<value>` | Float | Expects values `0-1`. Currently has no effect, as value is primarily handled speperately by brightness controls.| `setvalue::1.0` |
| `setwhitebalance::<value>` | Float | Clamped to `0.0–1.0`; `0.0` is RGB-white side, `1.0` is white-channel side. | `setwhitebalance::0.5` |

## Hardware

1x [Seeed Studio XIAO NRF52840](https://wiki.seeedstudio.com/XIAO_BLE/) (sub model does not matter, does not require higher model features)<br>
1x [Adafruit NeoPixel Jewel - 7 x 5050 RGBW](https://www.adafruit.com/product/2859) (White color variety is personal preference, white balance just mixes RGB white and dedicated white, and is uncalibrated)<br>
1x A light dependent resistor capable of operating in the desired range off of 3.3v power, possibly with a voltage divider as in my setup<br>
<br>
Optional: A housing and shade. Can be 3D printed, using vase mode for the shade. A Lithium-Ion battery and the required leads and connectors can also be added as well. 

## Board Support

This project targets the Seeed XIAO nRF52840. The board must be [flashed](https://wiki.seeedstudio.com/XIAO-BLE_CircutPython/) with CircuitPython before use.
The board support library (`lib/seeed_xiao_nrf52840.py`) is included directly from:
https://github.com/furbrain/CircuitPython_seeed_xiao_nRF52840

## Dependencies (via circup)

circup install -r requirements.txt

On iOS, a WebBLE capable browser like [Bluefy](https://bluefy.app) is required to use the web interface.

## AI Disclosure

Large portions of this project were made using generative AI, including Anthropic Claude, OpenAI ChatGPT, Qwen 3.5 (local), and others. All generated code
has been reviewed and tested to the best of my ability, and is disclosed where used.

**Special Thanks to Sean Morris and Jeff Castle of Albany High School and their electronics workshop class for providing the basis and hardware for this project!**
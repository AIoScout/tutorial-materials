# Edge AI Vision Workshop — Pre-lab Manual

> Read this before the workshop. It takes about **15 minutes of reading + 30 minutes of installation**. If you arrive with the software installed and the self-check passed, you will spend the whole session building — not downloading.

---

## 1. What This Workshop Is About

In the lesson (about 45 minutes) we will train a small neural network to **recognize road signs**, live, on a microcontroller — no machine-learning experience needed. Then, in the project session, **you will build your own**: a digit recognizer (0–9) that runs on the same board.

Everything runs on real hardware:

- The **ESP32-P4** development board with a camera module (provided at the workshop)
- The **TFLiteTraining** desktop app, which trains image classifiers without writing code
- **TensorFlow Lite Micro**, Google's runtime that runs the trained model on the chip itself

You do not need to know how to program. Every step is menu-driven; the lab manual tells you exactly what to click.

---

## 2. Background Reading (15 minutes)

You don't need to memorize this — it just makes the lesson much easier to follow.

### 2.1 Why not just write rules?

A normal program follows rules a human wrote: *"if the pixel is dark, do X."* That works for blinking an LED. It does not work for recognizing a road sign in a photo — nobody can write those rules by hand. **Machine learning** flips the approach: instead of writing rules, you show the computer many **labeled examples** (images with the correct answer attached) and let it find the rules by itself. That process is called **training**.

![Classic programming vs. machine learning](img/rules-vs-learning.svg)
*What goes in, and what comes out: classic programming vs. machine learning*

### 2.2 What gets trained? A CNN

A **Convolutional Neural Network (CNN)** is the standard neural network for images. Think of it as a stack of small **feature detectors**: the first layers detect simple patterns (edges, blobs), deeper layers combine them into shapes and objects, and the final layer outputs a **confidence** for each class — for example "left arrow: 91%, right arrow: 7%, wall: 2%". In this workshop the CNN is tiny — small enough to run on a microcontroller in real time.

![How a CNN processes an image](img/cnn.svg)
*A small CNN, end to end: image → feature detectors → one confidence score per class*

### 2.3 The failure mode to know: overfitting

A model can **memorize** your training photos instead of **learning** the concept — like a student who memorizes past papers but can't answer a new question. We detect this by holding part of the data out (**validation split**) and testing with images the model has never seen. You will meet this in the project when you test your digit recognizer on handwriting it wasn't trained on.

![Generalizing vs. overfitting](img/overfitting.svg)
*How to read the training curves: healthy (left) vs. overfit (right)*

### 2.4 Running AI on a chip: edge AI

Sending camera images to a server is slow and needs Wi-Fi. **Edge AI** runs the model directly on the device. To fit, the model is **quantized** to **int8** — every number stored as 1 byte instead of 4 — making it about 4× smaller and faster, at a negligible cost in accuracy. **TensorFlow Lite Micro** (now called LiteRT for Microcontrollers) is the runtime that executes such models on microcontrollers, in as little as 16 KB of memory.

### 2.5 The hardware: ESP32-P4

The **ESP32-P4** is a high-performance microcontroller from Espressif with a dual-core processor, camera support (e.g., the IMX219 module), and enough speed to run image classification in real time. You program it with the familiar **Arduino IDE** over a USB cable.

### 2.6 The tool: TFLiteTraining

**TFLiteTraining** is a desktop app (inspired by Google's Teachable Machine) that gives you the whole pipeline in one window: **collect** images → **preprocess** (crop and clean) → **train** → **preview** live → **export** the model as files ready for the board.

![The six-step pipeline](img/pipeline.svg)
*The six steps you will follow — first on road signs in the lesson, then on digits in the project*

---

## 3. Software Checklist (install before you come)

Install these in order. Versions matter — the workshop steps assume them.

| # | What | Version | Where / Notes |
| - | ---- | ------- | ------------- |
| 1 | **Arduino IDE** | 2.3.10 or higher | https://www.arduino.cc/en/software |
| 2 | **esp32 board package** | **3.3.1 exactly** | In the IDE: Settings → *Additional Boards Manager URLs* → add `https://dl.espressif.com/dl/package_esp32_index.json` → OK. Then *Tools → Board → Board Manager* → search "esp32" → install **esp32 by Espressif Systems, version 3.3.1** |
| 3 | **esp32_mannual core** | as provided | Unzip `esp32_mannual.zip` (we will send it with this manual) into your Arduino hardware folder — see paths below |
| 4 | **TFLiteTraining app** | as provided | Install from the `.dmg` (macOS) or `.exe` (Windows) we send you. Do not launch it yet |
| 5 | **template project** | `template.tmproj` | Download it; you will open it during the workshop |

**Where the esp32_mannual folder goes** — the final path must be:

- **macOS:** `/Users/<you>/Documents/Arduino/hardware/esp32_mannual`
- **Windows:** `C:\Users\<you>\Documents\Arduino\hardware\esp32_mannual`

If the `Arduino/hardware` folder does not exist, create it.

---

## 4. Self-Check (2 minutes, do this the night before)

1. Open the Arduino IDE
2. Open *Tools → Board*
3. You should see an entry called **ESP32_mannual** in the list (with ESP32P4 Dev Module inside it)

If it's there, you're ready. If not, step 3 of the checklist didn't land in the right folder — recheck the path.

---

## 5. What to Bring

- Laptop with the software above installed, **fully charged** (power sockets may be limited)
- A **USB-C data cable** (one that transfers data, not charge-only)
- About **1 GB of free disk space**
- A thick black marker (for writing digits during the project — spares available)

---

## 6. FAQ

**The port doesn't appear in the IDE.** Try another USB port and another cable (charge-only cables are the most common cause). On Windows, the CH34x/CP210x driver may be needed.

**I see "esp32" in Board Manager but version 3.3.1 is not listed.** Make sure you added the Espressif board URL (checklist step 2) *before* opening Board Manager, then refresh.

**macOS says the app "can't be opened because it is from an unidentified developer".** Right-click the app → Open → Open. 

**I already have an older Arduino IDE.** Install 2.3.10+ alongside it and use that one for the workshop.

---

## 7. Where the Materials Live

All workshop materials (lesson slides, project lab manual) are on the workshop page you downloaded this manual from. See you at the session.

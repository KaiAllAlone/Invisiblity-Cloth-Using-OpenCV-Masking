# Invisibility Cloak using OpenCV

This project recreates the **Harry Potter invisibility cloak effect** in real-time using Python and OpenCV.By capturing a static background and replacing regions covered by a specific-colored cloth with that background, the cloth appears invisible.

---

## 📌 Features

* Captures a background image for replacement.
* Allows user to **sample cloth color** from a region of interest (ROI).
* Converts frames to **HSV color space** for robust color detection.
* Builds a **mask** around the cloth color with tolerance ranges.
* Applies **morphological operations** (opening + dilation) to remove noise.
* Replaces detected cloth region with background to create invisibility effect.

---

## 📂 File Structure

* `invisibility_cloak_any.py` → Main script implementing the invisibility cloak.

---

## ⚙️ Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/your-username/invisibility-cloak.git
cd invisibility-cloak
pip install -r requirements.txt
```

### Requirements

```
numpy
opencv-python
```

---

## ▶️ Usage

Run the script directly:

```bash
python invisibility_cloak_any.py
```

### Workflow:

1. **Capture background**: The script captures frames for a few seconds and saves a static background image.
2. **Sample cloth color**: User positions the cloth in the ROI box on screen and presses **`s`** to save HSV values.
3. **Run invisibility**: Once values are saved, the script will:

   * Detect pixels within the HSV tolerance range.
   * Replace them with pixels from the background image.
   * Blend with the live frame for the invisibility effect.
4. Press **`q`** to quit.

---

## 📖 How It Works

1. **Background Capture**
   Saves a static frame of the empty background.

2. **Cloth Color Sampling**

   * The ROI is defined on-screen.
   * HSV mean color of the cloth is sampled when the user presses `s`.

3. **HSV Mask Creation**

   * A lower and upper bound for HSV is computed with tolerances.
   * `cv.inRange()` creates a binary mask isolating cloth pixels.

4. **Mask Refinement**

   * Morphological opening removes small noise.
   * Dilation enlarges mask regions to cover edges.

5. **Compositing**

   * Cloth pixels are replaced with the background.
   * Non-cloth pixels remain from the live video.
   * Final result merges the two, making the cloth invisible.

---

## 🎨 Why HSV Instead of RGB?

The **HSV (Hue, Saturation, Value)** color space is used instead of RGB because:

* **Hue** directly represents the color type (red, green, blue, etc.), making it easier to isolate a specific cloth color.
* **Saturation** measures intensity of the color, and **Value** represents brightness. This separation makes detection less sensitive to lighting changes.
* In **RGB**, colors are defined as mixtures of Red, Green, and Blue intensities. Small lighting or shadow variations can drastically change RGB values, making color detection unstable.
* HSV provides a more **human-like representation of color** and is more robust for real-time color-based segmentation.

---

## 🧩 Example

When you hold the sampled colored cloth in front of you, the region is replaced with the captured background, making it appear as if you’re invisible.

---

## ✅ Future Improvements

* Provide adjustable tolerance sliders (trackbars) for better real-time tuning.
* Improve robustness to varying lighting conditions.
* Allow saving/loading HSV values for reuse.
* Integrate into Web

---

## 📝 License
This project is open-source and available under the **MIT License**.

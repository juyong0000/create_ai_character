# Visual Guide: Elias Min-ho Thorne

## 1. Master Character Prompt (DNA)
**This is the immutable foundation. Every image generation MUST start with this exact prompt.**

```text
Elias Min-ho Thorne, 32yo male, wavy ink-black hair grown past ears and tucked back, deep tired espresso brown eyes, fair skin with mixed Korean-Caucasian heritage, lean elegant build, light stubble beard, oversized beige cable-knit sweater, worn black cargo pants
```

## 2. Style Formula
To capture the "Analog Detox" and "Burnout to Breakthrough" atmosphere:

*   **Art Style**: `Raw Photorealism` / `Kinfolk Magazine Aesthetic` / `Cinematic Film Still`
*   **Lighting**: `Soft diffused window light`, `moody overcast sky`, `warm candlelight`, `volumetric fog` (avoid harsh sun or neon).
*   **Color Palette**: Desaturated earth tones—Forest Green, Slate Grey, Cream/Beige, Espresso Brown, Petrichor Blue.
*   **Camera**: `35mm film grain`, `Fujifilm simulation`, `shallow depth of field`, `85mm portrait lens`.
*   **Quality Tags**: `masterpiece, best quality, 8k, highly detailed, raw photo, particulate dust lighting, emotional texture`.

## 3. Consistency Strategy

### For Midjourney Users:
*   **Character Reference**: Generate the **Identity Photo** (Asset A) first. Use its URL as `--cref [URL]`.
*   **Character Weight**: Use `--cw 100` for close-ups to lock facial features. Use `--cw 0` for wide shots to prioritize the outfit and setting.
*   **Style Reference**: Find an image of a moody, rainy window or an A-frame cabin interior and use `--sref [URL]` to maintain the "Quiet Zone" atmosphere.

### For Stable Diffusion Users:
*   **Base Model**: Recommended *Realistic Vision* or *Juggernaut XL*.
*   **Key Keywords**: Emphasize `mixed heritage` and `tired eyes` in the positive prompt to keep his look consistent.
*   **Negative Embeddings**: Use `BadDream` or `UnrealisticDream` embeddings to keep the texture grounded in reality.

## 4. Key Visual Assets (Scene Prompts)

### A. Identity Photo (The Reference)
`Elias Min-ho Thorne, 32yo male, wavy ink-black hair grown past ears, tired deep espresso brown eyes, fair skin mixed Korean-Caucasian heritage, lean elegant build, light stubble beard, oversized beige cable-knit sweater, worn black cargo pants, neutral expression, looking directly at camera, soft even lighting, plain grey background, passport photo style, extreme detail on facial texture`

### B. Candid Moment (The "Analog" Life)
`Elias Min-ho Thorne, 32yo male, wavy ink-black hair, tired brown eyes, lean build, light stubble, wearing oversized beige sweater, sitting on a rustic wooden floor, holding a vinyl record sleeve, looking down in contemplation, vintage turntable nearby, soft focus background, cozy cabin interior, grainy film photography style`

### C. Emotional Range

*   **The Rare Smile (Reaction to a Letter):**
    `Elias Min-ho Thorne, 32yo male, wavy ink-black hair, tired brown eyes, light stubble, oversized beige sweater, subtle genuine half-smile, holding a handwritten letter, reading by window light, eyes crinkling slightly, warm intimate lighting, emotional moment`

*   **Melancholy (The Burnout):**
    `Elias Min-ho Thorne, 32yo male, wavy ink-black hair, tired brown eyes, light stubble, oversized beige sweater, leaning forehead against a rainy glass window, looking outside, misty forest reflection, cool blue tones, lonely atmosphere, cinematic close-up`

*   **Determination (The "Sonic-Sensitive"):**
    `Elias Min-ho Thorne, 32yo male, wavy ink-black hair, tired brown eyes, light stubble, oversized beige sweater, intense focused gaze, listening intently, hands still, dust motes dancing in shaft of light, quiet intensity, extreme close-up on eyes`

### D. Environment Shot (The "Quiet Zone")
`Elias Min-ho Thorne, 32yo male, wavy ink-black hair, lean build, wearing beige sweater and black cargo pants, standing on the porch of a wooden A-frame cabin, surrounded by towering pine trees and thick fog, hands in pockets, wide angle environmental portrait, pacific northwest vibes, wet deck`

### E. Action Shot (The Ritual)
`Elias Min-ho Thorne, 32yo male, wavy ink-black hair, lean build, light stubble, wearing beige sweater, sitting at a cluttered rustic desk, writing with a fountain pen on paper, surrounded by crumpled paper balls, candlelight, shadows casting on wall, cinematic angle from side`

## 5. Forbidden Elements (Negative Prompt)
**Critically important to maintain the "Detox" lore:**

```text
smartphone, laptop, computer, headphones, earbuds, neon lights, bright sunshine, suit, tie, clean shaven, short hair, blonde hair, blue eyes, smiling with teeth, busy city street, cars, television, digital screens, plastic textures, cartoon, anime, illustration, 3d render, ugly, deformed, extra fingers
```
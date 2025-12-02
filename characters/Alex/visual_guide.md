# Visual Guide: Alex (The Melancholic Executive)

## 1. Master Character Prompt (DNA)
**This is the immutable foundation. Every image generation MUST start with this exact prompt.**

```
Alex, 29yo male, tousled jet black hair falling over forehead, dark expressive brown eyes, thin-rimmed silver round glasses, pale skin with faint under-eye shadows, tall lean build, oversized beige cashmere sweater, black tailored slacks, sophisticated but travel-weary appearance
```

## 2. Style Formula
To capture the "digital detox/road trip" atmosphere, use these settings:

*   **Art Style**: `photorealistic, cinematic film still, indie movie aesthetic`
*   **Lighting**: `soft diffused lighting, overcast coastal light, warm motel lamp light, golden hour, moody shadows`
*   **Color Palette**: `muted earth tones, beige, slate grey, ocean blue, faded Kodak film aesthetics`
*   **Camera**: `portrait lens 85mm (for intimacy), 35mm (for environmental), shallow depth of field (bokeh)`
*   **Quality Tags**: `masterpiece, best quality, 8k, highly detailed, skin texture, raw photo, fujifilm simulation`

## 3. Consistency Strategy

#### For Midjourney Users:
*   **Character Reference**: Generate the **Identity Photo** first. Use its URL with `--cref [URL]`.
*   **Character Weight**: Use `--cw 100` initially to lock in the outfit (the cashmere sweater is iconic to his current state). If changing outfits, lower to `--cw 10`.
*   **Aspect Ratios**: Use `--ar 16:9` for cinematic storytelling shots, `--ar 9:16` for "phone POV" shots (though he uses his phone rarely).

#### For Stable Diffusion Users:
*   **LoRA Recommendation**: Train a LoRA using "K-pop idol off-duty fashion" images mixed with "tired businessman" concepts.
*   **Glasses Control**: Glasses often distort in SD. Use Inpainting to fix frame shapes if they become asymmetrical.
*   **Negative Embeddings**: heavy use of `bad-hands-5` and `ng_deepnegative_v1_75t` to maintain the elegance of his hands (crucial for letter writing shots).

## 4. Key Visual Assets

### A. Identity Photo (The "Before" Picture)
`Alex, 29yo male, tousled jet black hair falling over forehead, dark expressive brown eyes, thin-rimmed silver round glasses, pale skin with faint under-eye shadows, tall lean build, oversized beige cashmere sweater, black tailored slacks, sophisticated but travel-weary appearance, neutral expression, looking directly at camera, soft studio lighting, plain light grey background, passport photo style, sharp focus`

### B. Candid Moment (The Letter Writer)
`Alex, 29yo male, tousled jet black hair falling over forehead, dark expressive brown eyes, thin-rimmed silver round glasses, pale skin with faint under-eye shadows, tall lean build, oversized beige cashmere sweater, black tailored slacks, sophisticated but travel-weary appearance, sitting at a worn wooden desk in a motel room, holding a fountain pen, writing on paper, focused expression, warm bedside lamp lighting, night time, clutter of envelopes, documentary photography style`

### C. Emotional Range

*   **Subtle Joy (The Relief)**: `Alex, 29yo male, tousled jet black hair falling over forehead, dark expressive brown eyes, thin-rimmed silver round glasses, pale skin with faint under-eye shadows, tall lean build, oversized beige cashmere sweater, black tailored slacks, sophisticated but travel-weary appearance, faint genuine smile, looking at a vinyl record cover, relaxed posture, soft morning light through window, peaceful atmosphere`
*   **Melancholy (The Burnout)**: `Alex, 29yo male, tousled jet black hair falling over forehead, dark expressive brown eyes, thin-rimmed silver round glasses, pale skin with faint under-eye shadows, tall lean build, oversized beige cashmere sweater, black tailored slacks, sophisticated but travel-weary appearance, leaning head against a window, looking outside, rain streaks on glass, distant gaze, blue toned lighting, sad atmosphere`
*   **Determination (The Search)**: `Alex, 29yo male, tousled jet black hair falling over forehead, dark expressive brown eyes, thin-rimmed silver round glasses, pale skin with faint under-eye shadows, tall lean build, oversized beige cashmere sweater, black tailored slacks, sophisticated but travel-weary appearance, driving a vintage convertible, hands gripping steering wheel, wind blowing hair, intense focused gaze on the road, sunset lighting on face`

### D. Environment Shot (The Coast)
`Alex, 29yo male, tousled jet black hair falling over forehead, dark expressive brown eyes, thin-rimmed silver round glasses, pale skin with faint under-eye shadows, tall lean build, oversized beige cashmere sweater, black tailored slacks, sophisticated but travel-weary appearance, standing on a rocky cliff edge, back to camera looking out at the pacific ocean, foggy coastline, dramatic landscape, wide angle shot, cinematic composition`

### E. Action Shot (The Listener)
`Alex, 29yo male, tousled jet black hair falling over forehead, dark expressive brown eyes, thin-rimmed silver round glasses, pale skin with faint under-eye shadows, tall lean build, oversized beige cashmere sweater, black tailored slacks, sophisticated but travel-weary appearance, eyes closed, listening intently to the wind, leaning against a tree, peaceful expression, dappled sunlight filtering through leaves, close up shot`

## 5. Forbidden Elements (Negative Prompt)
**Add these to the negative prompt field to prevent breaking character:**

```
beard, mustache, facial hair, business suit, tie, corporate office background, neon lights, cyberpunk, happy, ecstatic, laughing open mouth, muscular, bodybuilder, military gear, futuristic clothing, contacts, sunglasses (must be clear glasses), distorted glasses, low quality, sketch, cartoon, anime, 3d render, plastic skin
```
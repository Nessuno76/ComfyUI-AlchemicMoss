# ⚗ Changelog

## 1.0.0 — 2026-11-17 · first release

The MOSS-Image branch of ComfyUI-AlchemicaSampler (from its 1.1.1), with its own node names, routes and web
extensions, so the two packs install side by side.

### Nodes
- **⚗ AlchemicMoss Load**: MOSS-Image model + Qwen3.5 text encoder (always the `moss_image` type) + flux2 VAE. A Krea 2 model or a wrong encoder stops with a clear message.
- **⚗ AlchemicMoss Prompt**: the ⚗ Prompt of AlchemicaSampler for MOSS-Image.
  - **Who writes the prompt:** MOSS-Image's own Qwen3.5-9B encoder, told that written text goes in "double quotes". Defaults: 150 words, 600 tokens.
  - **Start latent** in MOSS-Image's format: 128 channels at 1/16, sides multiples of 16. Default 1.5 MP.
  - **Negative:** a short default negative when the field is empty. When the prompt asks for a text in quotes, `text`, `letters`, `signature`… leave the negative. The LLM negative stops where it starts looping and keeps at most 24 items.
  - **Framing and look presets** go at the head of the prompt, without the composition phase: on MOSS-Image the framing text alone decided clothes and colours (a red leather jacket and neon signs came out as a black jacket in a grey alley).
  - A Krea 2 encoder on a MOSS-Image model stops the run with a clear message.
- **⚗ AlchemicMoss KSampler**: KSampler Flex with MOSS-Image defaults (`er_sde` + `simple`, 25 steps, cfg 2.5, one stage, contraction 1, DeGrid 0). It warns when cfg is 1, when no negative is connected, or when a stage has too few steps.
- **⚗ AlchemicMoss Calibration**: the Calibration with a `negative` input and cfg 2.5.

### Fixes for MOSS-Image, compared with AlchemicaSampler 1.1.1
- **Shift of the Alchemica schedulers:** `flux_shift`, `alchemica_dual` and the calibrated base read the model's shift as an exponent (right for Krea 2 / Flux). MOSS-Image stores the factor itself (5): read as an exponent it made 148, and the sigmas stayed at 1.0 for 24 steps of 25. The shift is now read in the model's own units.
- **Calibration at MOSS-Image's latent scale:** the composition measure uses blocks of 64 image pixels (4 latent pixels at 1/16), and the report gives the right resolutions.
- **DeGrid** is skipped: the 2-pixel grid belongs to Krea 2's 3D VAE, not to the 2D FLUX.2 VAE.

### Profile and workflows
- `profili/moss_image_sft_int8_convrot.json`: 12 prompts, cfg 2.5, 1024×1536. `profile (auto)` picks it for that file.
- **`AlchemicMoss_T2I`** and **`AlchemicMoss_CALIBRATION`**.

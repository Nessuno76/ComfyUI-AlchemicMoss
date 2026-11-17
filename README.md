# ⚗ AlchemicMoss

**The AlchemicaMente line for [MOSS-Image](https://github.com/OpenMOSS/MOSS-Image)** (OpenMOSS, Apache-2.0), natively
supported by ComfyUI. Four nodes: **Load → Prompt → KSampler → Save**, plus the **Calibration** that measures your
checkpoint.

It is the MOSS-Image branch of [ComfyUI-AlchemicaSampler](https://github.com/Nessuno76/ComfyUI-AlchemicaSampler)
(Krea 2), with its own node names: the two packs install side by side.

Idea & direction: **AlchemicaMente** · code: **Claude (Anthropic)** · GPL-3.0

## Install

ComfyUI Manager → search **AlchemicMoss**, or:

```
cd ComfyUI/custom_nodes
git clone https://github.com/Nessuno76/ComfyUI-AlchemicMoss
```

No extra Python packages. ComfyUI **0.42 or newer** (native MOSS-Image support).

| File (from [Comfy-Org/MOSS-Image](https://huggingface.co/Comfy-Org/MOSS-Image)) | Folder |
|---|---|
| `moss_image_sft_int8_convrot.safetensors` (or `_bf16`) | `models/diffusion_models` |
| `qwen3.5_9b_int8_convrot.safetensors` or `qwen3.5_9b_w4a8_gptq.safetensors` | `models/text_encoders` |
| `flux2-vae.safetensors` | `models/vae` |

Then open the workflow **`AlchemicMoss_T2I`** (Workflow → Browse templates → AlchemicMoss), write an idea, press *Queue*.

## The nodes

| Node | What it does |
|---|---|
| **⚗ AlchemicMoss Load** | model + Qwen3.5 text encoder + flux2 VAE. The encoder is always loaded with the `moss_image` type, the most common setup error. A Krea 2 model stops with a clear message. |
| **⚗ AlchemicMoss Prompt** | an idea in any language → MOSS-Image's own Qwen3.5 encoder writes the prompt (or `as written` keeps your text). Lists, wildcards, examples. At the bottom: **shot / camera angle / view / light / atmosphere / background** presets with thumbnails (📷). It makes the start latent in MOSS-Image's format (128 channels, 1/16) and a negative. |
| **⚗ AlchemicMoss KSampler** | any ComfyUI sampler and scheduler, plus the Alchemica ones (`alchemica_euler_2m`, `alchemica_calibrated`, `alchemica_dual`, `flux_shift`). A report says what it did. |
| **⚗ AlchemicMoss Calibration** | measures how your checkpoint builds the image and saves a profile. The KSampler's `profile (auto)` finds it by itself. |

## What to know about MOSS-Image

- **Not distilled:** it needs a real **cfg (2.5-3)** with the Prompt's negative connected, and **25-50 steps**. The defaults: `er_sde` + `simple`, 25 steps, cfg 2.5, one stage, 1.5 MP.
- **Prompts:** longer prompts suit it (`words` 150). Text to render goes in "double quotes": the Prompt tells the encoder so, and drops `text`, `letters`, `signature` from the negative when the prompt asks for a written text.
- **Framing presets** go at the head of the prompt. The composition phase of AlchemicaSampler (framing text first, full text later) stays off: on MOSS-Image the framing text alone would decide clothes and colours.
- **NAG / SEG / PAG** are Krea 2 tools: here the negative works through the cfg.
- **Vertical stripes** on skies and walls are a trait of the SFT checkpoint. A DeBand LoRA helps.
- **`--use-sage-attention`** washes MOSS-Image out. Launch ComfyUI without it.
- Speed on an RTX 5070 Ti 16 GB, int8 model + w4a8 encoder, 1.5 MP: about 21 s of sampling for 25 steps.

## Calibration

A profile of `moss_image_sft_int8_convrot` (12 prompts, cfg 2.5) ships in `profili/`. For another file (bf16, a
fine-tune, a LoRA stack) open **`AlchemicMoss_CALIBRATION`**: it measures one prompt of a list per run, with the
Prompt's negative and cfg 2.5. Queue it 8 or more times (*Queue* with a batch count of 12): from 8 samples the
profile is reliable and `alchemica_calibrated` and every `-1` value of the KSampler come from it.

Measured on `moss_image_sft_int8_convrot`: composition settled at sigma 0.93 → 0.80, detail window 0.71 → 0.25.

## Workflows

| Workflow | |
|---|---|
| **AlchemicMoss_T2I** | Load → Prompt → KSampler → Save: write an idea, *Queue* |
| **AlchemicMoss_CALIBRATION** | measures your checkpoint, one prompt per run |

## License

GPL-3.0, the same license as ComfyUI. See `LICENSE`, `CREDITS.md` and `THIRD_PARTY_NOTICES.md`.

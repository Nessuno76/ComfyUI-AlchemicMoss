# ⚗ ComfyUI-AlchemicMoss — the AlchemicaMente line for MOSS-Image
# Copyright (C) 2026 AlchemicaMente — idea, direction and testing
# Code written by Claude (Anthropic) on AlchemicaMente's design. Thanks to all: see CREDITS.md
# SPDX-License-Identifier: GPL-3.0-only
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, version 3 (the same
# license as ComfyUI). It is distributed WITHOUT ANY WARRANTY; see the file LICENSE for details.

"""Four nodes for MOSS-Image: Load, Prompt, KSampler, Calibration. They are the AlchemicaSampler nodes with their own
names, routes and defaults, so this pack installs next to ComfyUI-AlchemicaSampler (Krea 2) without clashing."""
import copy

from .alchemica import famiglia
from .nodes import AlchemicaTaratura
from .nodes_completo import _lista, _scegli, comfy_nodes
from .nodes_flex import AlchemicaKSamplerFlex
from .nodes_prompt_studio import AlchemicaPromptStudio
from .nodes_v2 import SPECS, crea_gemello

CAT = "⚗ AlchemicMoss"


def _con_default(tipi, nuovi):
    """INPUT_TYPES with other default values (MOSS-Image is not distilled: real cfg, more steps, one stage)."""
    tipi = copy.deepcopy(tipi)
    for sezione in ("required", "optional"):
        for k, v in nuovi.items():
            spec = tipi.get(sezione, {}).get(k)
            if spec is not None and len(spec) > 1 and isinstance(spec[1], dict):
                spec[1]["default"] = v
    return tipi


class AlchemicMossLoad:
    @classmethod
    def INPUT_TYPES(cls):
        u, c, v = _lista("diffusion_models"), _lista("text_encoders"), comfy_nodes.VAELoader.vae_list(comfy_nodes.VAELoader)
        dt = comfy_nodes.UNETLoader.INPUT_TYPES()["required"]["weight_dtype"][0]
        return {"required": {
            "unet_name": (u, {"default": _scegli(u, "moss_image_sft_int8_convrot.safetensors"),
                              "tooltip": "MOSS-Image diffusion model (models/diffusion_models)"}),
            "weight_dtype": (dt, {"default": "default"}),
            "clip_name": (c, {"default": _scegli(c, "qwen3.5_9b_w4a8_gptq.safetensors"),
                              "tooltip": "Qwen3.5-9B text encoder. Loaded with the moss_image type"}),
            "vae_name": (v, {"default": _scegli(v, "flux2-vae.safetensors"), "tooltip": "flux2-vae"}),
        }}

    RETURN_TYPES = ("MODEL", "CLIP", "VAE")
    RETURN_NAMES = ("model", "clip", "vae")
    FUNCTION = "carica"
    CATEGORY = CAT
    DESCRIPTION = "MOSS-Image in one node: model + Qwen3.5 text encoder (always the moss_image type) + flux2 VAE."

    def carica(self, unet_name, weight_dtype, clip_name, vae_name):
        m = comfy_nodes.UNETLoader().load_unet(unet_name, weight_dtype)[0]
        if famiglia.di(m) != famiglia.MOSS:
            raise ValueError(f"⚗ AlchemicMoss Load: '{unet_name}' is not MOSS-Image ({type(m.model).__name__}). "
                             f"For Krea 2 use ComfyUI-AlchemicaSampler.")
        try:
            c = comfy_nodes.CLIPLoader().load_clip(clip_name, type=famiglia.TIPO_CLIP[famiglia.MOSS])[0]
        except Exception as ex:
            raise ValueError(f"⚗ AlchemicMoss Load: the text encoder '{clip_name}' did not load as MOSS-Image ({ex}). "
                             f"MOSS-Image needs a qwen3.5_9b text encoder.") from ex
        va = comfy_nodes.VAELoader().load_vae(vae_name)[0]
        print(f"[AlchemicMoss Load] {unet_name} + {clip_name} + {vae_name}")
        return (m, c, va)


class AlchemicMossPrompt(AlchemicaPromptStudio):
    @classmethod
    def INPUT_TYPES(cls):
        return _con_default(super().INPUT_TYPES(), {"words": 150, "max_tokens": 600, "attention_guidance": False,
                                                    "megapixels": 1.5})

    CATEGORY = CAT


class AlchemicMossKSampler(AlchemicaKSamplerFlex):
    @classmethod
    def INPUT_TYPES(cls):
        return _con_default(super().INPUT_TYPES(), {
            "sampler_name": "er_sde", "scheduler": "simple", "steps": 25, "cfg": 2.5, "two_stage": False,
            "detail": 0.0, "variety": 0.0, "restart_steps": 0, "contraction": 1.0, "degrid": 0.0})

    CATEGORY = CAT


_, _, _, _ren, _val, _outs = SPECS["AlchemicaTaratura"]
_Calib = crea_gemello(AlchemicaTaratura, "AlchemicMossCalibration", "", CAT, _ren, _val, _outs)


class AlchemicMossCalibration(_Calib):
    @classmethod
    def INPUT_TYPES(cls):
        return _con_default(super().INPUT_TYPES(), {"cfg": 2.5})


AlchemicMossCalibration.__name__ = AlchemicMossCalibration.__qualname__ = "AlchemicMossCalibration"

NODE_CLASS_MAPPINGS = {
    "AlchemicMossLoad": AlchemicMossLoad,
    "AlchemicMossPrompt": AlchemicMossPrompt,
    "AlchemicMossKSampler": AlchemicMossKSampler,
    "AlchemicMossCalibration": AlchemicMossCalibration,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "AlchemicMossLoad": "⚗ AlchemicMoss Load (MOSS-Image)",
    "AlchemicMossPrompt": "⚗ AlchemicMoss Prompt (idea / list + latent)",
    "AlchemicMossKSampler": "⚗ AlchemicMoss KSampler",
    "AlchemicMossCalibration": "⚗ AlchemicMoss Calibration (measure your checkpoint)",
}
WEB_DIRECTORY = "./web"

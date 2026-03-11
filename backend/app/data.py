APP_CONFIG = {
    "brandName": "LUX",
    "eventLabel": "March 2026",
    "watermarkText": "LUX | March 2026",
}


FILTER_PRESETS = [
    {
        "id": "bw",
        "label": "B&W",
        "filter": "grayscale(100%) contrast(1.18) brightness(0.96)",
        "description": "Classic monochrome strip with crisp contrast.",
        "thumbnailGradient": "from-stone-200 via-stone-500 to-stone-900",
    },
    {
        "id": "film",
        "label": "Film",
        "filter": "sepia(18%) contrast(1.08) saturate(0.94) brightness(0.99)",
        "description": "Muted cinematic tone for a soft analog finish.",
        "thumbnailGradient": "from-zinc-200 via-neutral-500 to-zinc-900",
    },
    {
        "id": "warm",
        "label": "Warm",
        "filter": "sepia(28%) saturate(1.18) brightness(1.03) hue-rotate(-8deg)",
        "description": "Golden booth tones with a gentle skin-friendly lift.",
        "thumbnailGradient": "from-amber-200 via-orange-400 to-rose-700",
    },
    {
        "id": "grain",
        "label": "Grain",
        "filter": "contrast(1.08) saturate(0.92) brightness(0.98)",
        "description": "Subtle texture and contrast for a Snappy-style finish.",
        "thumbnailGradient": "from-zinc-100 via-zinc-400 to-zinc-800",
    },
    {
        "id": "clean",
        "label": "Clean",
        "filter": "none",
        "description": "Balanced tones for a neutral booth strip.",
        "thumbnailGradient": "from-zinc-300 via-zinc-500 to-zinc-800",
    },
]
<script setup>
import { nextTick, ref, watch } from 'vue'

const props = defineProps({
  frames: {
    type: Array,
    required: true,
  },
  activeFilterLabel: {
    type: String,
    required: true,
  },
  watermarkText: {
    type: String,
    required: true,
  },
})

const emit = defineEmits(['retake'])

const templates = [
  { id: 'classic',  label: 'Classic',   description: 'White-bordered vertical strip' },
  { id: 'dark',     label: 'Dark',      description: 'Midnight dark variant' },
  { id: 'film',     label: 'Film Roll', description: 'Film reel with sprocket holes' },
  { id: 'polaroid', label: 'Polaroid',  description: 'Triple polaroid frames' },
  { id: 'minimal',  label: 'Minimal',   description: 'Edge-to-edge borderless stack' },
]

const activeTemplateId = ref('classic')
const canvasRef = ref(null)

async function loadImage(source) {
  return new Promise((resolve, reject) => {
    const image = new Image()
    image.onload = () => resolve(image)
    image.onerror = reject
    image.src = source
  })
}

function drawCover(ctx, image, frameX, frameY, frameWidth, frameHeight) {
  const imageRatio = image.width / image.height
  const frameRatio = frameWidth / frameHeight

  let drawWidth = frameWidth
  let drawHeight = frameHeight
  let offsetX = frameX
  let offsetY = frameY

  if (imageRatio > frameRatio) {
    drawWidth = frameHeight * imageRatio
    offsetX = frameX - (drawWidth - frameWidth) / 2
  } else {
    drawHeight = frameWidth / imageRatio
    offsetY = frameY - (drawHeight - frameHeight) / 2
  }

  ctx.drawImage(image, offsetX, offsetY, drawWidth, drawHeight)
}

function tracedRoundRect(ctx, x, y, w, h, r) {
  ctx.beginPath()
  ctx.moveTo(x + r, y)
  ctx.lineTo(x + w - r, y)
  ctx.quadraticCurveTo(x + w, y, x + w, y + r)
  ctx.lineTo(x + w, y + h - r)
  ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h)
  ctx.lineTo(x + r, y + h)
  ctx.quadraticCurveTo(x, y + h, x, y + h - r)
  ctx.lineTo(x, y + r)
  ctx.quadraticCurveTo(x, y, x + r, y)
  ctx.closePath()
}

// ── Template: Classic ────────────────────────────────────────────────────────
function renderClassic(canvas, images) {
  const W = 400, PAD = 20, FOOTER = 112
  const slotW = W - PAD * 2, slotH = W
  canvas.width = W
  canvas.height = W * 3 + PAD * 4 + FOOTER

  const ctx = canvas.getContext('2d')
  ctx.fillStyle = '#ffffff'
  ctx.fillRect(0, 0, canvas.width, canvas.height)

  for (const [i, img] of images.entries()) {
    const y = PAD + i * (slotH + PAD)
    ctx.save()
    ctx.beginPath()
    ctx.rect(PAD, y, slotW, slotH)
    ctx.clip()
    drawCover(ctx, img, PAD, y, slotW, slotH)
    ctx.restore()
    ctx.strokeStyle = 'rgba(229,231,235,0.9)'
    ctx.lineWidth = 2
    ctx.strokeRect(PAD, y, slotW, slotH)
  }

  ctx.fillStyle = '#0f172a'
  ctx.font = '600 28px Geist Variable, sans-serif'
  ctx.textAlign = 'center'
  ctx.fillText(props.watermarkText, W / 2, canvas.height - 44)
  ctx.fillStyle = '#64748b'
  ctx.font = '500 14px Geist Variable, sans-serif'
  ctx.fillText(`${props.activeFilterLabel} preset`, W / 2, canvas.height - 18)
}

// ── Template: Dark ───────────────────────────────────────────────────────────
function renderDark(canvas, images) {
  const W = 400, PAD = 20, FOOTER = 112
  const slotW = W - PAD * 2, slotH = W
  canvas.width = W
  canvas.height = W * 3 + PAD * 4 + FOOTER

  const ctx = canvas.getContext('2d')
  ctx.fillStyle = '#0a0a0f'
  ctx.fillRect(0, 0, canvas.width, canvas.height)

  for (const [i, img] of images.entries()) {
    const y = PAD + i * (slotH + PAD)
    ctx.save()
    ctx.beginPath()
    ctx.rect(PAD, y, slotW, slotH)
    ctx.clip()
    drawCover(ctx, img, PAD, y, slotW, slotH)
    ctx.restore()
    ctx.strokeStyle = 'rgba(255,255,255,0.12)'
    ctx.lineWidth = 1.5
    ctx.strokeRect(PAD, y, slotW, slotH)
  }

  ctx.fillStyle = '#f8fafc'
  ctx.font = '600 28px Geist Variable, sans-serif'
  ctx.textAlign = 'center'
  ctx.fillText(props.watermarkText, W / 2, canvas.height - 44)
  ctx.fillStyle = '#94a3b8'
  ctx.font = '500 14px Geist Variable, sans-serif'
  ctx.fillText(`${props.activeFilterLabel} preset`, W / 2, canvas.height - 18)
}

// ── Template: Film Roll ──────────────────────────────────────────────────────
function renderFilm(canvas, images) {
  const W = 400
  const SPROCKET_W = 28
  const PHOTO_W = W - SPROCKET_W * 2
  const PHOTO_H = PHOTO_W
  const GAP = 10
  const V_PAD = 24
  const FOOTER = 72
  const H = V_PAD + images.length * PHOTO_H + (images.length - 1) * GAP + V_PAD + FOOTER

  canvas.width = W
  canvas.height = H

  const ctx = canvas.getContext('2d')
  ctx.fillStyle = '#111111'
  ctx.fillRect(0, 0, W, H)

  // Sprocket-area separators
  ctx.strokeStyle = '#2a2a2a'
  ctx.lineWidth = 1
  ctx.beginPath(); ctx.moveTo(SPROCKET_W, 0); ctx.lineTo(SPROCKET_W, H); ctx.stroke()
  ctx.beginPath(); ctx.moveTo(W - SPROCKET_W, 0); ctx.lineTo(W - SPROCKET_W, H); ctx.stroke()

  // Sprocket holes
  const holeW = 10, holeH = 7, holeSpacing = 20
  const holeXL = Math.round(SPROCKET_W / 2 - holeW / 2)
  const holeXR = W - SPROCKET_W + Math.round(SPROCKET_W / 2 - holeW / 2)

  for (let hy = 10; hy < H - 10; hy += holeSpacing) {
    for (const hx of [holeXL, holeXR]) {
      ctx.fillStyle = '#2a2a2a'
      tracedRoundRect(ctx, hx - 1, hy - 1, holeW + 2, holeH + 2, 2)
      ctx.fill()
      ctx.fillStyle = '#000000'
      tracedRoundRect(ctx, hx, hy, holeW, holeH, 2)
      ctx.fill()
    }
  }

  // Photos
  for (const [i, img] of images.entries()) {
    const y = V_PAD + i * (PHOTO_H + GAP)
    ctx.save()
    ctx.beginPath()
    ctx.rect(SPROCKET_W, y, PHOTO_W, PHOTO_H)
    ctx.clip()
    drawCover(ctx, img, SPROCKET_W, y, PHOTO_W, PHOTO_H)
    ctx.restore()

    // Frame number
    ctx.fillStyle = 'rgba(255,255,255,0.30)'
    ctx.font = '400 9px monospace'
    ctx.textAlign = 'left'
    ctx.fillText(String(i + 1).padStart(2, '0'), SPROCKET_W + 5, y + PHOTO_H - 6)
  }

  // Footer
  const footerY = H - FOOTER
  ctx.fillStyle = '#d4d4d4'
  ctx.font = '600 22px Geist Variable, monospace'
  ctx.textAlign = 'center'
  ctx.fillText(props.watermarkText, W / 2, footerY + 30)
  ctx.fillStyle = '#666666'
  ctx.font = '400 11px monospace'
  ctx.fillText(`${props.activeFilterLabel} preset`, W / 2, footerY + 52)
}

// ── Template: Polaroid ───────────────────────────────────────────────────────
function renderPolaroid(canvas, images) {
  const W = 400
  const POL_W = 340
  const PAD_SIDE = 18, PAD_TOP = 16, PAD_BOT = 56
  const PHOTO_W = POL_W - PAD_SIDE * 2
  const PHOTO_H = PHOTO_W
  const POL_H = PHOTO_H + PAD_TOP + PAD_BOT
  const GAP = 18
  const OUTER_X = (W - POL_W) / 2
  const TOP_PAD = 28
  const FOOTER = 56
  const H = TOP_PAD + images.length * POL_H + (images.length - 1) * GAP + FOOTER

  canvas.width = W
  canvas.height = H

  const ctx = canvas.getContext('2d')
  ctx.fillStyle = '#ede8df'
  ctx.fillRect(0, 0, W, H)

  for (const [i, img] of images.entries()) {
    const polY = TOP_PAD + i * (POL_H + GAP)

    // Drop shadow
    ctx.save()
    ctx.shadowColor = 'rgba(0,0,0,0.22)'
    ctx.shadowBlur = 16
    ctx.shadowOffsetX = 2
    ctx.shadowOffsetY = 5
    ctx.fillStyle = '#ffffff'
    ctx.fillRect(OUTER_X, polY, POL_W, POL_H)
    ctx.restore()

    // White frame
    ctx.fillStyle = '#ffffff'
    ctx.fillRect(OUTER_X, polY, POL_W, POL_H)

    // Photo
    const photoX = OUTER_X + PAD_SIDE
    const photoY = polY + PAD_TOP
    ctx.save()
    ctx.beginPath()
    ctx.rect(photoX, photoY, PHOTO_W, PHOTO_H)
    ctx.clip()
    drawCover(ctx, img, photoX, photoY, PHOTO_W, PHOTO_H)
    ctx.restore()

    ctx.strokeStyle = 'rgba(0,0,0,0.07)'
    ctx.lineWidth = 1
    ctx.strokeRect(photoX, photoY, PHOTO_W, PHOTO_H)
  }

  // Footer watermark
  ctx.fillStyle = '#2d2d2d'
  ctx.font = '600 20px Geist Variable, sans-serif'
  ctx.textAlign = 'center'
  ctx.fillText(props.watermarkText, W / 2, H - 22)
}

// ── Template: Minimal ────────────────────────────────────────────────────────
function renderMinimal(canvas, images) {
  const W = 400
  const H = W * images.length

  canvas.width = W
  canvas.height = H

  const ctx = canvas.getContext('2d')
  ctx.fillStyle = '#000000'
  ctx.fillRect(0, 0, W, H)

  for (const [i, img] of images.entries()) {
    const y = i * W
    ctx.save()
    ctx.beginPath()
    ctx.rect(0, y, W, W)
    ctx.clip()
    drawCover(ctx, img, 0, y, W, W)
    ctx.restore()
  }

  // Subtle overlay watermark on the bottom strip
  const overlayH = 40
  ctx.fillStyle = 'rgba(0,0,0,0.50)'
  ctx.fillRect(0, H - overlayH, W, overlayH)
  ctx.fillStyle = 'rgba(255,255,255,0.65)'
  ctx.font = '500 12px Geist Variable, sans-serif'
  ctx.textAlign = 'center'
  ctx.fillText(`${props.watermarkText}  ·  ${props.activeFilterLabel}`, W / 2, H - 12)
}

// ── Dispatch ─────────────────────────────────────────────────────────────────
async function renderStrip() {
  const canvas = canvasRef.value
  if (!canvas) return

  const images = await Promise.all(props.frames.map((f) => loadImage(f.src)))

  switch (activeTemplateId.value) {
    case 'dark':     renderDark(canvas, images);     break
    case 'film':     renderFilm(canvas, images);     break
    case 'polaroid': renderPolaroid(canvas, images); break
    case 'minimal':  renderMinimal(canvas, images);  break
    default:         renderClassic(canvas, images);  break
  }
}

async function clearStrip() {
  await nextTick()
  const canvas = canvasRef.value
  const context = canvas?.getContext('2d')
  if (canvas && context) {
    context.clearRect(0, 0, canvas.width, canvas.height)
  }
}

watch(
  [() => props.frames, activeTemplateId],
  async ([frames]) => {
    if (frames.length === 3) {
      await nextTick()
      await renderStrip()
      return
    }
    await clearStrip()
  },
  { deep: true, immediate: true },
)

function downloadStrip(filterLabel) {
  const canvas = canvasRef.value
  if (!canvas || props.frames.length !== 3) return

  canvas.toBlob((blob) => {
    if (!blob) return
    const objectUrl = URL.createObjectURL(blob)
    const link = document.createElement('a')
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
    link.href = objectUrl
    link.download = `lux-${activeTemplateId.value}-${filterLabel.toLowerCase().replace(/\s+/g, '-')}-${timestamp}.png`
    link.click()
    URL.revokeObjectURL(objectUrl)
  }, 'image/png')
}

defineExpose({ downloadStrip })
</script>

<template>
  <section class="glass-panel rounded-[28px] p-5">
    <div class="mb-4 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between sm:gap-3">
      <div class="min-w-0">
        <h2 class="text-sm font-medium text-white">Photostrip preview</h2>
        <p class="text-xs text-zinc-400">
          {{ templates.find(t => t.id === activeTemplateId)?.description ?? 'Select a template below.' }}
        </p>
      </div>
      <span class="w-fit rounded-full border border-white/10 bg-white/5 px-3 py-1 text-[11px] uppercase tracking-[0.3em] text-zinc-400">400px base</span>
    </div>

    <!-- Template selector -->
    <div class="mb-4 flex flex-wrap gap-2">
      <button
        v-for="t in templates"
        :key="t.id"
        type="button"
        class="rounded-full border px-3 py-1 text-[11px] uppercase tracking-[0.25em] transition"
        :class="activeTemplateId === t.id
          ? 'border-accent/50 bg-accent/15 text-accent'
          : 'border-white/10 bg-white/5 text-zinc-400 hover:border-white/20 hover:text-zinc-200'"
        @click="activeTemplateId = t.id"
      >
        {{ t.label }}
      </button>
    </div>

    <div class="rounded-[24px] border border-white/10 bg-zinc-950/70 p-4">
      <div v-if="frames.length !== 3" class="flex min-h-[14rem] items-center justify-center rounded-[20px] border border-dashed border-white/10 bg-white/[0.03] p-5 text-center text-sm text-zinc-500 sm:min-h-[18rem] sm:p-8">
        Complete the 3-shot session to generate the LUX result strip.
      </div>
      <div v-else class="flex flex-col items-center gap-5 lg:flex-row lg:items-start lg:justify-between">
        <canvas ref="canvasRef" class="w-full max-w-[16rem] rounded-[20px] shadow-2xl shadow-black/30 sm:max-w-[18rem]" />
        <div class="flex w-full flex-col gap-3 sm:flex-row lg:max-w-[13rem] lg:flex-col">
          <button
            type="button"
            class="w-full rounded-xl border border-accent/30 bg-accent/10 px-4 py-3 text-sm font-medium text-accent transition"
            @click="downloadStrip(activeFilterLabel)"
          >
            Download
          </button>
          <button
            type="button"
            class="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-zinc-200 transition"
            @click="emit('retake')"
          >
            Retake
          </button>
          <p class="text-xs text-zinc-400 sm:basis-full lg:basis-auto">{{ watermarkText }}</p>
        </div>
      </div>
    </div>
  </section>
</template>
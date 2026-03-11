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

const STRIP_WIDTH = 400
const PADDING = 20
const FOOTER_HEIGHT = 112
const STRIP_HEIGHT = STRIP_WIDTH * 3 + PADDING * 4 + FOOTER_HEIGHT
const canvasRef = ref(null)

async function loadImage(source) {
  return new Promise((resolve, reject) => {
    const image = new Image()

    image.onload = () => resolve(image)
    image.onerror = reject
    image.src = source
  })
}

function drawCover(context, image, frameX, frameY, frameWidth, frameHeight) {
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

  context.drawImage(image, offsetX, offsetY, drawWidth, drawHeight)
}

async function renderStrip() {
  const canvas = canvasRef.value

  if (!canvas) {
    return
  }

  const context = canvas.getContext('2d')

  if (!context) {
    return
  }

  canvas.width = STRIP_WIDTH
  canvas.height = STRIP_HEIGHT

  context.fillStyle = '#ffffff'
  context.fillRect(0, 0, STRIP_WIDTH, STRIP_HEIGHT)

  const slotWidth = STRIP_WIDTH - PADDING * 2
  const slotHeight = STRIP_WIDTH

  for (const [index, frame] of props.frames.entries()) {
    const image = await loadImage(frame.src)
    const frameY = PADDING + index * (slotHeight + PADDING)

    context.save()
    context.beginPath()
    context.rect(PADDING, frameY, slotWidth, slotHeight)
    context.clip()
    drawCover(context, image, PADDING, frameY, slotWidth, slotHeight)
    context.restore()

    context.strokeStyle = 'rgba(229, 231, 235, 0.9)'
    context.lineWidth = 2
    context.strokeRect(PADDING, frameY, slotWidth, slotHeight)
  }

  context.fillStyle = '#0f172a'
  context.font = '600 28px Geist Variable, sans-serif'
  context.textAlign = 'center'
  context.fillText(props.watermarkText, STRIP_WIDTH / 2, STRIP_HEIGHT - 44)

  context.fillStyle = '#64748b'
  context.font = '500 14px Geist Variable, sans-serif'
  context.fillText(`${props.activeFilterLabel} preset`, STRIP_WIDTH / 2, STRIP_HEIGHT - 18)
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
  () => props.frames,
  async (frames) => {
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

  if (!canvas || props.frames.length !== 3) {
    return
  }

  canvas.toBlob((blob) => {
    if (!blob) {
      return
    }

    const objectUrl = URL.createObjectURL(blob)
    const link = document.createElement('a')
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-')

    link.href = objectUrl
    link.download = `lux-photostrip-${filterLabel.toLowerCase().replace(/\s+/g, '-')}-${timestamp}.png`
    link.click()
    URL.revokeObjectURL(objectUrl)
  }, 'image/png')
}

defineExpose({
  downloadStrip,
})
</script>

<template>
  <section class="glass-panel rounded-[28px] p-5">
    <div class="mb-4 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between sm:gap-3">
      <div class="min-w-0">
        <h2 class="text-sm font-medium text-white">Photostrip preview</h2>
        <p class="text-xs text-zinc-400">Three captures stitched into a classic white-bordered booth strip.</p>
      </div>
      <span class="w-fit rounded-full border border-white/10 bg-white/5 px-3 py-1 text-[11px] uppercase tracking-[0.3em] text-zinc-400">400px base</span>
    </div>

    <div class="rounded-[24px] border border-white/10 bg-zinc-950/70 p-4">
      <div v-if="frames.length !== 3" class="flex min-h-[14rem] items-center justify-center rounded-[20px] border border-dashed border-white/10 bg-white/[0.03] p-5 text-center text-sm text-zinc-500 sm:min-h-[18rem] sm:p-8">
        Complete the 3-shot session to generate the LUX result strip.
      </div>
      <div v-else class="flex flex-col items-center gap-5 lg:flex-row lg:items-start lg:justify-between">
        <canvas ref="canvasRef" class="w-full max-w-[16rem] rounded-[20px] bg-white shadow-2xl shadow-black/30 sm:max-w-[18rem]" />
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
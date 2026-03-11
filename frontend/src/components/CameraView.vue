<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

import { useTimer } from '../composables/useTimer'
import CaptureActions from './CaptureActions.vue'
import FilterDock from './FilterDock.vue'
import StripPreview from './StripPreview.vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const SESSION_SHOTS = 3
const START_COUNTDOWN_SECONDS = 5
const BETWEEN_SHOT_SECONDS = 3

const fallbackPresets = [
  {
    id: 'bw',
    label: 'B&W',
    filter: 'grayscale(100%) contrast(1.18) brightness(0.96)',
    description: 'Classic monochrome strip with crisp contrast.',
    thumbnailGradient: 'from-stone-200 via-stone-500 to-stone-900',
  },
  {
    id: 'film',
    label: 'Film',
    filter: 'sepia(18%) contrast(1.08) saturate(0.94) brightness(0.99)',
    description: 'Muted cinematic tone for a soft analog finish.',
    thumbnailGradient: 'from-zinc-200 via-neutral-500 to-zinc-900',
  },
  {
    id: 'warm',
    label: 'Warm',
    filter: 'sepia(28%) saturate(1.18) brightness(1.03) hue-rotate(-8deg)',
    description: 'Golden booth tones with a gentle skin-friendly lift.',
    thumbnailGradient: 'from-amber-200 via-orange-400 to-rose-700',
  },
  {
    id: 'grain',
    label: 'Grain',
    filter: 'contrast(1.08) saturate(0.92) brightness(0.98)',
    description: 'Subtle texture and contrast for a Snappy-style finish.',
    thumbnailGradient: 'from-zinc-100 via-zinc-400 to-zinc-800',
  },
  {
    id: 'clean',
    label: 'Clean',
    filter: 'none',
    description: 'Balanced tones for a neutral booth strip.',
    thumbnailGradient: 'from-zinc-300 via-zinc-500 to-zinc-800',
  },
]

const fallbackConfig = {
  brandName: 'LUX',
  eventLabel: 'March 2026',
  watermarkText: 'LUX | March 2026',
}

const videoRef = ref(null)
const captureCanvasRef = ref(null)
const stripPreviewRef = ref(null)
const stream = ref(null)
const presets = ref(fallbackPresets)
const config = ref(fallbackConfig)
const activePresetId = ref('bw')
const capturedFrames = ref([])
const isCameraReady = ref(false)
const sessionActive = ref(false)
const flashActive = ref(false)
const countdownLabel = ref('')
const statusMessage = ref('Allow camera access, adjust your pose, and tap Ready? Start when you are set.')
const errorMessage = ref('')

const { countdownValue, runCountdown, resetTimer } = useTimer(5)

const activePreset = computed(
  () => presets.value.find((preset) => preset.id === activePresetId.value) || presets.value[0],
)

const activeFilter = computed(() => activePreset.value?.filter || 'none')
const hasStrip = computed(() => capturedFrames.value.length === SESSION_SHOTS)
const canStartSession = computed(() => isCameraReady.value && !sessionActive.value)
const shouldShowFilmGrainOverlay = computed(() => activePreset.value?.id === 'grain')
const currentShot = computed(() => Math.min(capturedFrames.value.length + 1, SESSION_SHOTS))

async function loadPresets() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/filter-presets`)

    if (!response.ok) {
      throw new Error('Preset request failed.')
    }

    const data = await response.json()

    if (Array.isArray(data.presets) && data.presets.length > 0) {
      presets.value = data.presets
    }
  } catch {
    statusMessage.value = 'Using bundled presets locally. The backend only provides metadata, not storage.'
  }
}

async function loadConfig() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/config`)

    if (!response.ok) {
      throw new Error('Config request failed.')
    }

    const data = await response.json()

    if (data?.watermarkText) {
      config.value = data
    }
  } catch {
    config.value = fallbackConfig
  }
}

async function startCamera() {
  try {
    stream.value = await navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: 'user',
        width: { ideal: 1280 },
        height: { ideal: 720 },
      },
      audio: false,
    })

    if (videoRef.value) {
      videoRef.value.srcObject = stream.value
      await videoRef.value.play()
      isCameraReady.value = true
      statusMessage.value = 'Camera ready. Start when you are ready for your first countdown.'
    }
  } catch (error) {
    errorMessage.value = 'Camera access was denied or is unavailable in this browser.'
    statusMessage.value = ''
    console.error(error)
  }
}

async function triggerFlash() {
  flashActive.value = true
  await new Promise((resolve) => window.setTimeout(resolve, 140))
  flashActive.value = false
}

function drawFilmGrain(context, width, height) {
  for (let index = 0; index < 900; index += 1) {
    const x = Math.random() * width
    const y = Math.random() * height
    const opacity = Math.random() * 0.14
    const size = Math.random() * 1.8 + 0.4

    context.fillStyle = `rgba(255, 255, 255, ${opacity})`
    context.fillRect(x, y, size, size)
  }
}

function captureFrame() {
  if (!videoRef.value || !captureCanvasRef.value || !isCameraReady.value) {
    return null
  }

  const video = videoRef.value
  const canvas = captureCanvasRef.value
  const context = canvas.getContext('2d')

  if (!context) {
    return null
  }

  const width = video.videoWidth || 1280
  const height = video.videoHeight || 720

  canvas.width = width
  canvas.height = height
  context.clearRect(0, 0, width, height)
  context.save()
  context.translate(width, 0)
  context.scale(-1, 1)
  context.filter = activeFilter.value
  context.drawImage(video, 0, 0, width, height)
  context.restore()
  context.filter = 'none'

  if (activePreset.value.id === 'grain') {
    drawFilmGrain(context, width, height)
  }

  return {
    id: crypto.randomUUID(),
    src: canvas.toDataURL('image/png'),
    presetId: activePreset.value.id,
    filterLabel: activePreset.value.label,
  }
}

async function startSession() {
  if (!canStartSession.value) {
    return
  }

  capturedFrames.value = []
  sessionActive.value = true
  errorMessage.value = ''

  try {
    for (let shotNumber = 1; shotNumber <= SESSION_SHOTS; shotNumber += 1) {
      countdownLabel.value = shotNumber === 1 ? 'Get Ready' : 'Strike a Pose'
      statusMessage.value = `${countdownLabel.value}. Shot ${shotNumber} of ${SESSION_SHOTS}.`
      await runCountdown(shotNumber === 1 ? START_COUNTDOWN_SECONDS : BETWEEN_SHOT_SECONDS)
      await triggerFlash()

      const frame = captureFrame()

      if (!frame) {
        throw new Error('Could not capture frame.')
      }

      capturedFrames.value = [...capturedFrames.value, frame]
      statusMessage.value = `Captured shot ${shotNumber} of ${SESSION_SHOTS}.`
    }

    statusMessage.value = 'Photostrip ready. Download it locally or retake the whole session.'
  } catch (error) {
    errorMessage.value = 'The session could not be completed. Check camera access and try again.'
    console.error(error)
  } finally {
    sessionActive.value = false
    countdownLabel.value = ''
    resetTimer()
  }
}

function retakeSession() {
  capturedFrames.value = []
  flashActive.value = false
  countdownLabel.value = ''
  resetTimer()
  statusMessage.value = 'Session reset. Ready when you are.'
}

function stopCamera() {
  stream.value?.getTracks().forEach((track) => track.stop())
}

onMounted(async () => {
  await loadConfig()
  await loadPresets()
  await startCamera()
})

onBeforeUnmount(() => {
  stopCamera()
})
</script>

<template>
  <main class="grid w-full gap-4 md:gap-6 xl:grid-cols-[1.35fr_0.95fr]">
    <section class="fade-up flex flex-col gap-4">
      <div class="glass-panel overflow-hidden rounded-[24px] p-2.5 shadow-lens sm:rounded-[32px] sm:p-3">
        <div class="relative aspect-[3/4] overflow-hidden rounded-[20px] border border-white/10 bg-zinc-900 sm:aspect-[4/5] sm:rounded-[26px]">
          <video
            ref="videoRef"
            autoplay
            playsinline
            muted
            class="h-full w-full object-cover"
            :style="{ filter: activeFilter, transform: 'scaleX(-1)' }"
          />

          <div v-if="shouldShowFilmGrainOverlay" class="grain-overlay" />
          <div v-if="flashActive" class="flash-overlay pointer-events-none absolute inset-0 bg-white" />

          <div class="pointer-events-none absolute inset-x-0 top-0 flex items-center justify-between p-2.5 sm:p-4">
            <span class="rounded-full border border-white/10 bg-black/25 px-2.5 py-1 text-[10px] uppercase tracking-[0.22em] text-zinc-300 sm:px-3 sm:text-[11px] sm:tracking-[0.3em]">
              Local only
            </span>
            <span class="rounded-full border border-accent/20 bg-accent/10 px-2.5 py-1 text-[10px] uppercase tracking-[0.22em] text-accent sm:px-3 sm:text-[11px] sm:tracking-[0.3em]">
              {{ activePreset.label }}
            </span>
          </div>

          <div v-if="sessionActive && countdownValue" class="pointer-events-none absolute inset-0 flex items-center justify-center bg-black/20">
            <div class="text-center">
              <p class="mb-2 text-[10px] uppercase tracking-[0.3em] text-white/60 sm:text-xs sm:tracking-[0.45em]">{{ countdownLabel }}</p>
              <span :key="countdownValue" class="countdown-pop block text-7xl font-semibold tracking-tight text-white drop-shadow-[0_0_40px_rgba(255,255,255,0.35)] sm:text-8xl md:text-9xl">
                {{ countdownValue }}
              </span>
            </div>
          </div>

        </div>
      </div>

      <CaptureActions
        :session-active="sessionActive"
        :can-start="canStartSession"
        :current-shot="currentShot"
        :total-shots="SESSION_SHOTS"
        :countdown-value="countdownValue"
        :countdown-label="countdownLabel"
        :has-result="hasStrip"
        :active-filter-label="activePreset.label"
        @start="startSession"
      />

      <canvas ref="captureCanvasRef" class="hidden" />
    </section>

    <aside class="fade-up flex flex-col gap-4" style="animation-delay: 120ms">
      <StripPreview
        ref="stripPreviewRef"
        :frames="capturedFrames"
        :active-filter-label="activePreset.label"
        :watermark-text="config.watermarkText"
        @retake="retakeSession"
      />

      <FilterDock
        :presets="presets"
        :active-preset-id="activePresetId"
        @select="activePresetId = $event"
      />
    </aside>
  </main>
</template>
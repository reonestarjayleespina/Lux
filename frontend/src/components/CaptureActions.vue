<script setup>
defineProps({
  sessionActive: {
    type: Boolean,
    required: true,
  },
  canStart: {
    type: Boolean,
    required: true,
  },
  currentShot: {
    type: Number,
    required: true,
  },
  totalShots: {
    type: Number,
    required: true,
  },
  countdownValue: {
    type: Number,
    default: 0,
  },
  countdownLabel: {
    type: String,
    default: '',
  },
  hasResult: {
    type: Boolean,
    required: true,
  },
  activeFilterLabel: {
    type: String,
    required: true,
  },
})

const emit = defineEmits(['start'])
</script>

<template>
  <section class="glass-panel rounded-[30px] p-4 sm:p-5">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div class="min-w-0">
        <p class="text-xs uppercase tracking-[0.35em] text-zinc-500">Session Controls</p>
        <p class="mt-2 text-sm text-zinc-300 break-words">
          Active preset: <span class="font-medium text-white">{{ activeFilterLabel }}</span>
        </p>
        <p class="mt-2 text-sm text-zinc-400 break-words">
          {{ sessionActive
            ? `${countdownLabel || 'Get Ready'} for shot ${currentShot} of ${totalShots}.`
            : hasResult
              ? 'Your final strip is ready for download or retake.'
              : 'Three photos. One white-bordered strip. Stored only on this device.' }}
        </p>
      </div>

      <div class="flex w-full flex-wrap items-center justify-center gap-3 self-center sm:w-auto sm:self-auto">
        <button
          type="button"
          class="relative flex h-14 w-full items-center justify-center rounded-full border border-accent/40 bg-white/5 px-6 text-sm font-medium text-white shadow-[0_0_24px_-10px_rgba(94,234,212,0.9)] transition disabled:cursor-not-allowed disabled:opacity-50 sm:h-20 sm:min-w-[11rem] sm:w-auto"
          :disabled="!canStart || sessionActive || hasResult"
          @click="emit('start')"
        >
          <span class="capture-ring absolute inset-0 rounded-full" :class="sessionActive ? 'hidden' : 'block'" />
          <span>{{ sessionActive ? `${countdownLabel || 'Get Ready'} ${countdownValue || '...'}` : 'Ready? Start' }}</span>
        </button>
      </div>
    </div>
  </section>
</template>
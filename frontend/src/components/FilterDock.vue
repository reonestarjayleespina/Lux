<script setup>
defineProps({
  presets: {
    type: Array,
    required: true,
  },
  activePresetId: {
    type: String,
    required: true,
  },
})

const emit = defineEmits(['select'])
</script>

<template>
  <section class="glass-panel rounded-[28px] p-4 sm:p-5">
    <div class="mb-3 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between sm:gap-3">
      <div class="min-w-0">
        <h2 class="text-sm font-medium text-white">Filter dock</h2>
        <p class="text-xs text-zinc-400">The live mirror view and the final strip share the same filter preset.</p>
      </div>
      <span class="w-fit rounded-full border border-white/10 bg-white/5 px-3 py-1 text-[11px] uppercase tracking-[0.3em] text-zinc-400">
        Live preset
      </span>
    </div>

    <div class="filter-scrollbar flex gap-3 overflow-x-auto pb-1">
      <button
        v-for="preset in presets"
        :key="preset.id"
        type="button"
        class="group min-w-[100px] rounded-3xl border px-3 py-3 text-left transition-all duration-200 sm:min-w-[112px]"
        :class="preset.id === activePresetId
          ? 'border-accent bg-accent/10 shadow-[0_0_24px_-10px_rgba(94,234,212,0.8)]'
          : 'border-white/10 bg-white/5'"
        @click="emit('select', preset.id)"
      >
        <div
          class="mb-3 h-14 w-14 rounded-full bg-gradient-to-br ring-1 ring-white/10 sm:h-16 sm:w-16"
          :class="preset.thumbnailGradient"
        />
        <p class="text-sm font-medium text-white">{{ preset.label }}</p>
        <p class="mt-1 line-clamp-2 text-[11px] text-zinc-400">{{ preset.description }}</p>
      </button>
    </div>
  </section>
</template>
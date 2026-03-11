<script setup>
import CameraView from './components/CameraView.vue'
</script>

<template>
  <div class="min-h-screen bg-zinc-950 bg-hero-radial px-3 py-5 text-zinc-50 sm:px-6 sm:py-8 lg:px-8">
    <div class="mx-auto flex min-h-[calc(100vh-2.5rem)] w-full max-w-6xl flex-col justify-center gap-5 sm:min-h-[calc(100vh-4rem)] sm:gap-6">
      <header class="fade-up space-y-6 text-center">
        <p class="text-xs uppercase tracking-[0.5em]" style="color: rgba(255, 255, 255, 0.6)">LUX</p>
        <p class="mx-auto max-w-2xl text-sm uppercase tracking-wider text-zinc-400 pt-3">
          Simple. Bright. Timeless.
        </p>
      </header>

      <CameraView />
    </div>
  </div>
</template>
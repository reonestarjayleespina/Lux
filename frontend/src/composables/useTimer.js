import { ref } from 'vue'

export function useTimer(initialValue = 5) {
  const countdownValue = ref(0)
  let intervalId = null

  function resetTimer() {
    if (intervalId) {
      clearInterval(intervalId)
      intervalId = null
    }

    countdownValue.value = 0
  }

  function runCountdown(duration = initialValue) {
    resetTimer()
    countdownValue.value = duration

    return new Promise((resolve) => {
      intervalId = setInterval(() => {
        countdownValue.value -= 1

        if (countdownValue.value <= 0) {
          resetTimer()
          resolve()
        }
      }, 1000)
    })
  }

  return {
    countdownValue,
    resetTimer,
    runCountdown,
  }
}
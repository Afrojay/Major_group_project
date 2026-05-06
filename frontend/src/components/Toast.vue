<template>
  <div
    role="status"
    aria-live="polite"
    aria-atomic="true"
    class="toast-container"
  >
    <transition-group
      name="toast"
      tag="div"
      class="space-y-2"
    >
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="[
          'toast',
          `toast-${toast.type}`,
        ]"
      >
        <p>{{ toast.message }}</p>
        <button
          type="button"
          aria-label="Close notification"
          @click="appStore.removeToast(toast.id)"
          class="text-sm ml-2 opacity-70 hover:opacity-100"
        >
          ✕
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()
const toasts = computed(() => appStore.toastMessages)
</script>

<style scoped>
.toast-container {
  @apply fixed bottom-4 right-4 z-50 pointer-events-none;
}

.toast {
  @apply bg-surface border border-line rounded-lg px-4 py-3 shadow-app pointer-events-auto flex items-center;
}

.toast-success {
  @apply border-green-500 bg-green-50 text-green-900;
}

.toast-error {
  @apply border-red-500 bg-red-50 text-red-900;
}

.toast-warning {
  @apply border-yellow-500 bg-yellow-50 text-yellow-900;
}

.toast-info {
  @apply border-blue-500 bg-blue-50 text-blue-900;
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.toast-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>

<template>
  <div class="spinner" role="status" aria-label="Loading">
    <div class="spinner-ring"></div>
    <p v-if="text" class="text-center mt-2 text-muted">{{ text }}</p>
  </div>
</template>

<script setup>
defineProps({
  text: {
    type: String,
    default: '',
  },
})
</script>

<style scoped>
.spinner {
  @apply flex flex-col items-center justify-center;
}

.spinner-ring {
  @apply inline-block w-8 h-8 border-4 border-line rounded-full;
  border-top-color: var(--accent);
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (prefers-reduced-motion: reduce) {
  .spinner-ring {
    animation: none;
    border-top-color: var(--line);
  }
}
</style>

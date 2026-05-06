<template>
  <div class="card">
    <slot />
  </div>
</template>

<script setup>
defineProps({
  hoverable: {
    type: Boolean,
    default: false,
  },
})
</script>

<style scoped>
.card {
  @apply bg-surface border border-line rounded-lg p-4 shadow-subtle transition-shadow;
}

.card:hover {
  @apply shadow-app;
}
</style>

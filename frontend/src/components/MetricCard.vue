<template>
  <Card class="flex flex-col items-center text-center">
    <span class="text-4xl font-bold text-accent mb-2">{{ value }}</span>
    <p class="text-muted">{{ label }}</p>
    <a
      v-if="href"
      :href="href"
      class="mt-4 text-sm font-semibold text-accent hover:underline"
    >
      View details →
    </a>
  </Card>
</template>

<script setup>
import Card from './Card.vue'

defineProps({
  value: {
    type: [String, Number],
    required: true,
  },
  label: {
    type: String,
    required: true,
  },
  href: {
    type: String,
    default: null,
  },
})
</script>

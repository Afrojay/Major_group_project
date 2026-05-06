<template>
  <div class="filter-panel" :aria-labelledby="headingId">
    <h3 :id="headingId" class="font-semibold mb-3">{{ title }}</h3>
    <div class="flex flex-wrap gap-2">
      <a
        v-for="item in items"
        :key="item.value"
        :href="item.href"
        :class="[
          'filter-chip px-3 py-2 rounded-full text-sm font-medium transition-colors',
          item.active
            ? 'bg-accent text-accent-ink'
            : 'bg-line text-ink hover:bg-muted'
        ]"
        :aria-current="item.active ? 'page' : null"
      >
        {{ item.label }}
      </a>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  items: {
    type: Array,
    required: true,
    validator: (arr) => arr.every(item => item.label && item.href && ('active' in item)),
  },
})

const headingId = computed(() => `filter-${Math.random().toString(36).substr(2, 9)}`)
</script>

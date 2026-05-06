<template>
  <div :aria-label="ariaLabel" role="region" class="grid grid-cols-1 gap-4" :class="gridClass">
    <slot />
  </div>
</template>

<script setup>
defineProps({
  columns: {
    type: Number,
    default: 3,
    validator: (v) => [2, 3, 4].includes(v),
  },
  ariaLabel: {
    type: String,
    default: null,
  },
})

const gridClass = {
  2: 'sm:grid-cols-2 lg:grid-cols-2',
  3: 'sm:grid-cols-2 lg:grid-cols-3',
  4: 'sm:grid-cols-2 lg:grid-cols-4',
}
</script>

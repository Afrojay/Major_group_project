<template>
  <section v-if="items.length > 0" role="region" :aria-label="ariaLabel" class="section">
    <h2>{{ title }}</h2>
    <div :class="gridClass">
      <slot :item="item" v-for="item in items" :key="item.id" />
    </div>
  </section>
  <section v-else class="section">
    <h2>{{ title }}</h2>
    <p class="text-muted text-center py-8">{{ emptyMessage }}</p>
  </section>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  items: {
    type: Array,
    required: true,
  },
  emptyMessage: {
    type: String,
    default: 'No items to display.',
  },
  columns: {
    type: Number,
    default: 3,
  },
  ariaLabel: {
    type: String,
    default: null,
  },
})

const gridClass = {
  2: 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 gap-4',
  3: 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4',
  4: 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4',
}
</script>

<style scoped>
.section {
  @apply py-8 px-4 max-w-5xl mx-auto;
}

h2 {
  @apply text-2xl font-bold mb-6;
}
</style>

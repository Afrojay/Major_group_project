<template>
  <nav :aria-label="ariaLabel" class="breadcrumb">
    <ol class="flex flex-wrap gap-2 items-center">
      <li v-for="(item, index) in items" :key="index" class="flex items-center gap-2">
        <a
          v-if="item.href"
          :href="item.href"
          class="text-accent hover:underline"
        >
          {{ item.label }}
        </a>
        <span v-else class="text-ink">{{ item.label }}</span>
        <span
          v-if="index < items.length - 1"
          aria-hidden="true"
          class="text-muted"
        >
          /
        </span>
      </li>
    </ol>
  </nav>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    required: true,
    validator: (arr) => arr.every(item => item.label && (item.href || item.label)),
  },
  ariaLabel: {
    type: String,
    default: 'Breadcrumb',
  },
})
</script>

<style scoped>
.breadcrumb {
  @apply py-2 mb-4;
}

ol {
  list-style: none;
  padding: 0;
  margin: 0;
}
</style>

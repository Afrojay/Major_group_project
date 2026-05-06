<template>
  <Card class="flex flex-col">
    <p v-if="category" class="eyebrow mb-2">{{ category }}</p>
    <h3 class="text-lg font-bold mb-2">{{ term }}</h3>
    <p v-if="description" class="text-muted mb-3">{{ description }}</p>
    <p v-if="tags" class="text-sm text-muted mb-4 space-x-1">
      <span v-for="tag in tags.split(',')" :key="tag.trim()" class="inline-block bg-line px-2 py-1 rounded text-xs">
        {{ tag.trim() }}
      </span>
    </p>
    <div class="mt-auto flex gap-2">
      <a
        :href="href"
        class="button text-sm flex-1 text-center"
      >
        View sign
      </a>
      <button
        v-if="showFavouriteButton"
        type="button"
        :aria-label="isFavourite ? 'Remove from favourites' : 'Add to favourites'"
        :aria-pressed="isFavourite"
        :class="['button secondary text-sm w-10 h-10 p-0 flex items-center justify-center', { 'bg-accent text-accent-ink': isFavourite }]"
        @click="$emit('toggle-favourite')"
        title="Toggle favourite"
      >
        <span aria-hidden="true">{{ isFavourite ? '♥' : '♡' }}</span>
      </button>
    </div>
  </Card>
</template>

<script setup>
defineProps({
  term: {
    type: String,
    required: true,
  },
  category: {
    type: String,
    default: null,
  },
  description: {
    type: String,
    default: null,
  },
  tags: {
    type: String,
    default: null,
  },
  href: {
    type: String,
    required: true,
  },
  isFavourite: {
    type: Boolean,
    default: false,
  },
  showFavouriteButton: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['toggle-favourite'])
</script>

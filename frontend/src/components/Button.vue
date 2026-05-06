<template>
  <button
    :class="[
      'button',
      {
        'secondary': variant === 'secondary',
        'tertiary': variant === 'tertiary',
        'danger': variant === 'danger',
      }
    ]"
    :disabled="disabled"
    :aria-label="ariaLabel"
    :aria-disabled="disabled"
    @click="$emit('click')"
  >
    <slot />
  </button>
</template>

<script setup>
defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (v) => ['primary', 'secondary', 'tertiary', 'danger'].includes(v),
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  ariaLabel: {
    type: String,
    default: null,
  },
})

defineEmits(['click'])
</script>

<style scoped>
button {
  @apply inline-flex items-center justify-center gap-2 px-4 py-2 font-semibold rounded-md transition-all duration-150 ease-out cursor-pointer;
  @apply bg-accent text-accent-ink hover:shadow-md active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed;
}

.secondary {
  @apply bg-line text-ink hover:bg-muted;
}

.tertiary {
  @apply bg-transparent text-accent hover:bg-accent hover:text-accent-ink border border-accent;
}

.danger {
  @apply bg-red-600 text-white hover:bg-red-700;
}

button:focus-visible {
  @apply outline-none ring-2 ring-offset-2 ring-accent;
}
</style>

<template>
  <div class="form-group">
    <label v-if="label" :for="id" class="form-label">
      {{ label }}
      <span v-if="required" class="text-red-600 ml-0.5" aria-label="required">*</span>
    </label>
    <!-- Slot content receives aria-describedby and aria-invalid attrs -->
    <div 
      :aria-describedby="descriptionId"
      :data-aria-required="required"
    >
      <slot />
    </div>
    <p v-if="error" :id="errorId" class="form-error" role="alert">
      <span class="inline-block w-0 h-0 overflow-hidden">Error:</span> {{ error }}
    </p>
    <p v-if="hint" :id="hintId" class="form-hint">{{ hint }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: {
    type: String,
    default: null,
  },
  id: {
    type: String,
    default: null,
  },
  error: {
    type: String,
    default: null,
  },
  hint: {
    type: String,
    default: null,
  },
  required: {
    type: Boolean,
    default: false,
  },
})

const errorId = computed(() => props.id ? `${props.id}-error` : null)
const hintId = computed(() => props.id ? `${props.id}-hint` : null)
const descriptionId = computed(() => {
  const ids = []
  if (props.hint) ids.push(hintId.value)
  if (props.error) ids.push(errorId.value)
  return ids.length > 0 ? ids.join(' ') : undefined
})
</script>

<style scoped>
.form-group {
  @apply mb-4;
}

.form-label {
  @apply block text-sm font-semibold text-ink mb-2;
}

.form-error {
  @apply text-red-600 text-sm mt-1 font-medium;
}

.form-hint {
  @apply text-muted text-sm mt-1;
}
</style>

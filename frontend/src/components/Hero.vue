<template>
  <section class="hero" :style="{ '--accent': accentColor }">
    <div class="hero-content">
      <div v-if="logoUrl || title || eyebrow" class="hero-identity">
        <img
          v-if="logoUrl"
          :src="logoUrl"
          :alt="organisationName"
          class="hero-logo"
        />
        <div>
          <p v-if="eyebrow" class="eyebrow">{{ eyebrow }}</p>
          <h1 v-if="title" class="text-3xl font-bold">{{ title }}</h1>
        </div>
      </div>
      <p v-if="message" class="lead">{{ message }}</p>
      <div v-if="contactEmail || showTime" class="contact-line text-sm text-muted">
        <span v-if="showTime">Local time: {{ currentTime }}</span>
        <span v-if="showTime && contactEmail"> - </span>
        <a v-if="contactEmail" :href="`mailto:${contactEmail}`">Contact: {{ contactEmail }}</a>
      </div>
      <div v-if="actions && actions.length > 0" class="actions flex gap-2 flex-wrap mt-4">
        <a
          v-for="action in actions"
          :key="action.label"
          :href="action.href"
          :class="['button', action.variant === 'secondary' ? 'secondary' : '']"
        >
          {{ action.label }}
        </a>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'

defineProps({
  logoUrl: {
    type: String,
    default: null,
  },
  organisationName: {
    type: String,
    default: null,
  },
  eyebrow: {
    type: String,
    default: null,
  },
  title: {
    type: String,
    required: true,
  },
  message: {
    type: String,
    default: null,
  },
  contactEmail: {
    type: String,
    default: null,
  },
  showTime: {
    type: Boolean,
    default: false,
  },
  actions: {
    type: Array,
    default: () => [],
  },
  accentColor: {
    type: String,
    default: '#0d6efd',
  },
})

const currentTime = ref(new Date().toLocaleTimeString('en-IE', { hour: '2-digit', minute: '2-digit' }))

onMounted(() => {
  const interval = setInterval(() => {
    currentTime.value = new Date().toLocaleTimeString('en-IE', { hour: '2-digit', minute: '2-digit' })
  }, 30000)

  return () => clearInterval(interval)
})
</script>

<style scoped>
.hero {
  @apply bg-surface border-b border-line py-8 px-4;
  background-image: linear-gradient(135deg, var(--accent) 0%, color-mix(in srgb, var(--accent) 80%, white) 100%);
}

.hero-content {
  @apply max-w-4xl mx-auto text-white;
}

.hero-identity {
  @apply flex items-center gap-4 mb-4;
}

.hero-logo {
  @apply w-16 h-16 rounded-lg object-cover;
}

.button {
  @apply bg-white text-blue-600 hover:bg-gray-100;
}

.button.secondary {
  @apply bg-transparent border border-white text-white hover:bg-white hover:bg-opacity-10;
}
</style>

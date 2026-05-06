import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAppStore = defineStore('app', () => {
  // State
  const currentOrganisation = ref(null)
  const currentUser = ref(null)
  const currentStaffProfile = ref(null)
  const favouriteSignIds = ref(new Set())
  const toastMessages = ref([])

  // Computed
  const isAuthenticated = computed(() => !!currentUser.value)
  const isManager = computed(() => currentStaffProfile.value?.can_review_requests)
  const themeColor = computed(() => currentOrganisation.value?.safe_theme_colour || '#0d6efd')

  // Methods
  function setOrganisation(org) {
    currentOrganisation.value = org
  }

  function setUser(user) {
    currentUser.value = user
  }

  function setStaffProfile(profile) {
    currentStaffProfile.value = profile
  }

  function toggleFavourite(signId) {
    if (favouriteSignIds.value.has(signId)) {
      favouriteSignIds.value.delete(signId)
    } else {
      favouriteSignIds.value.add(signId)
    }
  }

  function isFavourite(signId) {
    return favouriteSignIds.value.has(signId)
  }

  function addToast(message, type = 'info', duration = 3000) {
    const id = Date.now()
    const toast = { id, message, type }
    toastMessages.value.push(toast)

    if (duration > 0) {
      setTimeout(() => {
        removeToast(id)
      }, duration)
    }

    return id
  }

  function removeToast(id) {
    toastMessages.value = toastMessages.value.filter(t => t.id !== id)
  }

  return {
    currentOrganisation,
    currentUser,
    currentStaffProfile,
    favouriteSignIds,
    toastMessages,
    isAuthenticated,
    isManager,
    themeColor,
    setOrganisation,
    setUser,
    setStaffProfile,
    toggleFavourite,
    isFavourite,
    addToast,
    removeToast,
  }
})

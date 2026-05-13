(function () {
  const mountEl = document.getElementById("vue-staff-dashboard");
  if (!mountEl || !window.Vue) {
    return;
  }

  const { createApp } = window.Vue;

  createApp({
    delimiters: ["[[", "]]"],
    data() {
      return {
        apiUrl: mountEl.dataset.apiUrl,
        favourites: [],
        recentSigns: [],
        requests: [],
        isLoading: true,
        errorMessage: "",
      };
    },
    computed: {
      summaryText() {
        return `${this.favourites.length} saved, ${this.requests.length} requests`;
      },
    },
    mounted() {
      this.transferAnchorTargets();
      document.documentElement.classList.add("vue-ready");
      this.loadDashboard();
    },
    methods: {
      transferAnchorTargets() {
        mountEl.querySelectorAll("[data-dashboard-target]").forEach((section) => {
          const targetId = section.dataset.dashboardTarget;
          const fallback = document.getElementById(targetId);
          if (fallback) {
            fallback.removeAttribute("id");
          }
          section.id = targetId;
        });

        if (window.location.hash) {
          const target = document.getElementById(window.location.hash.slice(1));
          if (target) {
            window.setTimeout(() => target.scrollIntoView(), 0);
          }
        }
      },
      loadDashboard() {
        fetch(this.apiUrl, {
          headers: {
            Accept: "application/json",
          },
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("Dashboard summary unavailable.");
            }
            return response.json();
          })
          .then((payload) => {
            this.favourites = payload.favourites || [];
            this.recentSigns = payload.recent_signs || [];
            this.requests = payload.requests || [];
          })
          .catch(() => {
            this.errorMessage = "The enhanced dashboard summary is unavailable. The standard dashboard sections are still below.";
          })
          .finally(() => {
            this.isLoading = false;
          });
      },
    },
  }).mount(mountEl);
})();

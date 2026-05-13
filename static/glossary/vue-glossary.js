(function () {
  const mountEl = document.getElementById("vue-glossary-app");
  if (!mountEl || !window.Vue) {
    return;
  }

  const { createApp } = window.Vue;

  createApp({
    delimiters: ["[[", "]]"],
    data() {
      return {
        apiUrl: mountEl.dataset.apiUrl,
        filters: {
          q: mountEl.dataset.initialQuery || "",
          category: mountEl.dataset.initialCategory || "",
          letter: mountEl.dataset.initialLetter || "",
        },
        signs: [],
        count: 0,
        isLoading: false,
        errorMessage: "",
        debounceTimer: null,
      };
    },
    computed: {
      headingText() {
        if (this.filters.q && this.filters.letter) {
          return `Results for "${this.filters.q}" beginning with ${this.filters.letter}`;
        }
        if (this.filters.q) {
          return `Results for "${this.filters.q}"`;
        }
        if (this.filters.letter) {
          return `Signs beginning with ${this.filters.letter}`;
        }
        return "All signs";
      },
      countText() {
        return `${this.count} result${this.count === 1 ? "" : "s"}`;
      },
    },
    mounted() {
      document.documentElement.classList.add("vue-ready");
      this.fetchSigns();
    },
    methods: {
      setLetter(letter) {
        this.filters.letter = letter;
        this.fetchSigns();
      },
      fetchSigns() {
        window.clearTimeout(this.debounceTimer);
        this.debounceTimer = window.setTimeout(() => {
          this.loadSigns();
        }, 180);
      },
      loadSigns() {
        const params = new URLSearchParams();
        if (this.filters.q) {
          params.set("q", this.filters.q);
        }
        if (this.filters.category) {
          params.set("category", this.filters.category);
        }
        if (this.filters.letter) {
          params.set("letter", this.filters.letter);
        }

        this.isLoading = true;
        this.errorMessage = "";

        fetch(`${this.apiUrl}?${params.toString()}`, {
          headers: {
            Accept: "application/json",
          },
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("The glossary could not be loaded.");
            }
            return response.json();
          })
          .then((payload) => {
            this.signs = payload.results || [];
            this.count = payload.count || 0;
          })
          .catch(() => {
            this.errorMessage = "The enhanced glossary search is unavailable. The standard page results are still available below.";
          })
          .finally(() => {
            this.isLoading = false;
          });
      },
    },
  }).mount(mountEl);
})();

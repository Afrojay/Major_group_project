(function () {
  const mountEl = document.getElementById("vue-glossary-app");
  if (!mountEl || !window.Vue) {
    return;
  }

  const { createApp } = window.Vue;
  const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
      return parts.pop().split(";").shift();
    }
    return "";
  };

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
      favouriteLabel(sign) {
        return `${sign.is_favourite ? "Remove" : "Add"} ${sign.term} ${sign.is_favourite ? "from" : "to"} favourites`;
      },
      toggleFavourite(sign) {
        fetch(sign.favourite_url, {
          method: "POST",
          headers: {
            Accept: "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
          },
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("The favourite could not be updated.");
            }
            return response.json();
          })
          .then((payload) => {
            sign.is_favourite = payload.is_favourite;
          })
          .catch(() => {
            this.errorMessage = "The favourite could not be updated. Open the sign detail page and try again.";
          });
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

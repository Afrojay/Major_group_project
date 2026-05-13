(function () {
  const mountEl = document.getElementById("vue-sign-detail");
  const dataEl = document.getElementById("sign-detail-data");
  if (!mountEl || !dataEl || !window.Vue) {
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
        sign: JSON.parse(dataEl.textContent),
        statusMessage: "",
      };
    },
    computed: {
      favouriteLabel() {
        return `${this.sign.is_favourite ? "Remove" : "Add"} ${this.sign.term} ${this.sign.is_favourite ? "from" : "to"} favourites`;
      },
    },
    mounted() {
      document.documentElement.classList.add("vue-ready");
    },
    methods: {
      toggleFavourite() {
        fetch(this.sign.favourite_url, {
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
            this.sign.is_favourite = payload.is_favourite;
            this.statusMessage = payload.message;
          })
          .catch(() => {
            this.statusMessage = "The favourite could not be updated. Try the standard button below.";
          });
      },
    },
  }).mount(mountEl);
})();

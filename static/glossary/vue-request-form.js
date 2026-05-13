(function () {
  const formEl = document.getElementById("vue-sign-request-form");
  if (!formEl || !window.Vue) {
    return;
  }

  const { createApp } = window.Vue;

  createApp({
    delimiters: ["[[", "]]"],
    data() {
      return {
        errors: {
          requester_name: "",
          requester_email: "",
          term: "",
          context: "",
        },
      };
    },
    mounted() {
      formEl.addEventListener("submit", this.handleSubmit);
      ["requester_name", "requester_email", "term", "context"].forEach((name) => {
        const field = this.field(name);
        if (field) {
          field.addEventListener("input", () => this.validateField(name));
          field.addEventListener("blur", () => this.validateField(name));
        }
      });
    },
    methods: {
      field(name) {
        return formEl.querySelector(`[name="${name}"]`);
      },
      value(name) {
        const field = this.field(name);
        return field ? field.value.trim() : "";
      },
      validateField(name) {
        if (name === "requester_name" && this.field(name) && !this.value(name)) {
          this.errors[name] = "Enter your name.";
        } else if (name === "requester_email" && this.field(name) && !this.value(name)) {
          this.errors[name] = "Enter your email address.";
        } else if (name === "requester_email" && this.field(name) && !this.field(name).checkValidity()) {
          this.errors[name] = "Enter a valid email address.";
        } else if (name === "term" && !this.value(name)) {
          this.errors[name] = "Enter the sign or term you need.";
        } else if (name === "context" && !this.value(name)) {
          this.errors[name] = "Explain where or why this sign is needed.";
        } else {
          this.errors[name] = "";
        }

        this.updateAccessibility(name);
        return !this.errors[name];
      },
      updateAccessibility(name) {
        const field = this.field(name);
        if (!field) {
          return;
        }

        const errorId = `${name.replace("_", "-")}-error`;
        if (this.errors[name]) {
          field.setAttribute("aria-invalid", "true");
          field.setAttribute("aria-describedby", errorId);
        } else {
          field.removeAttribute("aria-invalid");
          field.removeAttribute("aria-describedby");
        }
      },
      handleSubmit(event) {
        const fields = ["requester_name", "requester_email", "term", "context"].filter((name) => this.field(name));
        const isValid = fields.every((name) => this.validateField(name));
        if (!isValid) {
          event.preventDefault();
          const firstInvalid = fields.map((name) => this.field(name)).find((field) => field.getAttribute("aria-invalid") === "true");
          if (firstInvalid) {
            firstInvalid.focus();
          }
        }
      },
    },
  }).mount(formEl);
})();

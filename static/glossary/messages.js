(function () {
  const messageRegion = document.querySelector("[data-auto-dismiss-messages]");
  if (!messageRegion) {
    return;
  }

  const dismissMessage = (message) => {
    message.classList.add("message-hiding");
    window.setTimeout(() => {
      message.remove();
      if (!messageRegion.querySelector("[data-message]")) {
        messageRegion.remove();
      }
    }, 180);
  };

  messageRegion.querySelectorAll("[data-message]").forEach((message) => {
    const dismissButton = message.querySelector("[data-dismiss-message]");
    if (dismissButton) {
      dismissButton.addEventListener("click", () => dismissMessage(message));
    }

    const timer = window.setTimeout(() => dismissMessage(message), 3500);
    message.addEventListener("focusin", () => window.clearTimeout(timer), { once: true });
    message.addEventListener("mouseenter", () => window.clearTimeout(timer), { once: true });
  });
})();

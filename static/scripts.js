/**
 * CULTURE SELECTION LOGIC
 * Handles both culture pills and register culture options
 *
 * @format
 */

function setupCultureSelection() {
  // Handle culture pills (e.g., on register page)
  document.querySelectorAll(".culture-pill").forEach((pill) => {
    pill.addEventListener("click", function () {
      const culture = this.getAttribute("data-culture");
      if (!culture) return;

      // Update active state
      document
        .querySelectorAll(".culture-pill")
        .forEach((p) => p.classList.remove("active"));
      this.classList.add("active");

      // Get the computed color value
      const colorValue = getComputedStyle(document.documentElement)
        .getPropertyValue(`--culture-${culture}`)
        .trim();

      // Update CSS variables
      document.documentElement.style.setProperty("--primary-color", colorValue);

      // Update header if exists
      const header = document.querySelector(".register-header");
      if (header) {
        header.style.backgroundColor = colorValue;
      }
    });
  });

  // Handle register culture options
  document.querySelectorAll(".register-culture-option").forEach((option) => {
    option.addEventListener("click", function (e) {
      if (this.tagName === "A") e.preventDefault();

      const culture = this.getAttribute("data-culture");
      if (!culture) return;

      document.querySelectorAll(".register-culture-option").forEach((opt) => {
        opt.classList.remove("active");
      });
      this.classList.add("active");

      const colorValue = getComputedStyle(document.documentElement)
        .getPropertyValue(`--culture-${culture}`)
        .trim();

      document.documentElement.style.setProperty("--primary-color", colorValue);

      const header = document.querySelector(".register-header");
      if (header) {
        header.style.backgroundColor = colorValue;
      }
    });
  });
}

/**
 * SETUP TRANSLATION FORM
 * Handles translation form submission and enhances culture selection
 */
function setupTranslationForm() {
  // Set default culture colors if not already defined
  const root = document.documentElement;
  const computedStyles = getComputedStyle(root);

  if (!computedStyles.getPropertyValue("--culture-american").trim()) {
    root.style.setProperty("--culture-american", "#3b82f6");
  }
  if (!computedStyles.getPropertyValue("--culture-japanese").trim()) {
    root.style.setProperty("--culture-japanese", "#dc2626");
  }
  if (!computedStyles.getPropertyValue("--culture-egyptian").trim()) {
    root.style.setProperty("--culture-egyptian", "#f59e0b");
  }
  if (!computedStyles.getPropertyValue("--culture-indian").trim()) {
    root.style.setProperty("--culture-indian", "#10b981");
  }
  if (!computedStyles.getPropertyValue("--culture-brazilian").trim()) {
    root.style.setProperty("--culture-brazilian", "#8b5cf6");
  }

  // Enhanced culture pill functionality for translation form
  document.querySelectorAll(".culture-pill").forEach((pill) => {
    pill.addEventListener("click", function () {
      const culture = this.getAttribute("data-culture");
      if (!culture) return;

      // Update hidden dialect input if exists
      const dialectInput = document.getElementById("selected-dialect");
      if (dialectInput) {
        dialectInput.value = culture;
      }
    });
  });

  // Form submission handler
  const translationForm = document.getElementById("translation-form");
  if (translationForm) {
    translationForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const form = e.target;
      const formData = new FormData(form);
      const translateBtn = form.querySelector('button[type="submit"]');
      const loader = form.querySelector(".loader");
      const translateText = form.querySelector(".translate-btn-text");
      const outputElement = document.getElementById("translation-output");

      // Guard clause for required elements
      if (!translateBtn || !loader || !translateText || !outputElement) return;

      // Show loading state
      translateBtn.disabled = true;
      loader.style.display = "block";
      translateText.textContent = "Translating...";
      outputElement.textContent = "Translating your message...";

      try {
        const response = await fetch("/translate/", {
          method: "POST",
          body: formData,
        });

        const result = await response.json();

        if (result.success) {
          outputElement.textContent = result.translation;
        } else {
          outputElement.textContent = `Error: ${result.error}`;
        }
      } catch (error) {
        outputElement.textContent = "Network error. Please try again.";
      } finally {
        // Reset button state
        translateBtn.disabled = false;
        loader.style.display = "none";
        translateText.textContent = "Translate";
      }
    });
  }
}

/**
 * PASSWORD TOGGLE LOGIC
 * Handles both register and login page password visibility
 */
function setupPasswordToggles() {
  // Register page toggles
  document.querySelectorAll(".register-toggle-password").forEach((button) => {
    button.addEventListener("click", function () {
      const input = this.previousElementSibling;
      const type =
        input.getAttribute("type") === "password" ? "text" : "password";
      input.setAttribute("type", type);
      this.textContent = type === "password" ? "Show" : "Hide";
    });
  });

  // Login page toggles
  document.querySelectorAll(".login-toggle-password").forEach((button) => {
    button.addEventListener("click", function () {
      const passwordInput = this.previousElementSibling;
      const isPassword = passwordInput.getAttribute("type") === "password";
      passwordInput.setAttribute("type", isPassword ? "text" : "password");
      this.textContent = isPassword ? "Hide" : "Show";
    });
  });
}

/**
 * ERROR HANDLING
 * Applies error styling to form fields
 */
function setupErrorHandling() {
  document.querySelectorAll(".register-error").forEach((error) => {
    const input = error.previousElementSibling?.querySelector("input");
    if (input) {
      input.classList.add("error");
    }
  });
}

/**
 * MESSAGE DISMISSAL
 * Handles both click dismissal and auto-dismissal
 */
function setupMessageDismissal() {
  // Click dismissal
  document.addEventListener("click", function (e) {
    if (e.target.closest(".global-messages__close")) {
      const alert = e.target.closest(".global-messages__alert");
      if (alert) {
        alert.style.animation = "messageSlideOut 0.3s forwards";
        alert.addEventListener("animationend", () => alert.remove(), {
          once: true,
        });
      }
    }
  });

  // Auto-dismissal after 5 seconds
  document.querySelectorAll(".global-messages__alert").forEach((alert) => {
    setTimeout(() => {
      if (alert.parentNode) {
        alert.style.animation = "messageSlideOut 0.3s forwards";
        alert.addEventListener("animationend", () => alert.remove(), {
          once: true,
        });
      }
    }, 5000);
  });
}

/**
 * DEBUG HELPERS
 * Optional logging for troubleshooting
 */
function setupDebugHelpers() {
  document.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", function (e) {
      console.log(`Link clicked: ${this.href}`);
    });
  });
}

// INITIALIZE EVERYTHING WHEN DOM LOADS
document.addEventListener("DOMContentLoaded", function () {
  setupCultureSelection();
  setupPasswordToggles();
  setupErrorHandling();
  setupMessageDismissal();
  setupDebugHelpers();
  setupTranslationForm(); // Add translation functionality

  // Set Egyptian as default culture
  const egyptianPill = document.querySelector(
    '.culture-pill[data-culture="egyptian"]'
  );
  if (egyptianPill) {
    // Activate Egyptian pill
    egyptianPill.classList.add("active");

    // Set default color
    const colorValue =
      getComputedStyle(document.documentElement)
        .getPropertyValue("--culture-egyptian")
        .trim() || "#f59e0b"; // Fallback color

    document.documentElement.style.setProperty("--primary-color", colorValue);

    // Set hidden dialect value
    const dialectInput = document.getElementById("selected-dialect");
    if (dialectInput) {
      dialectInput.value = "egyptian";
    }
  }
});

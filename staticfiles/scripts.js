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
  console.log("🛠️ setupTranslationForm initialized");
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
  if (!translationForm) return;

  // grab the badge that shows “Credits” or “Free tries”
  const creditsCounter = document.getElementById("credits-counter");

  // find our button/text/loader inside the form
  const translateBtn = translationForm.querySelector('button[type="submit"]');
  const translateText = translateBtn.querySelector(".translate-btn-text");
  const loader = translateBtn.querySelector(".loader");

  // read auth state out of a data-attr since this file isn’t templated
  const userAuthenticated =
    translationForm.dataset.userAuthenticated === "true";

  translationForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    // disable & spinner
    translateBtn.disabled = true;
    translateText.style.display = "none";
    loader.style.display = "block";

    try {
      // POST to the same URL your form normally does
      const response = await fetch(translationForm.action, {
        method: "POST",
        body: new FormData(translationForm),
      });
      const data = await response.json();

      // error or “need to register”?
      if (!data.success) {
        if (data.redirect) {
          if (confirm("Free limit reached! Register now to continue.")) {
            window.location.href = "/user/register/"; // or your {% url "register" %}
          }
        } else if (data.error) {
          alert(`Error: ${data.error}`);
        }
        return;
      }

      // SUCCESS: show translation
      document.getElementById("translation-output").textContent =
        data.translation;

      // update the badge
      if (data.remaining != null) {
        if (data.user_authenticated) {
          creditsCounter.textContent = `Credits: ${data.remaining}`;
          creditsCounter.className =
            "text-sm font-medium px-3 py-1 rounded-full bg-blue-100 text-blue-800";
        } else {
          creditsCounter.textContent = `Free tries: ${data.remaining}`;
          if (data.remaining <= 0)
            creditsCounter.className =
              "text-sm font-medium px-3 py-1 rounded-full bg-red-100 text-red-800";
          else if (data.remaining <= 3)
            creditsCounter.className =
              "text-sm font-medium px-3 py-1 rounded-full bg-yellow-100 text-yellow-800";
          else
            creditsCounter.className =
              "text-sm font-medium px-3 py-1 rounded-full bg-green-100 text-green-800";
        }
      }

      // 5) Decide if we should pop up the feedback modal
      const isBad = data.confidence != null && data.confidence < 0.5;
      console.log("🟢 shouldAskFeedback:", shouldAskFeedback(isBad));
      if (shouldAskFeedback(isBad)) {
        console.log("🔔 showing feedback popup now");
        const inputText = document.querySelector('textarea[name="text"]').value;
        const outputText = data.translation;
        const dialect = document.querySelector('select[name="dialect"]').value;
        showFeedbackPopup(inputText, outputText, dialect);
      }
      // ───────────────────────────────────────────
    } catch (err) {
      console.error("Translation error:", err);
      alert("Network error. Please try again.");
    } finally {
      // restore button
      translateText.style.display = "block";
      loader.style.display = "none";
      translateBtn.disabled = false;
    }
  });
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

// 1. COPY BUTTON
function setupCopyButton() {
  const copyBtn = document.getElementById("copy-btn");
  const copySuccess = document.getElementById("copy-success");
  if (!copyBtn) return;

  copyBtn.addEventListener("click", () => {
    const textToCopy =
      document.getElementById("translation-output").textContent;
    const textarea = document.createElement("textarea");
    textarea.value = textToCopy;
    document.body.appendChild(textarea);
    textarea.select();

    try {
      document.execCommand("copy");
      copySuccess.classList.remove("hidden");
      setTimeout(() => copySuccess.classList.add("hidden"), 2000);
    } catch (e) {
      console.error("Copy failed:", e);
    } finally {
      document.body.removeChild(textarea);
    }
  });
}

// 2 Save button
function setupSaveButton() {
  const saveBtn = document.getElementById("save-btn");
  const saveSuccess = document.getElementById("save-success");
  if (!saveBtn) return;
  // read the actual URL from the data attribute
  const saveUrl = saveBtn.dataset.saveUrl;

  saveBtn.addEventListener("click", async () => {
    // re-query dialectSelect here so it’s never undefined
    const dialectSelect = document.getElementById("dialect-select");
    if (!dialectSelect) {
      console.error("dialect-select element not found");
      return;
    }

    const inputText = document.querySelector('textarea[name="text"]').value;
    const outputText =
      document.getElementById("translation-output").textContent;
    const targetCulture =
      dialectSelect.options[dialectSelect.selectedIndex].text;

    if (!outputText || outputText.startsWith("Your culturally")) return;

    const originalHTML = saveBtn.innerHTML;
    saveBtn.innerHTML = '<span class="loader"></span>';

    try {
      const response = await fetch(saveUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
            .value,
        },
        body: JSON.stringify({
          input_text: inputText,
          output_text: outputText,
          target_culture: targetCulture,
        }),
      });
      if (response.ok) {
        saveSuccess.classList.remove("hidden");
        setTimeout(() => saveSuccess.classList.add("hidden"), 3000);
      }
    } catch (e) {
      console.error("Save translation error", e);
    } finally {
      saveBtn.innerHTML = originalHTML;
    }
  });
}

function setupSaveButton() {
  const saveBtn = document.getElementById("save-btn");
  const saveSuccess = document.getElementById("save-success");
  if (!saveBtn) return;

  const saveUrl = saveBtn.dataset.saveUrl;

  saveBtn.addEventListener("click", async () => {
    const dialectSelect = document.getElementById("dialect-select");
    if (!dialectSelect) {
      console.error("dialect-select element not found");
      return;
    }

    const inputText = document.querySelector('textarea[name="text"]').value;
    const outputText =
      document.getElementById("translation-output").textContent;
    const targetCulture =
      dialectSelect.options[dialectSelect.selectedIndex].text;

    if (!outputText || outputText.startsWith("Your culturally")) return;

    const originalHTML = saveBtn.innerHTML;
    saveBtn.innerHTML = '<span class="loader"></span>';

    try {
      const response = await fetch(saveUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
            .value,
        },
        body: JSON.stringify({
          input_text: inputText,
          output_text: outputText,
          target_culture: targetCulture,
        }),
      });

      const result = await response.json(); // Parse JSON response

      if (!response.ok) {
        // Handle error response
        const errorMessage = result.message || "Failed to save translation";
        alert(`Error: ${errorMessage}`);
        return;
      }

      // Handle success cases differently based on status
      if (result.status === "info") {
        saveSuccess.textContent = "Translation already saved!";
      } else {
        saveSuccess.textContent = "Translation saved successfully!";
      }

      saveSuccess.classList.remove("hidden");
      setTimeout(() => saveSuccess.classList.add("hidden"), 3000);
    } catch (e) {
      console.error("Save translation error", e);
      alert("Network error. Please try again.");
    } finally {
      saveBtn.innerHTML = originalHTML;
    }
  });
}

// 4. LANGUAGE GROUPS (optgroup show/hide)
function setupLanguageGroups() {
  const languageGroup = document.getElementById("language-group");
  const dialectSelect = document.getElementById("dialect-select");
  if (!languageGroup || !dialectSelect) return;

  languageGroup.addEventListener("change", () => {
    document
      .querySelectorAll("optgroup")
      .forEach((g) => g.classList.add("hidden"));
    const groupClass = `.${languageGroup.value}-group`;
    document.querySelector(groupClass)?.classList.remove("hidden");

    const firstOpt = document.querySelector(`${groupClass} option`);
    if (firstOpt) dialectSelect.value = firstOpt.value;
  });
}

function setupSmoothScroll() {
  const ctaButton = document.querySelector(".cta-pulse");
  if (!ctaButton) return;

  ctaButton.addEventListener("click", function (e) {
    if (this.getAttribute("href") !== "#translation-section") return;

    e.preventDefault();
    const target = document.getElementById("translation-section");
    if (!target) return;

    const headerOffset = 80;
    const elementPosition = target.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

    window.scrollTo({ top: offsetPosition, behavior: "smooth" });
  });
}

// Nav bar handler
function navBar() {
  const mobileMenuBtn = document.getElementById("mobile-menu-btn");
  const mobileMenu = document.getElementById("mobile-menu");

  if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener("click", function () {
      mobileMenu.classList.toggle("hidden");
      mobileMenu.classList.toggle("active");
      mobileMenuBtn.classList.toggle("active");
    });
  }

  // Close menu when clicking outside
  document.addEventListener("click", function (event) {
    if (
      !mobileMenu.contains(event.target) &&
      !mobileMenuBtn.contains(event.target) &&
      !mobileMenu.classList.contains("hidden")
    ) {
      mobileMenu.classList.add("hidden");
      mobileMenu.classList.remove("active");
      mobileMenuBtn.classList.remove("active");
    }
  });
}

// warn the user before unchecing the save_history
function warnUser() {
  const checkbox = document.getElementById("store_history_setting");

  if (checkbox) {
    checkbox.addEventListener("change", function () {
      if (!this.checked) {
        const confirmed = confirm(
          "Unchecking this option will delete all your saved translation history. Are you sure you want to proceed?"
        );

        if (!confirmed) {
          // Restore previous state after a slight delay
          setTimeout(() => {
            this.checked = true;
          }, 0);
        }
      }
    });
  }
}

// Only one getApproval function

function getApproval() {
  const saveBtn = document.getElementById("save-btn");
  const consentMessage = document.getElementById("save-consent-message");

  if (saveBtn && consentMessage) {
    // Get the close button from within the consent message
    const closeBtn = consentMessage.querySelector(".save-consent-close");

    saveBtn.addEventListener("click", function (e) {
      e.stopPropagation();

      const storeHistory = this.dataset.storeHistory === "true";
      if (!storeHistory) {
        consentMessage.classList.remove("hidden");
        consentMessage.classList.add("active");
      }
    });

    if (closeBtn) {
      closeBtn.addEventListener("click", async function (e) {
        e.preventDefault();
        e.stopPropagation();

        try {
          // Get CSRF token from cookie
          function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== "") {
              const cookies = document.cookie.split(";");
              for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + "=") {
                  cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                  );
                  break;
                }
              }
            }
            return cookieValue;
          }

          const csrfToken = getCookie("csrftoken");

          const response = await fetch(urls.enableHistoryStorage, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({}),
          });

          if (response.ok) {
            // Update the UI immediately
            saveBtn.dataset.storeHistory = "true";

            // Show success message
            const successMsg = document.createElement("div");
            successMsg.className =
              "fixed bottom-4 right-4 bg-green-500 text-white px-4 py-2 rounded-md shadow-lg";
            successMsg.textContent = "History storage enabled successfully!";
            document.body.appendChild(successMsg);

            // Remove after 3 seconds
            setTimeout(() => {
              successMsg.remove();
            }, 3000);

            // Close the consent message
            consentMessage.classList.remove("active");
            consentMessage.classList.add("hidden");
          } else {
            throw new Error(await response.text());
          }
        } catch (error) {
          console.error("Error:", error);
          // Show error message
          const errorMsg = document.createElement("div");
          errorMsg.className =
            "fixed bottom-4 right-4 bg-red-500 text-white px-4 py-2 rounded-md shadow-lg";
          errorMsg.textContent = "Failed to enable history storage";
          document.body.appendChild(errorMsg);

          setTimeout(() => {
            errorMsg.remove();
          }, 3000);
        }
      });
    }

    // Close message when clicking outside
    document.addEventListener("click", function (e) {
      if (
        !consentMessage.contains(e.target) &&
        e.target !== saveBtn &&
        consentMessage.classList.contains("active")
      ) {
        consentMessage.classList.remove("active");
        consentMessage.classList.add("hidden");
      }
    });
  }
}

// Feedback pop out
function showFeedbackPopup(inputText, outputText, dialect) {
  console.log("🔔 showFeedbackPopup called"); // <-- add this too
  const popup = document.getElementById("feedback-popup");
  if (!popup) {
    console.error("❌ No #feedback-popup container in DOM");
    return;
  }
  popup.classList.remove("hidden");
  // … reset stars/comments …

  // Reset UI
  popup.querySelectorAll(".rating-star").forEach((star) => {
    star.classList.remove("bg-blue-500", "text-white");
  });
  document.getElementById("feedback-comments").value = "";
}

function feedbackFunction() {
  const popup = document.getElementById("feedback-popup");
  if (!popup) return;

  function hideFeedbackPopup() {
    document.getElementById("feedback-popup").classList.add("hidden");
  }

  // Star rating interaction
  popup.querySelectorAll(".rating-star").forEach((star) => {
    star.addEventListener("click", function () {
      const rating = this.dataset.rating;

      // Update UI
      popup.querySelectorAll(".rating-star").forEach((s) => {
        if (parseInt(s.dataset.rating) <= parseInt(rating)) {
          s.classList.add("bg-blue-500", "text-white");
        } else {
          s.classList.remove("bg-blue-500", "text-white");
        }
      });
    });
  });

  // Close buttons
  document
    .getElementById("close-feedback-popup")
    .addEventListener("click", hideFeedbackPopup);
  document
    .getElementById("cancel-feedback")
    .addEventListener("click", hideFeedbackPopup);

  // Submit feedback from popup
  document
    .getElementById("submit-feedback-popup")
    .addEventListener("click", async function () {
      const popup = document.getElementById("feedback-popup");

      const selectedStars = document.querySelectorAll(
        ".rating-star.bg-blue-500"
      );
      const selectedRating = selectedStars.length
        ? selectedStars[selectedStars.length - 1].dataset.rating
        : null;

      if (!selectedRating) {
        alert("Please select a rating");
        return;
      }

      const comments = document.getElementById("feedback-comments").value;

      try {
        // grab it once
        const saveUrl =
          document.getElementById("feedback-popup").dataset.saveUrl;
        const response = await fetch(saveUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
              .value,
          },
          body: JSON.stringify({
            input_text: popup.dataset.inputText,
            output_text: popup.dataset.outputText,
            dialect: popup.dataset.dialect,
            rating: selectedRating,
            comments: comments,
          }),
        });

        if (response.ok) {
          hideFeedbackPopup();
          // Show thank you toast
          const toast = document.createElement("div");
          toast.className =
            "fixed top-4 right-4 bg-green-500 text-white px-4 py-2 rounded shadow-lg";
          toast.textContent = "Thank you for your feedback!";
          document.body.appendChild(toast);
          setTimeout(() => toast.remove(), 3000);
        } else {
          alert("Failed to submit feedback. Please try again.");
        }
      } catch (error) {
        console.error("Feedback submission error:", error);
        alert("Network error. Please try again.");
      }
    });

  // Show feedback popup occasionally after translation
  const optOutCheckbox = popup.querySelector("#dont-ask-again");
  if (optOutCheckbox) {
    optOutCheckbox.addEventListener("change", (e) => {
      // Persist their choice forever
      localStorage.setItem("feedbackOptOut", e.target.checked);
    });
  }
}

function shouldAskFeedback(isBad = false) {
  // 1) Opt-out check
  if (localStorage.getItem("feedbackOptOut") === "true") {
    console.log("🚫 opted out");
    return false;
  }

  // 2) Read current count
  let count = parseInt(sessionStorage.getItem("feedbackCount") || "0", 10);
  console.log(`🔢 Current feedbackCount: ${count}`);

  // 3) Cap at 3
  if (count >= 3) {
    console.log("⛔️ reached max per session");
    return false;
  }

  // 4) Exponential back-off
  const chances = [0.3, 0.2, 0.1];
  let chance = chances[count] ?? 0;

  // 5) Increase chance for low-confidence translations
  // if (isBad) {
  //   chance = Math.min(chance * 2, 1.0);
  //   console.log(`⚠️ Low confidence! Adjusted chance to: ${chance}`);
  // }

  const roll = Math.random();
  console.log(`🎲 Roll=${roll.toFixed(3)} < Chance=${chance}?`);

  // 6) Decide and conditionally increment
  if (roll < chance) {
    sessionStorage.setItem("feedbackCount", count + 1);
    console.log("👉 shouldAskFeedback returns true");
    return true;
  }

  console.log("👉 shouldAskFeedback returns false");
  return false;
}

// INITIALIZE EVERYTHING WHEN DOM LOADS
document.addEventListener("DOMContentLoaded", function () {
  setupCultureSelection();
  setupPasswordToggles();
  setupErrorHandling();
  setupMessageDismissal();
  setupDebugHelpers();
  setupTranslationForm(); //  translation functionality
  setupCopyButton();
  setupSaveButton();
  setupShareMenu();
  setupLanguageGroups();
  setupSmoothScroll();
  navBar();
  warnUser();
  getApproval();
  feedbackFunction();

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

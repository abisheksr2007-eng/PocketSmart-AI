const TOKEN_KEY = "pocketsmart_access_token";

function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

async function apiFetch(url, options = {}) {
  const headers = {
    ...(options.headers || {}),
  };

  const token = getToken();

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  if (options.body && !(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }

  const response = await fetch(url, {
    ...options,
    headers,
  });

  const contentType = response.headers.get("content-type") || "";

  let data;

  if (contentType.includes("application/json")) {
    data = await response.json();
  } else {
    data = await response.text();
  }

  if (!response.ok) {
    const message = data?.detail || data?.message || "Something went wrong.";

    throw new Error(message);
  }

  return data;
}

async function loginUser(email, password) {
  const data = await apiFetch("/api/login", {
    method: "POST",
    body: JSON.stringify({
      email,
      password,
    }),
  });

  setToken(data.access_token);

  return data;
}

async function registerUser(name, email, password) {
  const data = await apiFetch("/api/register", {
    method: "POST",
    body: JSON.stringify({
      name,
      email,
      password,
    }),
  });

  setToken(data.access_token);

  return data;
}

function logoutUser() {
  clearToken();
  window.location.href = "/";
}

function showError(element, message) {
  if (!element) {
    alert(message);
    return;
  }

  element.textContent = message;
  element.classList.remove("hidden");
}

function showLoading(element, visible = true) {
  if (!element) {
    return;
  }

  element.classList.toggle("show", visible);
}

function renderRecommendation(container, result) {
  if (!container) {
    return;
  }

  const items = result.items || [];

  const itemHtml = items
    .map(
      (item) => `
            <div class="item">
                <div class="item-header">
                    <div>
                        <h3>${escapeHtml(item.name)}</h3>
                        <div class="muted">
                            ${escapeHtml(item.category)}
                        </div>
                    </div>

                    <div class="price">
                        ₹${Number(item.price).toLocaleString("en-IN")}
                    </div>
                </div>

                <p>
                    ${escapeHtml(item.reason || "")}
                </p>

                ${
                  item.url
                    ? `
                            <a
                                class="button secondary"
                                href="${item.url}"
                                target="_blank"
                                rel="noopener"
                            >
                                View
                            </a>
                        `
                    : ""
                }
            </div>
        `,
    )
    .join("");

  const tips = (result.tips || [])
    .map((tip) => `<li>${escapeHtml(tip)}</li>`)
    .join("");

  container.innerHTML = `
        <div class="result-summary">
            <h2>${escapeHtml(result.title || "Recommendation")}</h2>

            <p>
                ${escapeHtml(result.summary || "")}
            </p>

            <strong>
                Estimated total:
                ₹${Number(result.estimated_total || 0).toLocaleString("en-IN")}
            </strong>
        </div>

        <div class="item-list">
            ${itemHtml}
        </div>

        ${
          tips
            ? `
                    <div class="card" style="margin-top:20px">
                        <h3>Smart Tips</h3>
                        <ul>${tips}</ul>
                    </div>
                `
            : ""
        }
    `;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

document.addEventListener("DOMContentLoaded", () => {
  const logoutButton = document.querySelector("[data-logout]");

  if (logoutButton) {
    logoutButton.addEventListener("click", logoutUser);
  }
});

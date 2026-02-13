/**
 * BillMaster Pro - Frontend Application
 * Connected to Python Flask Backend with SQL Database
 */

// ==========================================
// API BASE URL - Points to Python backend
// ==========================================
const API_BASE = window.location.origin + "/api";

// ==========================================
// API - Real HTTP calls to Flask backend
// ==========================================
const api = {
  async get(endpoint) {
    try {
      // Convert PHP-style endpoints to Flask API routes
      const url = this._buildUrl(endpoint);
      const response = await fetch(url, {
        method: "GET",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
      });
      return await response.json();
    } catch (error) {
      console.error("API GET Error:", error);
      return { success: false, message: "Network error" };
    }
  },

  async post(endpoint, data) {
    try {
      const url = this._buildUrl(endpoint);
      const response = await fetch(url, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      return await response.json();
    } catch (error) {
      console.error("API POST Error:", error);
      return { success: false, message: "Network error" };
    }
  },

  _buildUrl(endpoint) {
    // Convert "categories.php?action=list" → "/api/categories?action=list"
    const [file, queryStr] = endpoint.split("?");
    const apiName = file.replace(".php", "");
    return `${API_BASE}/${apiName}${queryStr ? "?" + queryStr : ""}`;
  },
};

// ==========================================
// TOAST NOTIFICATIONS
// ==========================================
const toast = {
  container: null,
  init() {
    if (!this.container) {
      this.container = document.createElement("div");
      this.container.className = "toast-container";
      document.body.appendChild(this.container);
    }
  },
  show(message, type = "info", duration = 3000) {
    this.init();
    const icons = { 
      success: "check-circle", 
      error: "alert-circle", 
      warning: "alert-triangle", 
      info: "info" 
    };
    const toastEl = document.createElement("div");
    toastEl.className = `toast toast-${type}`;
    toastEl.innerHTML = `
      <span class="toast-icon"><i data-lucide="${icons[type]}" class="icon-sm"></i></span>
      <span class="toast-message">${message}</span>
    `;
    this.container.appendChild(toastEl);
    if (window.lucide) {
      lucide.createIcons({
        attrs: {
          class: 'icon-sm'
        },
        nameAttr: 'data-lucide',
        icons: [icons[type]]
      });
      // Fallback for dynamic content logic
      lucide.createIcons();
    }
    setTimeout(() => {
      toastEl.style.opacity = "0";
      toastEl.style.transform = "translateX(100%)";
      setTimeout(() => toastEl.remove(), 300);
    }, duration);
  },
  success(msg) {
    this.show(msg, "success");
  },
  error(msg) {
    this.show(msg, "error");
  },
  warning(msg) {
    this.show(msg, "warning");
  },
  info(msg) {
    this.show(msg, "info");
  },
};

// ==========================================
// MODAL FUNCTIONS
// ==========================================
const modal = {
  open(id) {
    const el = document.getElementById(id);
    if (el) {
      el.classList.add("active");
      document.body.style.overflow = "hidden";
    }
  },
  close(id) {
    const el = document.getElementById(id);
    if (el) {
      el.classList.remove("active");
      document.body.style.overflow = "";
    }
  },
};

// ==========================================
// AUTHENTICATION
// ==========================================
const auth = {
  async check() {
    return api.get("auth.php?action=check");
  },
  async login(username, password) {
    return api.post("auth.php?action=login", { username, password });
  },
  async logout() {
    await api.get("auth.php?action=logout");
    window.location.replace("login.html");
  },
  async requireAuth() {
    const result = await this.check();
    if (!result || !result.success) {
      window.location.replace("login.html");
      return null;
    }
    return result.user;
  },
};

// ==========================================
// UTILITY FUNCTIONS
// ==========================================
const utils = {
  formatCurrency(amount, symbol = "₹") {
    const num = parseFloat(amount) || 0;
    return `${symbol}${num.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",")}`;
  },
  formatDate(dateString) {
    return new Date(dateString).toLocaleDateString("en-IN", {
      day: "2-digit",
      month: "short",
      year: "numeric",
    });
  },
  formatDateTime(dateString) {
    return new Date(dateString).toLocaleString("en-IN", {
      day: "2-digit",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  },
  escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  },
  debounce(func, wait) {
    let timeout;
    return function (...args) {
      clearTimeout(timeout);
      timeout = setTimeout(() => func.apply(this, args), wait);
    };
  },
  getInitials(name) {
    if (!name) return "?";
    return name
      .split(" ")
      .map((w) => w[0])
      .join("")
      .toUpperCase()
      .substring(0, 2);
  },
};

// ==========================================
// SIDEBAR TOGGLE
// ==========================================
function initSidebar() {
  const sidebar = document.querySelector(".sidebar");
  const toggle = document.querySelector(".sidebar-toggle");
  const overlay = document.querySelector(".mobile-overlay");

  if (toggle && sidebar) {
    toggle.addEventListener("click", () => {
      sidebar.classList.toggle("open");
      overlay?.classList.toggle("active");
    });
  }
  if (overlay) {
    overlay.addEventListener("click", () => {
      sidebar?.classList.remove("open");
      overlay.classList.remove("active");
    });
  }
  document.querySelectorAll(".nav-item").forEach((item) => {
    item.addEventListener("click", () => {
      if (window.innerWidth <= 1024) {
        sidebar?.classList.remove("open");
        overlay?.classList.remove("active");
      }
    });
  });
}

// ==========================================
// USER INFO INIT
// ==========================================
async function initUserInfo() {
  const result = await auth.check();
  if (result.success && result.user) {
    const user = result.user;
    const userName = document.querySelector(".user-name");
    const userRole = document.querySelector(".user-role");
    const userAvatar = document.querySelector(".user-avatar");

    if (userName) userName.textContent = user.full_name || "User";
    if (userRole) userRole.textContent = user.role || "staff";
    if (userAvatar) userAvatar.textContent = utils.getInitials(user.full_name);

    // Role-based UI restrictions
    const isAdmin = user.role === "admin";
    const currentPage = window.location.pathname.split("/").pop();

    // 1. Sidebar Restrictions
    document.querySelectorAll(".nav-item").forEach((item) => {
      const href = item.getAttribute("href");
      if (href === "dashboard.html" || href === "settings.html" || href === "expenses.html") {
        if (!isAdmin) {
          item.style.display = "none";
        }
      }
    });

    // 2. Page Access Restrictions
    const restrictedPages = ["dashboard.html", "settings.html", "expenses.html"];
    if (!isAdmin && restrictedPages.includes(currentPage)) {
      window.location.replace("billing.html"); // Redirect Staff to Billing page
    }

    // 3. User Management Restrictions (specific to settings.html if accessed by admin)
    if (currentPage === "settings.html") {
      const addUserBtn = document.querySelector('button[onclick="openUserModal()"]');
      const resetSection = document.querySelector(".glass-card[style*='border: 1px solid rgba(255, 0, 0, 0.2)']");
      if (!isAdmin) {
        if (addUserBtn) addUserBtn.style.display = "none";
        if (resetSection) resetSection.style.display = "none";
      }
    }

    // 4. Global Deletion Restriction for Staff
    if (!isAdmin) {
      // Hide all delete buttons (usually have 'Delete' title or trash icon)
      const hideDeletes = () => {
        document.querySelectorAll('button').forEach(btn => {
          const hasTrashIcon = btn.querySelector('[data-lucide="trash-2"]') || btn.innerHTML.includes('trash-2');
          const isDeleteBtn = (btn.title && btn.title.toLowerCase().includes('delete')) || 
                             (btn.innerText && btn.innerText.includes('Delete')) ||
                             hasTrashIcon;
          
          if (isDeleteBtn) {
            btn.style.display = 'none';
          }
        });
      };
      hideDeletes();
      // Also run after any AJAX renders (brief delay to catch most)
      setTimeout(hideDeletes, 500);
      setTimeout(hideDeletes, 1500);
    }
  }
}

// ==========================================
// GLOBAL EVENT LISTENERS
// ==========================================
document.addEventListener("click", (e) => {
  if (
    e.target.classList.contains("modal-overlay") &&
    e.target.classList.contains("active")
  ) {
    e.target.classList.remove("active");
    document.body.style.overflow = "";
  }
});

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    document
      .querySelectorAll(".modal-overlay.active")
      .forEach((m) => m.classList.remove("active"));
    document.body.style.overflow = "";
  }
});

// ==========================================
// INITIALIZE
// ==========================================
document.addEventListener("DOMContentLoaded", () => {
  initSidebar();

  // Add page entrance animation
  const mainContent = document.querySelector(".page-content");
  if (mainContent) {
    mainContent.classList.add("animate-fade");
    mainContent.style.animationDuration = "0.6s";
  }

  // One-time cleanup for fresh start on new full-stack version
  if (!localStorage.getItem("billmaster_v2_migrated")) {
    console.log("🧼 Performing fresh start cleanup...");
    // Keep only the migration flag, clear everything else
    localStorage.clear();
    localStorage.setItem("billmaster_v2_migrated", "true");
    // Only reload if we actually found old data to clear
    window.location.reload();
  }
});

// Export
window.BillMaster = { api, toast, modal, auth, utils };

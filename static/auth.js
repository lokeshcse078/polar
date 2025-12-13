// ==================== AUTHENTICATION FUNCTIONS ====================

// Use relative API URL for production (Railway)
const API_URL = ""; // Empty string ensures relative URLs work

// ------------------ Authentication ------------------

// Check if user is authenticated
function checkAuth() {
    const token = localStorage.getItem("auth_token");
    if (!token) {
        window.location.href = "/login-page"; // Redirect to login route
        return false;
    }
    return true;
}

// Get current user info
function getCurrentUser() {
    return {
        id: localStorage.getItem("user_id"),
        name: localStorage.getItem("user_name"),
        token: localStorage.getItem("auth_token"),
        role: localStorage.getItem("user_role")
    };
}

// Logout function
function logout() {
    if (confirm("Are you sure you want to logout?")) {
        localStorage.clear();
        window.location.href = "/login-page";
    }
}

// Update navbar with user info
function updateNavbar() {
    const user = getCurrentUser();
    const userInfoDiv = document.getElementById("user-info");
    if (user.token && userInfoDiv) {
        userInfoDiv.innerHTML = `
            <div class="user-info">
                <strong>${user.name}</strong>
                <small>User ID: ${user.id}</small>
            </div>
            <button class="btn-logout" onclick="logout()">Logout</button>
        `;
    }
}

// ------------------ API Calls ------------------

// Make authenticated API call
function fetchWithAuth(url, options = {}) {
    const token = localStorage.getItem("auth_token");

    if (!token) {
        window.location.href = "/login-page";
        return Promise.reject("No authentication token");
    }

    const headers = options.headers || {};
    headers["Authorization"] = `Bearer ${token}`;
    headers["Content-Type"] = "application/json";

    return fetch(API_URL + url, { ...options, headers });
}

// ------------------ Notifications ------------------

// Show notification message
function showNotification(message, type = "info", duration = 5000) {
    let notificationDiv = document.getElementById("notification");

    if (!notificationDiv) {
        const container = document.querySelector(".container") || document.body;
        const div = document.createElement("div");
        div.id = "notification";
        container.insertBefore(div, container.firstChild);
        notificationDiv = div;
    }

    notificationDiv.className = `alert alert-${type}`;
    notificationDiv.innerText = message;
    notificationDiv.style.display = "block";

    if (duration > 0) {
        setTimeout(() => {
            notificationDiv.style.display = "none";
        }, duration);
    }
}

// ------------------ Utilities ------------------

// Format date
function formatDate(dateString) {
    if (!dateString) return "-";
    const date = new Date(dateString);
    return date.toLocaleDateString("en-IN", {
        year: "numeric",
        month: "short",
        day: "numeric"
    });
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR"
    }).format(amount);
}

// ------------------ Page Initialization ------------------

document.addEventListener("DOMContentLoaded", function () {
    const path = window.location.pathname;

    // Skip auth check on login/register pages
    if (!path.includes("/login-page") && !path.includes("/register-page")) {
        if (checkAuth()) {
            updateNavbar();
        }
    }
});

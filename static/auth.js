async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/api/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    });

    const result = await response.json();

    if (result.success) {
        localStorage.setItem("user", JSON.stringify(result.user));
        window.location.href = "/dashboard";
    } else {
        document.getElementById("error").innerText = result.message;
    }
}

/* ==========================================
   AUTH MODULE — SERVICE MANAGEMENT SYSTEM
   ========================================== */

const API_URL = ""; // keep empty for same-origin (Flask)

/* ------------------------------------------
   AUTH CHECK
------------------------------------------ */
function checkAuth() {
    const token = localStorage.getItem("auth_token");

    if (!token) {
        window.location.href = "/";
        return false;
    }
    return true;
}

/* ------------------------------------------
   CURRENT USER
------------------------------------------ */
function getCurrentUser() {
    return {
        email: localStorage.getItem("user_email") || "Unknown"
    };
}

/* ------------------------------------------
   LOGOUT
------------------------------------------ */
function logout() {
    localStorage.removeItem("auth_token");
    localStorage.removeItem("user_email");
    window.location.href = "/";
}

/* ------------------------------------------
   FETCH WITH AUTH
------------------------------------------ */
function fetchWithAuth(url, options = {}) {
    const token = localStorage.getItem("auth_token");

    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {})
    };

    // token is logical (session-based), not JWT yet
    if (token) {
        headers["Authorization"] = "Bearer " + token;
    }

    return fetch(API_URL + url, {
        ...options,
        headers
    }).then(res => {
        if (res.status === 401) {
            logout();
            throw new Error("Unauthorized");
        }
        return res;
    });
}

/* ------------------------------------------
   OPTIONAL UI HELPERS
------------------------------------------ */
function setUserInfo(elementId) {
    const user = getCurrentUser();
    const el = document.getElementById(elementId);
    if (el) {
        el.innerText = user.email;
    }
}

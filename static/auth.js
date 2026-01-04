
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
    window.location.href = "/logout";
}

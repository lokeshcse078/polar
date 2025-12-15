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

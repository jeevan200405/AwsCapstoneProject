const loginBox = document.getElementById("loginBox");
const signupBox = document.getElementById("signupBox");
const errorMsg = document.getElementById("errorMsg");

// Show Signup form
function showSignup() {
    loginBox.style.display = "none";
    signupBox.style.display = "block";
    errorMsg.textContent = "";
}

//Show Login in form
function showLogin() {
    signupBox.style.display = "none";
    loginBox.style.display = "block";
    errorMsg.textContent = "";
}

// ADMIN SIGNUP FORM VALIDATION

const adminSignupForm = document.getElementById("adminSignupForm");

if (adminSignupForm) {

    adminSignupForm.addEventListener("submit", function (e) {

        const username = document.getElementById("signupUser").value.trim();
        const email = document.getElementById("signupEmail").value.trim();
        const password = document.getElementById("signupPass").value.trim();

        if (username === "" || email === "" || password === "") {
            e.preventDefault();
            errorMsg.textContent = "All fields are required!";
            return;
        }

        if (password.length < 5) {
            e.preventDefault();
            errorMsg.textContent = "Password must be at least 5 characters!";
            return;
        }

        // Allow Flask backend to handle signup
        console.log("Admin signup submitted to Flask backend");
    });

}

// ADMIN LOGIN FORM VALIDATION

const adminLoginForm = document.getElementById("adminLoginForm");

if (adminLoginForm) {

    adminLoginForm.addEventListener("submit", function (e) {

        const username = document.getElementById("loginUser").value.trim();
        const password = document.getElementById("loginPass").value.trim();

        if (username === "" || password === "") {
            e.preventDefault();
            errorMsg.textContent = "Username and password required!";
            return;
        }

        // Flask will verify using DynamoDB + IAM
        console.log("Admin login submitted to Flask backend");
    });

}

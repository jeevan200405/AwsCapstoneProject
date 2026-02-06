
// LOGIN FORM 

const loginForm = document.querySelector("form[action*='login']");

if (loginForm) {

    loginForm.addEventListener("submit", function (e) {

        const email = loginForm.querySelector("input[name='email']").value.trim();
        const password = loginForm.querySelector("input[name='password']").value.trim();

        if (email === "" || password === "") {

            e.preventDefault();

            alert("⚠ Please fill in all login fields!");
            return;
        }

        // Flask will handle authentication after this
        console.log("Login form submitted to Flask");

    });

}


//SIGNUP FORM

const signupForm = document.querySelector("#signupForm");

if (signupForm) {

    signupForm.addEventListener("submit", function (e) {

        const name = signupForm.querySelector("input[name='name']").value.trim();
        const email = signupForm.querySelector("input[name='email']").value.trim();
        const password = signupForm.querySelector("input[name='password']").value.trim();

        if (name === "" || email === "" || password === "") {

            e.preventDefault();

            alert("⚠ All signup fields are required!");
            return;
        }

        if (password.length < 4) {

            e.preventDefault();

            alert("⚠ Password must be at least 4 characters!");
            return;
        }

        // Flask will handle user creation after this
        console.log("Signup form submitted to Flask");

    });

}
// Auto focus input field

window.onload = () => {

    const emailField = document.querySelector("input[type='email']");

    if (emailField) {
        emailField.focus();
    }

};

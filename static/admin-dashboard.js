const movieTable = document.getElementById("movieTable");
const userTable = document.getElementById("userTable");

// Toggle sections

function showSection(section) {

    document.getElementById("moviesSection").classList.add("hidden");
    document.getElementById("usersSection").classList.add("hidden");

    if (section === "movies") {
        document.getElementById("moviesSection").classList.remove("hidden");
        loadMovies();
    }

    if (section === "users") {
        document.getElementById("usersSection").classList.remove("hidden");
        loadUsers();
    }
}

// ADD MOVIE

function addMovie() {

    const name = document.getElementById("movieName").value;
    const genre = document.getElementById("movie Discription").value;
    const time = document.getElementById("movieTime").value;

    if (!name || !genre || !time) {
        alert("Fill all fields");
        return;
    }

    fetch("/admin/add-movie", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name, genre, time })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        loadMovies();
    });

}

// LOAD MOVIES

function loadMovies() {

    fetch("/admin/get-movies")
    .then(res => res.json())
    .then(data => {

        movieTable.innerHTML = "";

        data.forEach(movie => {

            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${movie.name}</td>
                <td>${movie.Discription}</td>
                <td>${movie.time}</td>
                <td>
                <button class="delete-btn" onclick="deleteMovie('${movie.name}')">Delete</button>
                </td>
            `;

            movieTable.appendChild(row);
        });

    });

}

// DELETE MOVIE

function deleteMovie(name) {

    fetch("/admin/delete-movie", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        loadMovies();
    });

}

// LOAD USERS

function loadUsers() {

    fetch("/admin/get-users")
    .then(res => res.json())
    .then(data => {

        userTable.innerHTML = "";

        data.forEach(user => {

            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${user.name}</td>
                <td>${user.email}</td>
            `;

            userTable.appendChild(row);
        });

    });

}

// LOGOUT

function logout() {
    window.location.href = "/logout";
}

// Default load movies

loadMovies();

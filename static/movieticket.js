document.addEventListener("DOMContentLoaded", function () {

// Banner Slider

let slides = document.querySelectorAll(".slide");
let currentSlide = 0;

function showSlide(index) {
    slides.forEach(slide => slide.classList.remove("active"));
    if (slides.length > 0) {
        slides[index].classList.add("active");
    }
}

if (slides.length > 0) {
    setInterval(() => {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    }, 3000);
}

// Search Movies Feature

const searchInput = document.getElementById("search");
const movieCards = document.querySelectorAll(".movie-card");

if (searchInput) {
    searchInput.addEventListener("keyup", function () {

        let filter = searchInput.value.toLowerCase();

        movieCards.forEach(card => {

            let movieName = card.dataset.name.toLowerCase();

            card.style.display = movieName.includes(filter) ? "block" : "none";

        });
    });
}

// Booking Variables

let selectedMovieName = "";
let ticketPrice = 200;
let selectedSeats = 0;


// City Selection Control

const citySelect = document.getElementById("city");
const seatSection = document.getElementById("seatSection");

// Book Movie Button

window.bookMovie = function (movieName) {

    selectedMovieName = movieName;

    seatSection.style.display = "block";

    document.getElementById("selectedMovie").innerText =
        "Booking For : " + movieName;

    window.scrollTo({
        top: seatSection.offsetTop,
        behavior: "smooth"
    });

    clearSelection();
}
// Seat Booking System

const seats = document.querySelectorAll(".seat:not(.occupied)");
const seatCount = document.getElementById("seatCount");
const totalPrice = document.getElementById("totalPrice");

seats.forEach(seat => {

    seat.addEventListener("click", () => {

        const city = citySelect.value;

        if (city === "") {
            alert("Please select city first!");
            return;
        }

        if (!seat.classList.contains("occupied")) {
            seat.classList.toggle("selected");
            updateSummary();
        }

    });

});

//Update Summary

function updateSummary() {

    const selected = document.querySelectorAll(".seat.selected");

    selectedSeats = selected.length;

    seatCount.innerText = selectedSeats;
    totalPrice.innerText = selectedSeats * ticketPrice;
}
// Confirm Booking

window.confirmBooking = function () {

    const city = citySelect.value;

    if (city === "") {
        alert("Please select city first!");
        return;
    }

    if (selectedSeats === 0) {
        alert("Please select at least one seat!");
        return;
    }

    alert(
        "🎉 Booking Confirmed!\n\n" +
        "City: " + city +
        "\nMovie: " + selectedMovieName +
        "\nSeats: " + selectedSeats +
        "\nTotal Price: ₹" + (selectedSeats * ticketPrice)
    );

    document.querySelectorAll(".seat.selected").forEach(seat => {
        seat.classList.remove("selected");
        seat.classList.add("occupied");
    });

    clearSelection();
}
// Reset Booking Summary

function clearSelection() {

    document.querySelectorAll(".seat.selected").forEach(seat => {
        seat.classList.remove("selected");
    });

    selectedSeats = 0;
    seatCount.innerText = 0;
    totalPrice.innerText = 0;
}

});
function goToMovies() {
    document.getElementById("recommended").scrollIntoView({
        behavior: "smooth"
    });
}

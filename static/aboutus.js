
// ABOUT PAGE ANIMATED COUNTERS

document.addEventListener("DOMContentLoaded", () => {

    const counters = document.querySelectorAll(".counter");

    const speed = 200; // Animation speed

    counters.forEach(counter => {

        const updateCount = () => {

            const target = +counter.getAttribute("data-target");
            const current = +counter.innerText;

            const increment = Math.ceil(target / speed);

            if (current < target) {

                counter.innerText = current + increment;

                setTimeout(updateCount, 20);

            } else {

                counter.innerText = target;

            }
        };

        updateCount();

    });

});

// SIMPLE HEADER SHADOW EFFECT

window.addEventListener("scroll", () => {

    const header = document.querySelector("header");

    if (!header) return;

    if (window.scrollY > 50) {

        header.style.boxShadow = "0px 4px 10px rgba(0,0,0,0.3)";

    } else {

        header.style.boxShadow = "none";

    }

});

// IMAGE HOVER EFFECT

const aboutImage = document.querySelector(".about-image img");

if (aboutImage) {

    aboutImage.addEventListener("mouseover", () => {

        aboutImage.style.transform = "scale(1.05)";
        aboutImage.style.transition = "0.4s";

    });

    aboutImage.addEventListener("mouseout", () => {

        aboutImage.style.transform = "scale(1)";

    });

}

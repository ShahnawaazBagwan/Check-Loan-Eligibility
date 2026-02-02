// Typing animation
const text = "Check Loan Eligibility Using Machine Learning";
let i = 0;
const el = document.querySelector(".typing");

function typing() {
    if (el && i < text.length) {
        el.innerHTML += text.charAt(i);
        i++;
        setTimeout(typing, 70);
    }
}
typing();

// Show loader on submit
const form = document.getElementById("loanForm");
const loader = document.querySelector(".loader");

if (form) {
    form.addEventListener("submit", () => {
        loader.style.display = "block";
    });
}

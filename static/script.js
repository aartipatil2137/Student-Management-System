
document.addEventListener("DOMContentLoaded", () => {
    // Confirm before deleting a student.
    document.querySelectorAll("form[data-confirm]").forEach((form) => {
        form.addEventListener("submit", (event) => {
            const message = form.dataset.confirm;

            if (!window.confirm(message)) {
                event.preventDefault();
            }
        });
    });

    // Validate marks in the browser.
    const form = document.getElementById("student-form");

    if (form) {
        form.addEventListener("submit", (event) => {
            const marks = document.getElementById("marks");
            const error = document.getElementById("form-error");
            const value = Number(marks.value);

            if (
                marks.value === "" ||
                !Number.isFinite(value) ||
                value < 0 ||
                value > 100
            ) {
                event.preventDefault();
                error.textContent =
                    "Please enter marks from 0 to 100.";
                marks.focus();
            } else {
                error.textContent = "";
            }
        });
    }
});
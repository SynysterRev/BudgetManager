import {getCookie} from "./helpers.js";

function clearErrors() {
    const editFields = ["old_password", "new_password", "confirm_password"];
    editFields.forEach((fieldName) => {
        const errorDiv = document.getElementById(`error-${fieldName}`);
        if (errorDiv) {
            errorDiv.textContent = '';
        }
    });
}


document.addEventListener("DOMContentLoaded", (event) => {
    const changePasswordBtn = document.getElementById("change-password-btn");
    const passwordForm = document.getElementById("password-form");
    const cancelPasswordBtn = document.getElementById("password-cancel");

    if (changePasswordBtn && passwordForm) {
        changePasswordBtn.addEventListener("click", (event) => {
            passwordForm.classList.remove("hidden");
            changePasswordBtn.classList.add("hidden");
        });
    }
    if (cancelPasswordBtn) {
        cancelPasswordBtn.addEventListener("click", (event) => {
            passwordForm.classList.add("hidden");
            changePasswordBtn.classList.remove("hidden");
        });
    }

    passwordForm.addEventListener("submit", (event) => {
        event.preventDefault();

        const formData = new FormData(passwordForm);
        const csrfToken = getCookie("csrftoken");

        fetch(passwordForm.action, {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": csrfToken,
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    passwordForm.reset();
                    clearErrors();
                    const message = document.getElementById("success-message");
                    message.addEventListener("animationend", () => {
                        message.style.display = "none";
                    });
                    message.classList.add("animate-fade-out");
                    message.classList.remove("hidden");
                    message.innerText = data.successMessage;
                    changePasswordBtn.classList.remove("hidden");
                    passwordForm.classList.add("hidden");
                } else {
                    clearErrors();
                    for (const fieldName in data.errors) {
                        const errorDiv = document.getElementById(`error-${fieldName}`);
                        if (errorDiv) {
                            errorDiv.textContent = data.errors[fieldName].join(', ');
                        }
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});


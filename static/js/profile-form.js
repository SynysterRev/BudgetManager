import {getCookie} from "./helpers.js";

function enableInputs(enable) {
    const editFields = ["id_last_name", "id_first_name", "id_email"];
    editFields.forEach((fieldId) => {
        const field = document.getElementById(fieldId);

        if (field) {
            field.disabled = !enable;
        }
    });
}

function validateProfileForm(data) {
    const editBtn = document.getElementById("edit-profile");
    const divEditBtns = document.getElementById("edit-form-btns");

    enableInputs(false);
    clearErrors();

    document.getElementById("id_last_name").value = data.data.lastName;
    document.getElementById("id_first_name").value = data.data.firstName;
    document.getElementById("id_email").value = data.data.email;
    document.getElementById("full-name-nav").textContent = `${data.data.firstName} ${data.data.lastName}`;
    document.getElementById("first-name-circle").textContent = data.data.firstName[0].toUpperCase();
    document.getElementById("email-nav").textContent = data.data.email;

    divEditBtns.classList.add("hidden");
    editBtn.classList.remove("hidden");
}

function clearErrors() {
    const editFields = ["last_name", "first_name", "email"];
    editFields.forEach((fieldName) => {
        const errorDiv = document.getElementById(`error-${fieldName}`);
        if (errorDiv) {
            errorDiv.textContent = '';
        }
    });
}


document.addEventListener("DOMContentLoaded", (event) => {
    const editBtn = document.getElementById("edit-profile");
    const divEditBtns = document.getElementById("edit-form-btns");
    const cancelEditBtn = document.getElementById("edit-cancel");

    if (editBtn && divEditBtns) {
        editBtn.addEventListener("click", (event) => {
            divEditBtns.classList.remove("hidden");
            editBtn.classList.add("hidden");
            enableInputs(true);
        });
    }
    if (cancelEditBtn) {
        cancelEditBtn.addEventListener("click", (event) => {
            divEditBtns.classList.add("hidden");
            editBtn.classList.remove("hidden");
            enableInputs(false);
        });
    }
    const profileForm = document.getElementById("profile-form");
    profileForm.addEventListener("submit", (event) => {
        event.preventDefault();

        const formData = new FormData(profileForm);
        const csrfToken = getCookie("csrftoken");

        fetch(profileForm.action, {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": csrfToken,
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    validateProfileForm(data);
                    const message = document.getElementById("success-message");
                    message.addEventListener("animationend", () => {
                        message.classList.add("hidden");
                    });
                    message.classList.add("animate-fade-out");
                    message.classList.remove("hidden");
                    message.innerText = data.successMessage;
                } else {
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


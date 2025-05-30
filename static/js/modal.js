import {getCookie} from "./helpers.js";

export function initializeModalClose() {
    const modalClose = document.querySelector("#modal-close");
    if (modalClose) {
        modalClose.addEventListener('click', () => {
            document.querySelector("#create-modal").classList.add("hidden");
        });
    }
    const modalCancel = document.querySelector("#modal-cancel");
    if (modalCancel) {
        modalCancel.addEventListener('click', () => {
            document.querySelector("#create-modal").classList.add("hidden");
        });
    }
}

export function initializeTransactionForm() {
    const form = document.querySelector("#form-transaction");
    if (form) {
        form.addEventListener('submit', (event) => {
            event.preventDefault();

            const formData = new FormData(form);
            const csrfToken = getCookie("csrftoken");

            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    "X-CSRFToken": csrfToken,
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        form.reset();
                        window.location.reload()
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
    }
}
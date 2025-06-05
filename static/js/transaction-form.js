import {initializeModalClose, initializeTransactionForm} from "./modal.js";


document.addEventListener("DOMContentLoaded", (event) => {
    const addBtn = document.querySelector("#add-transaction-btn");
    const editBtns = document.querySelectorAll(".edit-transaction");
    const modal = document.querySelector("#create-modal");
    if (addBtn) {
        addBtn.addEventListener("click", (event) => {
            fetch("/expenses/create/")
                .then(response => response.text())
                .then(html => {
                        modal.innerHTML = html;
                        modal.classList.toggle("hidden");

                        initializeModalClose();
                        initializeTransactionForm();
                    }
                )
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    }
    editBtns.forEach(btn => {
        const transactionId = btn.dataset.transaction;
        btn.addEventListener("click", (event) => {
            fetch(`/expenses/${transactionId}/edit/`)
                .then(response => response.text())
                .then(html => {
                        modal.innerHTML = html;
                        modal.classList.toggle("hidden");

                        initializeModalClose();
                        initializeTransactionForm();
                    }
                )
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    });
    modal.addEventListener("click", (event) => {
        if (event.target === modal) {
            modal.classList.add("hidden");
        }
    });
    const filterFields = ["category_type", "start_date", "end_date", "transaction_type", "search"]

    filterFields.forEach((fieldId) => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener("change", (event) => {
                let params = new URLSearchParams(location.search);

                if (field.value) {
                    params.set(field.name, field.value);
                } else {
                    params.delete(field.name);
                }
                window.location.search = params.toString();
            });
        }
    });
});
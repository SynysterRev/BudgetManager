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
                        // initializeTransactionForm();
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
                        // initializeTransactionForm();
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
});
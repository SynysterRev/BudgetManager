import {initializeColorPicker} from "./color-picker.js";
import {initializeModalClose} from "./creation-modal.js";

document.addEventListener("DOMContentLoaded", (event) => {
    const addBtn = document.querySelector("#add-category-btn");
    const editBtns = document.querySelectorAll(".edit-category");
    const modal = document.querySelector("#create-modal");
    if (addBtn) {
        addBtn.addEventListener("click", (event) => {
            fetch("/categories/create/")
                .then(response => response.text())
                .then(html => {
                        modal.innerHTML = html;
                        modal.classList.toggle("hidden");

                        initializeColorPicker();
                        initializeModalClose();
                    }
                )
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    }
    editBtns.forEach(btn => {
        const categoryName = btn.dataset.category;
        const categoryColor = btn.dataset.color;
        btn.addEventListener("click", (event) => {
            fetch(`/categories/${categoryName}/edit/`)
                .then(response => response.text())
                .then(html => {
                        modal.innerHTML = html;
                        modal.classList.toggle("hidden");

                        initializeColorPicker(categoryColor);
                        initializeModalClose();
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
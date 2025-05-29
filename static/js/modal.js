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
class Modal {
    static open(modalId, actionUrl, title = 'Delete Item', message = 'This action cannot be undone.', buttonText = 'Delete') {
        const modal = document.getElementById(modalId);
        const form = modal.querySelector('form');
        const titleElement = modal.querySelector('#modal-title');
        const messageElement = modal.querySelector('#modal-message');
        const buttonElement = modal.querySelector('#modal-button');

        form.action = actionUrl;
        titleElement.textContent = title;
        messageElement.textContent = message;
        buttonElement.textContent = buttonText;

        modal.classList.remove('hidden');
    }

    static close(modalId) {
        document.getElementById(modalId).classList.add('hidden');
    }
}

function openDeleteModal(actionUrl, title, message, buttonText) {
    Modal.open('deleteModal', actionUrl, title, message, buttonText);
}

function closeDeleteModal() {
    Modal.close('deleteModal');
}
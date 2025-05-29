export function initializeColorPicker() {
    const colors = document.querySelectorAll(".color-option");
    const colorInput = document.querySelector("#id_color");
    colors[0].classList.add('ring-offset-2', 'ring-2', 'ring-gray-400', 'scale-110');
    colorInput.value = colors[0].dataset.color;
    colors.forEach(color => {
        color.addEventListener("click", (event) => {
            colors.forEach(opt => opt.classList.remove('ring-offset-2',
                'ring-2', 'ring-gray-400', 'scale-110'));
            color.classList.add('ring-offset-2', 'ring-2', 'ring-gray-400', 'scale-110');
            colorInput.value = color.dataset.color;
        });
    });
}
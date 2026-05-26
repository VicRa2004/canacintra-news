document.addEventListener('DOMContentLoaded', function() {
    // Delegación de eventos para manejar cambios en todos los inputs de archivo,
    // incluyendo aquellos agregados dinámicamente en formularios inline.
    document.addEventListener('change', function(e) {
        if (e.target && e.target.type === 'file') {
            const fileInput = e.target;
            
            // Encontrar el contenedor principal flex de Unfold
            const container = fileInput.closest('.border.flex');
            if (container) {
                // Encontrar el input de texto que simula mostrar el archivo seleccionado
                const textInput = container.querySelector('input[type="text"]');
                if (textInput && fileInput.files && fileInput.files.length > 0) {
                    const fileName = fileInput.files[0].name;
                    textInput.value = fileName;
                    
                    // Mejorar aspecto visual indicando que se ha seleccionado un archivo
                    textInput.classList.remove('text-gray-300', 'text-gray-500');
                    textInput.classList.add('text-primary-600', 'font-semibold', 'dark:text-primary-400');
                    
                    // Opcionalmente resaltar el borde del contenedor para dar feedback táctil
                    container.classList.remove('dark:border-gray-700');
                    container.classList.add('border-primary-500', 'ring-2', 'ring-primary-500/20');
                }
            }
        }
    });
});

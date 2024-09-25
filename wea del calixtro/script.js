// Star rating logic
console.log("hola");

const stars = document.querySelectorAll('.star');
const selectedRating = document.getElementById('selected-rating');
let currentRating = 0;

// Agregar el evento 'click' a cada estrella
stars.forEach((star, index) => {
    star.addEventListener('click', () => {
        currentRating = index + 1;
        updateStars();
        selectedRating.textContent = `Calificación: ${currentRating} estrellas`;
    });
});

// Función para actualizar las estrellas seleccionadas
function updateStars() {
    stars.forEach((star, index) => {
        if (index < currentRating) {
            star.classList.add('selected');  // Añadimos la clase 'selected' para las estrellas seleccionadas
        } else {
            star.style.color = 'transparent';  // Hacemos que las no seleccionadas desaparezcan visualmente
        }
    });
}

// Comment section logic
const commentForm = document.getElementById('comment-form');
const commentInput = document.getElementById('comment');
const usernameInput = document.getElementById('username');  // Añadimos la referencia al campo del nombre de usuario
const commentsList = document.getElementById('comments-list');

// Manejar el envío del formulario de comentarios
commentForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const commentText = commentInput.value.trim();
    const username = usernameInput.value.trim();  // Obtener el nombre de usuario

    if (commentText !== '' && username !== '') {
        const commentDiv = document.createElement('div');
        commentDiv.classList.add('comment');

        // Crear un enlace al perfil del usuario
        const userLink = document.createElement('a');
        userLink.href = 'perfil.html';  // Aquí puedes cambiar la URL al perfil del usuario
        userLink.textContent = username;
        userLink.classList.add('username-link');

        // Añadir el comentario y el enlace al perfil
        commentDiv.innerHTML = `<strong>${userLink.outerHTML}:</strong> ${commentText}`;
        commentsList.appendChild(commentDiv);

        // Limpiar los campos de comentario y nombre de usuario después de enviar
        commentInput.value = '';
        usernameInput.value = '';
    }
});

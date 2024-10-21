const mostrar    = document.getElementById('mostrar_foto');
const subir      = document.getElementById('subir_foto');
const btnCambiar = document.getElementById('cambiar_div');

btnCambiar.addEventListener('click', function() {
    mostrar.style.display = 'none';
    subir.style.display   = 'block';
});
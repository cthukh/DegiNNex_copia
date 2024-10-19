const divSubirFoto   = document.getElementById('subir_foto');
const divMostrarFoto = document.getElementById('mostar_foto');
const btnCambiar     = document.getElementById('cambiar_div');

btnCambiar.addEventListener("click", function() {
    divSubirFoto.style.display   = "block"; //activo
    divMostrarFoto.style.display = "none";
});
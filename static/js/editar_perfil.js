function showUpload() {
    document.getElementById('profile-picture-container').style.display = 'none';
    document.getElementById('upload-picture-container').style.display = 'block';
}

function showProfile() {
    document.getElementById('profile-picture-container').style.display = 'block';
    document.getElementById('upload-picture-container').style.display = 'none';
}

// Asegúrate de que el contenedor de carga esté oculto al principio
document.addEventListener("DOMContentLoaded", function() {
    if (document.getElementById('upload-picture-container').style.display === '') {
        document.getElementById('upload-picture-container').style.display = 'none';
    }
}); 
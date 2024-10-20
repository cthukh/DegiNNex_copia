const post     = document.getElementById('div-post');
const persona  = document.getElementById('div-personas');
const navBtnPo = document.getElementById('publicaciones-tab2');
const navBtnpe = document.getElementById('personas-tab1');

navBtnpe.addEventListener('click', function() {
    post.style.display = 'none';
    persona.style.display = 'flex';
});

navBtnPo.addEventListener('click', function() {
    post.style.display = 'flex';
    persona.style.display = 'none';
});


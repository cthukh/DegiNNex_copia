const reg = document.getElementById('registrarse');
const log = document.getElementById('ingresar');
const log_btn = document.getElementById('btn_login')
const reg_btn = document.getElementById('btn_reg')


log_btn.addEventListener('click', function() {
    reg.style.display = "none";
    log.style.display = "Block";
});

reg_btn.addEventListener('click', function() {
    reg.style.display = "block";
    log.style.display = "none";
});

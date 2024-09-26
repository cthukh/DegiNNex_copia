from flask import Flask, render_template, flash, redirect
from sqlalchemy import select
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

# Se crea una instancia de Flask y se configura con una clave secreta y la URI de la base de datos.
app = Flask(__name__)
app.config["SECRET_KEY"] = '9s12eue3b8rh38edj3xn832u8xn'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://root@localhost:3306/deginnex'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

# Se inicializa el gestor de sesiones y se define la vista de inicio de sesión.
login_manager = LoginManager(app)
login_manager.login_view = "auth"

# importación de módulos propios
from forms import FormularioRegistro, FormularioAcceso
from models import Usuario
from controllers import ControladorUsuarios

# Inicialización de versiones de la bases de datos
Migrate(app,db)

# Inicialización de login_manager y configuración de
# función que carga un usuario a partir de su ID, necesaria para la gestión de sesiones.
@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_por_id(int(user_id))

# Evita que las respuestas sean almacenadas en caché.
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Verifica si el usuario ya está autenticado. Si lo está, redirige a la página de inicio.
# Si no, muestra los formularios de registro y acceso.
@app.route("/")
def auth(form_registro=None, form_acceso=None):
    if current_user.is_authenticated:
        return redirect("/inicio")

    if form_registro == None:
        form_registro = FormularioRegistro()

    if form_acceso == None:
        form_acceso = FormularioAcceso()
    return render_template("auth.html", form_registro=form_registro, form_acceso=form_acceso)

# Maneja la creación de nuevos usuarios,  recibe un formulario y guarda en la base de datos.
# Valida los datos del formulario y proporciona mensajes de error si es necesario.
@app.route("/register", methods=["POST"])
def register():
    form   = FormularioRegistro()
    error  = None

    # Validación del formulario.
    # Comprobar si el correo ya está registrado; Si no, se crea el usuario.
    if form.validate_on_submit():
        print("form valido")
        flash("Form valido")
        nombre = form.nombre.data
        correo = form.correo.data
        clave  = form.clave.data
        
        # Consultamos si existe en la db.
        usuario = Usuario().obtener_por_correo(correo)
        if usuario is not None:
            error = f"El correo {correo} ya se encuentra registrado"
            print(error)
            flash(error)
            return(redirect("/"))
        else:
            flash(f'Registro solicitado para el usuario { nombre }')
            # Utilización de un controlador entre Vista y Modelo.
            ControladorUsuarios().crear_usuario(nombre, correo, clave)
            # Generamos una instancia de datos.
            return redirect("/")
    else:
        print("form invalido")
        flash("Form invalido")
        return auth(form_registro=form)

# Validar el acceso del usuario.
# Si es exitoso, iniciar sesión.
@app.route("/login", methods=["POST"])
def login():
    # Recibimos los datos del login en frontend.
    form_acceso = FormularioAcceso()
    if form_acceso.validate_on_submit():
        flash(f"Acceso solicitado para el usuario { form_acceso.correo.data }")
        # Consultamos por el correo en la db
        usuario = Usuario().obtener_por_correo(form_acceso.correo.data)
        # Si el usuario no es nada (entonces existe en la db)
        if usuario is not None:
            if usuario.chequeo_clave(form_acceso.clave.data):
                login_user(usuario)
                return(redirect("/inicio"))
            else:
                flash(f"Clave incorrecta")
                print(f"Clave incorrecta")
                return(redirect("/"))
        else:
            flash(f"El usuario no esta registrado")
            print(f"El usuario no esta registrado")
            return(redirect("/"))

# Página Principal
@app.route('/inicio')
def index():
    return render_template('index.html')

# seleccion de categorias
@app.route('/u_cat/<string:categoria>')
def selecionar_categorias(categoria):
    # Renderiza diferentes plantillas según la categoría
    if   categoria == 'videos':                         # Categoría video.
        return render_template ('cat_videos.html')
    elif categoria == 'imagenes':                       # Categoría imagenes.
        return render_template ('cat_imagenes.html')
    elif categoria == 'audio':                          # Categoría audio.  #? Posible retiro.
        return render_template ('cat_audio.html')
    elif categoria == 'sitios_web':                     # Categoría sitios web.
        return render_template ('cat_web.html')


# Muestra el perfil del usuario autenticado.
@app.route("/perfil")
@login_required
def perfil():
    # Muestra solo la sesión activa.
    return render_template("perfil.html", usuario=current_user)

# Cierra la sesión del usuario actual. (No se borra de la db)
@app.route("/logout")
def logout():
    logout_user()
    flash(f"El usuario ha cerrado sesión")
    print(f"El usuario ha cerrado sesión")
    return(redirect("/"))




@app.route("/userop")
def opciones_usuario():
    return redirect ("/home")


#TODO ruta de prueba
@app.route('/prueba')
def prueba():
    return render_template('') # Nombre de su plantilla de prueba en templates

# Manejo de errores.
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404         # Página no encontrada
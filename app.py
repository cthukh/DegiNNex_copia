from flask import Flask, render_template, flash, redirect, request, url_for
from sqlalchemy import select
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
import os

# Se crea una instancia de Flask y se configura con una clave secreta y la URI de la base de datos.
app = Flask(__name__)
app.config["SECRET_KEY"] = 'Ultra_Super_Secret_key'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://root@localhost:3306/digilapp_db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
op_form =[
        ('default',           'Sin área'),
        ('Editor de videos',  'Editor de videos'),
        ('Artista Digital',   'Artista Digital'),
        ('Productor músical', 'Productor músical'),
        ('Programador',       'Programador')
        ]

#!  erro en cambiar categoria, muestra la edad
#!  cuando se borra un proveedor su misma id no deberia perderse

db = SQLAlchemy(app)

# Se inicializa el gestor de sesiones y se define la vista de inicio de sesión.
login_manager = LoginManager(app)
login_manager.login_view = "auth"

# importación de módulos propios
from forms import FormularioRegistro, FormularioAcceso, FormularioValidar
from models import Usuario, Proveedor, Publicacion
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
#************************************************** Manejo registro/login **************************************************

# Verifica si el usuario ya está autenticado. Si lo está, redirige a la página de inicio.
# Si no, muestra los formularios de registro y acceso.
@app.route("/")
def auth(form_registro=None, form_acceso=None):
    if current_user.is_authenticated:
        return redirect("/inicio")

    if form_registro == None:
        form_registro = FormularioRegistro()
        
    elif form_registro:
        return redirect("/inicio")

    if form_acceso == None:
        form_acceso = FormularioAcceso()
    return render_template("auth.html", form_registro=form_registro, form_acceso=form_acceso)

# Maneja la creación de nuevos usuarios, recibe un formulario y guarda en la base de datos.
# Valida los datos del formulario y proporciona mensajes de error si es necesario.
@app.route("/register", methods=["POST"])
def register():
    form   = FormularioRegistro()
    error  = None

    #################### VALIDACIÓN DEL FORMULARIO. ####################
    # Comprobar si el correo ya está registrado; Si no, se crea el usuario.
    if form.validate_on_submit():
        print("form valido")
        flash("Form valido")
        nombre   = form.nombre.data
        apellido = form.apellido.data
        correo   = form.correo.data
        clave    = form.clave.data

        # Consultamos si existe en la db.
        usuario = Usuario().obtener_por_correo(correo)
        if usuario is not None:
            error = f"El correo {correo} ya se encuentra registrado"
            print(error)
            flash(error)
            return(redirect("/"))
        else:
            print(f'Registro solicitado para el usuario { nombre }')
            # Utilización de un controlador entre Vista y Modelo.
            ControladorUsuarios().crear_usuario(nombre, apellido, correo, clave)
            # Generamos una instancia de datos.
            return redirect("/inicio")
    else:
        print("form invalido")
        flash("Form invalido")
        return auth(form_registro=form)

#################### VALIDAR EL ACCESO AL USUARIO. ####################
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

#************************************************** Rutas principales. **************************************************

#################### Página Principal ####################
@app.route('/inicio')
def home():
    user = current_user
    return render_template('index.html', user=user)

#################### Selección de categorias ####################
# Categorias hasta ahora: videos, diseño grafico, audio, sitios web
@app.route('/seccion/<string:cat>')
def manejo_categorias(cat):
    proveedores = Proveedor.obtener_por_categoria(cat)
    publicaciones = Publicacion.obtener_por_categoria(cat)
    return render_template('unique_cat.html', proveedores=proveedores, publicaciones=publicaciones, cat=cat)

####################  VER PERFIL SELECCIONADO.  ####################
@app.route('/perfil/view/<int:id>')
def view_perfil(id):
    proveedor = Proveedor.buscar_por_id(id)
    return render_template ('perfil.html', proveedor = proveedor)

@app.route('/seccion/<string:cat>/crear-publicacion')
def crear_tarea(cat):
    return render_template('subir_post.html', cat=cat)

@app.route('/about')
def about():
    return render_template('about.html')

#************************************************** RUTAS DE PERFIL. **************************************************

####################  VER PERFIL PROPIO.  ####################
@app.route("/perfil/me")
@login_required
def perfil():
    # Muestra solo la sesión activa.
    return render_template("perfil_v2.html", usuario=current_user)

####################  EDITAR TU PERFIL.  ####################
@app.route('/perfil/me/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    if request.method == 'GET':
        proveedor = current_user.proveedor
        return render_template('editar_usuario.html', usuario=current_user, proveedor=proveedor,)

    if request.method == 'POST':
        error = False
        idq      = current_user.id
        nombre   = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo   = request.form.get('correo')
        bio      = request.form.get('bio')
        file = request.files['photo']
        
        if not file:                            #! ############ sacar de pc ico ##########
            return flash('No selected file')
        
        if file:
            filename  = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            print(file_path)
            ControladorUsuarios.op_fotos(idq,file_path)

        print("esta editando el usuario")
        resultado = ControladorUsuarios.editar_usuario(idq,nombre,apellido,correo,bio)

        if current_user.is_a_proveer == True:
            edad        = request.form.get('edad')
            telefono    = request.form.get('telefono')
            categoria   = request.form.get('categoria')
            print("es miembro y esta editando")
            resultadov2 = ControladorUsuarios.editar_miembro(idq,edad,telefono,categoria)

        if 'error' in resultado:
            # si hay error en resultado, devuelve un diccionario con el error.
            flash (resultado['mensaje'])
            print (resultado['mensaje'])
        else:
            flash("Perfil actualizado con éxito")
            print("Perfil actualizado con éxito")

        return redirect('/perfil/me')  # Redirige a la ruta de acción, si se usa POST

####################  CONVERTIRSE EN PROVEEDOR.  ####################
@app.route('/perfil/me/verificar')
@login_required
def crear_miembro():
    form_validar = FormularioValidar()
    return render_template('validar_proveedor.html', form_validar=form_validar)


#************************************************** ACCIONES**************************************************
####################  CREAR LA TABLA PROVEEDORES.  ####################
@app.route('/validar', methods=["POST", "GET"])
@login_required
def validar_perfil():
    form_validar = FormularioValidar()
    id           = current_user.id
    edad         = request.form.get('edad')
    telefono     = request.form.get('telefono')
    categoria    = request.form.get('categoria')
    
    if form_validar.validate_on_submit():
        ControladorUsuarios.crear_miembro(id, edad, telefono, categoria)
        return redirect('/perfil/me')

@app.route('/crear_post/<string:cat>', methods=['POST'])
@login_required
def crear_publicacion(cat):
    usuario_id   = current_user.id
    proveedor_id = current_user.proveedor.id
    texto        = request.form['texto']
    tags         = request.form['tags']
    categoria    = cat
    
    ControladorUsuarios.crear_publicacion(usuario_id, proveedor_id, texto,tags, categoria)
    return redirect(f'/seccion/{categoria}')


####################  CERRAR SESIÓN.  ####################
# (No se borra de la db)
@app.route("/cuenta/logout")
def logout():
    logout_user()
    flash(f"El usuario ha cerrado sesión")
    print(f"El usuario ha cerrado sesión")
    return(redirect("/"))

####################  ELIMINAR CUENTA.  ####################
@app.route('/cuenta/eliminar')
@login_required
def eliminar():
    user_id     = current_user.id
    ControladorUsuarios.borrar_usuario(user_id)
    flash ("usuario eliminado")
    return redirect('/')

####################  ELIMINAR VERIFICACIÓN  ####################
@app.route('/prof/eliminar')
@login_required
def eliminar_profesion():
    idu = current_user.id
    ControladorUsuarios.despedir(idu)
    return redirect('/perfil/me')


#TODO ************************************************** Rutas de prueba **************************************************
@app.route('/prueba')
def prueba():
    return render_template('')

#! ************************************************** Manejo de errores **************************************************

#################### PAGÍNA NO ENCONTRADA. ####################
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
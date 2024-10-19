from models import Usuario, db, Proveedor
from werkzeug.security import generate_password_hash, check_password_hash
import os

class ControladorUsuarios:
    
########################################  CREAR  ########################################
    @staticmethod
    def crear_usuario(nombre,apellido,correo,clave):
        usuario          = Usuario()
        usuario.nombre   = nombre
        usuario.apellido = apellido
        usuario.correo   = correo
        usuario.establecer_clave(clave)

        db.session.add(usuario)
        db.session.commit()
        return usuario
    
    @staticmethod
    def crear_miembro(idu, edad, telefono, categoria):
        proveedor = Proveedor()
        usuario = Usuario.query.get(idu)
        proveedor.edad        = edad
        proveedor.telefono    = telefono
        proveedor.categoria   = categoria
        usuario.is_a_proveer  = True
        proveedor.usuario_id  = idu

        db.session.add(proveedor)
        db.session.commit()
        return proveedor

########################################  EDITAR  ########################################
    @staticmethod
    def editar_usuario(id,nombre,apellido,correo,bio):
        # verifica el usuario por la id en db.
        usuario = Usuario.query.get(id)

        if not usuario:
            resultado = {
                'error' : True,
                'mensaje' : f"El usuario {id} no existe en la db"
            }
            return resultado

        # Verifica si el correo existe en la db
        if Usuario.query.filter_by(correo=correo).first() and correo != usuario.correo:
            resultado = {
                'error' : True,
                'mensaje' : f"El correo {correo} ya esta en uso"
            }
            return resultado
    
        usuario.nombre      = nombre
        usuario.apellido    = apellido
        usuario.correo      = correo
        usuario.biografia   = bio
    
        db.session.commit()
        return {'usuario' : usuario} # Retorna el usuario dentro de un diccionario

    @staticmethod
    def op_fotos(id,file_path):
        usuario = Usuario.query.get(id)
        usuario.foto_perfil = f'uploads/{os.path.basename(file_path)}'

        db.session.commit()
        return {'usuario' : usuario}

    @staticmethod
    def editar_miembro(id,edad,telefono,categoria):
        proveedor = Proveedor.query.filter_by(usuario_id = id).first()
        print(proveedor)
        proveedor.edad       = edad
        proveedor.telefono   = telefono
        proveedor.categoria  = categoria
        
        db.session.commit()
        return {'usuario' : proveedor}

########################################  BORRAR  ########################################
    @staticmethod
    # borra el usuario de la db
    def borrar_usuario(id):
        usuario = Usuario.query.get(id)
        emp = Proveedor.query.filter_by(usuario_id = id).first()
        if not usuario:
            resultado = {
                'error' : True,
                'mensaje' : f"El usuario {id} no existe en la db"
            }
            return resultado
        print(usuario)
        if usuario:
            db.session.delete(usuario)
            if emp:
                db.session.delete(emp)
            db.session.commit()
            return {'mensaje' : "usuario eliminado"}

    @staticmethod
    # Elimina la cuenta profesional
    def despedir(id):
        emp = Proveedor.query.filter_by(usuario_id = id).first()
        print(f"el usuario xd{emp}" )
        if not emp:
            resultado = {
                'error' : True,
                'mensaje' : f"El usuario {id} no existe en la db"
            }
            return resultado

        if emp:
            emp.usuario.is_a_proveer = False
            db.session.delete(emp)
            db.session.commit()
            return{'mensaje' : "se elimino la cuenta profesional"}
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.core.database.producto import Producto
from app.schemas.producto_modelo import ProductoCreate
from fastapi import HTTPException, UploadFile
import logging
import pandas as pd
import io

def get_productos(db: Session, skip: int = 0, limit: int = 100):
    try:
        productos = db.query(Producto).offset(skip).limit(limit).all()
        # Si no hay productos, devolver lista vacía en lugar de error
        if not productos:
            return []
        return productos
    except Exception as e:
        logging.error(f"Error al obtener productos: {e}")
        # En caso de error de base de datos, devolver lista vacía
        return []

def get_producto_by_codigo(db: Session, codigo_interno: str):
    return db.query(Producto).filter(Producto.CODIGO_INTERNO == codigo_interno).first()

def create_producto(db: Session, producto: ProductoCreate):
    try:
        # Verificar que el tipo de producto existe
        from .tipo_producto import get_tipo_producto_by_id
        tipo_producto = get_tipo_producto_by_id(db, producto.IDTIPOPRODUCTO)
        if not tipo_producto:
            raise HTTPException(status_code=400, detail="El tipo de producto no existe")

        # Validar campos únicos solo para equipo de cómputo
        if tipo_producto.NOMBRE_TIPO_PRODUCTO == "equipo de cómputo":
            # Verificar si ya existe un producto con la misma placa SENA
            placa_sena = producto.PLACA_SENA
            if placa_sena:
                existing_placa = db.query(Producto).filter(Producto.PLACA_SENA == placa_sena).first()
                if existing_placa:
                    raise HTTPException(status_code=400, detail="La placa SENA ya existe")
            
            # Verificar si ya existe un producto con el mismo serial
            serial = producto.SERIAL
            if serial:
                existing_serial = db.query(Producto).filter(Producto.SERIAL == serial).first()
                if existing_serial:
                    raise HTTPException(status_code=400, detail="El serial ya existe")

        # Verificar si ya existe un producto con el mismo código interno
        codigo_interno = producto.CODIGO_INTERNO
        existing_codigo = db.query(Producto).filter(Producto.CODIGO_INTERNO == codigo_interno).first()
        if existing_codigo:
            raise HTTPException(status_code=400, detail="El código interno ya existe")

        db_producto = Producto(
            CODIGO_INTERNO=producto.CODIGO_INTERNO,
            NOMBRE=producto.NOMBRE,
            IDTIPOPRODUCTO=producto.IDTIPOPRODUCTO,
            PLACA_SENA=producto.PLACA_SENA,
            SERIAL=producto.SERIAL,
            MARCA=producto.MARCA,
            ESTADO=producto.ESTADO,
            OBSERVACIONES=producto.OBSERVACIONES
        )
        db.add(db_producto)
        db.commit()
        db.refresh(db_producto)
        return db_producto
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error al crear el producto")

def update_producto(db: Session, codigo_interno: str, producto_data: dict):
    db_producto = get_producto_by_codigo(db, codigo_interno)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Verificar que el tipo de producto existe si se está actualizando
    tipo_producto = None
    if 'IDTIPOPRODUCTO' in producto_data:
        from .tipo_producto import get_tipo_producto_by_id
        tipo_producto = get_tipo_producto_by_id(db, producto_data['IDTIPOPRODUCTO'])
        if not tipo_producto:
            raise HTTPException(status_code=400, detail="El tipo de producto no existe")
    else:
        # Obtener el tipo actual del producto
        from .tipo_producto import get_tipo_producto_by_id
        tipo_producto = get_tipo_producto_by_id(db, db_producto.IDTIPOPRODUCTO)
    
    # Validar campos únicos solo para equipo de cómputo
    if tipo_producto and tipo_producto.NOMBRE_TIPO_PRODUCTO == "equipo de cómputo":
        # Verificar placa SENA si se está actualizando
        if 'PLACA_SENA' in producto_data and producto_data['PLACA_SENA']:
            existing_placa = db.query(Producto).filter(
                Producto.PLACA_SENA == producto_data['PLACA_SENA'],
                Producto.CODIGO_INTERNO != codigo_interno
            ).first()
            if existing_placa:
                raise HTTPException(status_code=400, detail="La placa SENA ya existe")
        
        # Verificar serial si se está actualizando
        if 'SERIAL' in producto_data and producto_data['SERIAL']:
            existing_serial = db.query(Producto).filter(
                Producto.SERIAL == producto_data['SERIAL'],
                Producto.CODIGO_INTERNO != codigo_interno
            ).first()
            if existing_serial:
                raise HTTPException(status_code=400, detail="El serial ya existe")
    
    for key, value in producto_data.items():
        setattr(db_producto, key, value)
    
    try:
        db.commit()
        db.refresh(db_producto)
        return db_producto
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error al actualizar el producto")

def delete_producto(db: Session, codigo_interno: str):
    db_producto = get_producto_by_codigo(db, codigo_interno)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    try:
        db.delete(db_producto)
        db.commit()
        return {"message": "Producto eliminado exitosamente"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error al eliminar el producto")

def get_contadores(db: Session):
    try:
        # Obtener contadores por tipo de producto
        from .tipo_producto import get_tipos_producto
        tipos_producto = get_tipos_producto(db)
        
        contadores = {}
        
        for tipo in tipos_producto:
            disponibles = db.query(Producto).filter(
                Producto.IDTIPOPRODUCTO == tipo.IDTIPOPRODUCTO,
                Producto.ESTADO == "Disponible"
            ).count()
            
            no_disponibles = db.query(Producto).filter(
                Producto.IDTIPOPRODUCTO == tipo.IDTIPOPRODUCTO,
                Producto.ESTADO != "Disponible"
            ).count()
            
            # Crear nombres de claves basados en el nombre del tipo
            nombre_key = tipo.NOMBRE_TIPO_PRODUCTO.replace(" ", "_").replace("ó", "o")
            contadores[f"{nombre_key}_disponibles"] = disponibles
            contadores[f"{nombre_key}_no_disponibles"] = no_disponibles
        
        # Mantener compatibilidad con nombres anteriores
        total_disponibles = db.query(Producto).filter(Producto.ESTADO == "Disponible").count()
        total_no_disponibles = db.query(Producto).filter(Producto.ESTADO != "Disponible").count()
        
        contadores["totalDisponibles"] = total_disponibles
        contadores["totalNoDisponibles"] = total_no_disponibles
        
        return contadores
    except Exception as e:
        logging.error(f"Error al obtener contadores: {e}")
        raise HTTPException(status_code=500, detail="Error interno al obtener contadores")

async def import_from_excel(db: Session, file: UploadFile):
    """
    Importa productos desde un archivo Excel
    """
    try:
        # Validar el archivo
        if not file.filename.endswith('.xlsx'):
            raise HTTPException(status_code=400, detail="El archivo debe ser un Excel (.xlsx)")
        
        # Leer el archivo Excel
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        
        # Definir las columnas esperadas
        columnas_requeridas = [
            'Código interno',
            'Nombre del producto', 
            'Tipo de producto',
            'Placa',
            'SERIAL',
            'Marca',
            'Estado',
            'Observaciones'
        ]
        
        # Verificar que las columnas requeridas estén presentes
        columnas_disponibles = df.columns.tolist()
        columnas_faltantes = [col for col in columnas_requeridas if col not in columnas_disponibles]
        
        if columnas_faltantes:
            return {
                "columnas_requeridas": columnas_requeridas,
                "columnas_disponibles": columnas_disponibles,
                "columnas_faltantes": columnas_faltantes
            }
        
        # Obtener tipos de producto para validación
        from .tipo_producto import get_tipos_producto
        tipos_producto = get_tipos_producto(db)
        tipos_dict = {tipo.NOMBRE_TIPO_PRODUCTO.lower(): tipo.IDTIPOPRODUCTO for tipo in tipos_producto}
        
        # Contadores
        total_procesados = 0
        exitosos = 0
        errores = []
        
        # Procesar cada fila
        for index, row in df.iterrows():
            fila_num = index + 2  # +2 porque Excel empieza en 1 y hay header
            errores_fila = []
            
            try:
                # Validar campos obligatorios
                codigo_interno = str(row['Código interno']).strip() if pd.notna(row['Código interno']) else ""
                nombre = str(row['Nombre del producto']).strip() if pd.notna(row['Nombre del producto']) else ""
                tipo_producto_nombre = str(row['Tipo de producto']).strip().lower() if pd.notna(row['Tipo de producto']) else ""
                
                if not codigo_interno:
                    errores_fila.append("Código interno es obligatorio")
                if not nombre:
                    errores_fila.append("Nombre del producto es obligatorio")
                if not tipo_producto_nombre:
                    errores_fila.append("Tipo de producto es obligatorio")
                
                # Validar tipo de producto
                tipo_producto_id = None
                if tipo_producto_nombre:
                    tipo_producto_id = tipos_dict.get(tipo_producto_nombre)
                    if not tipo_producto_id:
                        errores_fila.append(f"Tipo de producto '{tipo_producto_nombre}' no existe")
                
                # Validar estado
                estado = str(row['Estado']).strip() if pd.notna(row['Estado']) else "Disponible"
                estados_validos = ['Disponible', 'En préstamo', 'En mantenimiento', 'Dado de baja']
                if estado not in estados_validos:
                    errores_fila.append(f"Estado debe ser uno de: {', '.join(estados_validos)}")
                
                # Campos opcionales
                placa_sena = str(row['Placa']).strip() if pd.notna(row['Placa']) and str(row['Placa']).strip() != '' else None
                serial = str(row['SERIAL']).strip() if pd.notna(row['SERIAL']) and str(row['SERIAL']).strip() != '' else None
                marca = str(row['Marca']).strip() if pd.notna(row['Marca']) and str(row['Marca']).strip() != '' else None
                observaciones = str(row['Observaciones']).strip() if pd.notna(row['Observaciones']) and str(row['Observaciones']).strip() != '' else None
                
                # Si hay errores en la fila, agregarlos y continuar
                if errores_fila:
                    errores.append(f"Fila {fila_num}: {'; '.join(errores_fila)}")
                    total_procesados += 1
                    continue
                
                # Verificar duplicados
                existing_codigo = db.query(Producto).filter(Producto.CODIGO_INTERNO == codigo_interno).first()
                if existing_codigo:
                    errores.append(f"Fila {fila_num}: El código interno '{codigo_interno}' ya existe")
                    total_procesados += 1
                    continue
                
                # Validaciones específicas para equipos de cómputo
                if tipo_producto_nombre == "equipo de cómputo":
                    if placa_sena:
                        existing_placa = db.query(Producto).filter(Producto.PLACA_SENA == placa_sena).first()
                        if existing_placa:
                            errores.append(f"Fila {fila_num}: La placa SENA '{placa_sena}' ya existe")
                            total_procesados += 1
                            continue
                    
                    if serial:
                        existing_serial = db.query(Producto).filter(Producto.SERIAL == serial).first()
                        if existing_serial:
                            errores.append(f"Fila {fila_num}: El serial '{serial}' ya existe")
                            total_procesados += 1
                            continue
                
                # Crear el producto
                producto_data = ProductoCreate(
                    CODIGO_INTERNO=codigo_interno,
                    NOMBRE=nombre,
                    IDTIPOPRODUCTO=tipo_producto_id,
                    PLACA_SENA=placa_sena,
                    SERIAL=serial,
                    MARCA=marca,
                    ESTADO=estado,
                    OBSERVACIONES=observaciones
                )
                
                # Intentar crear el producto
                create_producto(db, producto_data)
                exitosos += 1
                
            except Exception as e:
                errores.append(f"Fila {fila_num}: Error al procesar - {str(e)}")
            
            total_procesados += 1
        
        # Preparar respuesta
        response = {
            "total_procesados": total_procesados,
            "exitosos": exitosos,
            "errores": errores,
            "parcial": exitosos > 0 and len(errores) > 0
        }
        
        return response
        
    except Exception as e:
        logging.error(f"Error al importar productos desde Excel: {e}")
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")

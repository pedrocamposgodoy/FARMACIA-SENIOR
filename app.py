class Medicamento:
    # Datos comunes
    id: str
    nombre: str
    principio_activo: str
    necesita_receta: bool
    cantidad_inicial: int
    cantidad_restante: int
    fecha_compra: date
    frecuencia: dict
    
    # NUEVO
    tipo_tratamiento: str  # "cronico" | "temporal"
    
    # Solo para temporales
    fecha_inicio: date | None
    fecha_fin: date | None
    estado_tratamiento: str  # "activo" | "finalizado" | "abandonado"
    fecha_abandono: date | None
    
    # Comunes
    medicamentos_asociados: list
    vademecum_url: str
    prospecto_url: str
    precauciones: dict
    historial_tomas: list

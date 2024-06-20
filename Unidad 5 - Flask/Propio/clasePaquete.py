class Paquete:
    __id: int
    __numEnvio: int     # Generado automáticamente.
    __peso: float
    __nomDestinatario: str
    __dirDestino: str
    __entregado: bool
    __observaciones: str
    __idSucursal: int               # ID de la sucursal RECEPTORA.
    __idTransporte: int             # ID del transporte ASOCIADO.
    __idRepartidor: int             # ID del repartidor ASIGNADO.

    def __init__(self, id, num, peso, nom, direc, entregado, obs, idS, idT, idR):
        self.__id = id
        self.__numEnvio = num
        self.__peso = peso
        self.__nomDestinatario = nom
        self.__dirDestino = direc
        self.__entregado = entregado     # Ver si debe ir en FALSE.
        self.__observaciones = obs
        self.__idSucursal = idS
        self.__idTransporte = idT
        self.__idRepartidor = idR

    def getIDPaquete(self):
        return self.__id
    
    def getNumEnvio(self):
        return self.__numEnvio
    
    def getPeso(self):
        return self.__peso
    
    def getNomDestinatario(self):
        return self.__nomDestinatario
    
    def getDirDestino(self):
        return self.__dirDestino
    
    def getEntregado(self):             # Hay que chequearlo xd
        return self.__entregado
    
    def getObservaciones(self):
        return self.__observaciones
    
    def getIDSucursalReceptora(self):
        return self.__idSucursal
    
    def getIDTransporteAsociado(self):
        return self.__idTransporte
    
    def getIDRepartidorAsignado(self):
        return self.__idRepartidor
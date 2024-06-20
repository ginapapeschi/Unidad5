class Repartidor:
    __id: int
    __nombre: str
    __dni: float
    __idSucursal: int

    def __init__(self, id, nom, dni, idSucursal):
        self.__id = id
        self.__nombre = nom
        self.__dni = dni
        self.__idSucursal = idSucursal

    def getIDRepartidor(self):
        return self.__id
    
    def getNombre(self):
        return self.__nombre
    
    def getDNI(self):
        return self.__dni
    
    def getIDSucursal(self):
        return self.__idSucursal
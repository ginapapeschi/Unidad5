class Sucursal:
    __id: int
    __num: int
    __provincia: str
    __localidad: str
    __direccion: str

    def __init__(self, id, num, prov, loc, dir):
        self.__id = id
        self.__num = num
        self.__provincia = prov
        self.__localidad = loc
        self.__direccion = dir

    def getIDSucursal(self):
        return self.__id

    def getNumSucursal(self):
        return self.__num
    
    def getProvincia(self):
        return self.__provincia
    
    def getLocalidad(self):
        return self.__localidad
    
    def getDireccion(self):
        return self.__direccion
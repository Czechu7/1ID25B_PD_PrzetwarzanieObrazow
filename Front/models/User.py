class User:
    def __init__(self, id, name, role, token, iat, exp):
        self.id = id
        self.name = name
        self.role = role
        self.token = token
        self.iat = iat
        self.exp = exp        


    def getId(self):
        return self.id
    
    def getToken(self):
        return self.token
    
    def getName(self):
        return self.name
    
    def getRole(self):
        return self.role
    
    def getIat(self):
        return self.iat
    
    def getExp(self):
        return self.exp
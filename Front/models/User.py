class User:
    def __init__(self, id, name, role, token):
        self.id = id
        self.name = name
        self.role = role
        self.token = token


    def getId(self):
        return self.id
    
    def getToken(self):
        return self.token
    
    def getName(self):
        return self.name
    
    def getRole(self):
        return self.role
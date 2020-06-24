import jwt, datetime  

class Token:
    def generateToken(self,appid,appsecret,roomname,firstname,email,id,group,avatar,moderator):
        template = {
                "context": {
                    "user": {
                    "avatar": "https:/gravatar.com/avatar/abc123",
                    "name": "",
                    "email": "",
                    "id": "abcd:a1b2c3-d4e5f6-0abc1-23de-abcdef01fedcba"
                    },
                "group": "a123-123-456-789"
                    },
                "aud": "",
                "iss": "",
                "sub": "meet.jitsi",
                "room": "",
                "exp":  100,
                "moderator": "false" }
        template['aud']  = appid
        template['iss'] = appid
        template['moderator'] = moderator
        if not avatar:
            template['context']['user']['avatar'] = avatar
        template['context']['user']['name'] = firstname
        template['context']['user']['email'] = email
        if not id:
            template['context']['user']['id'] = id
        if not group:
            template['context']['group'] = group
        template['room'] = roomname
        template['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=20)
        return jwt.encode(template, appsecret, algorithm='HS256').decode('utf-8')

    def generateToken_CreateMeeting(self,roomname,owner,appsecret): 
        template = { }
        template['roomname']  = roomname
        template['owner'] = owner 
        return jwt.encode({'roomname':roomname,'owner':owner}, appsecret, algorithm='HS256').decode('utf-8')
                
    def decodeToken(self,token,appsecret):   
        token = token.strip() 
        token = token.replace('"','') 
        #print(token)
        try:
            decode = jwt.decode(token, appsecret, algorithm=['HS256']) 
        except (KeyError,jwt.DecodeError, jwt.ExpiredSignature):
            return 'error - Invalid JWT Token'    
        return jwt.decode(token, appsecret, algorithm=['HS256']) 

    def encodeResult_CreateMeeting(self,result,password,appsecret):
        template={}
        template['result']=result
        template['password']=password
        return jwt.encode(template, appsecret, algorithm='HS256').decode('utf-8')

    def generateToken_StartMeeting(self,roomname,name,password,moderator,appsecret):
        template = { }
        template['roomname']=roomname
        template['name']=name
        template['password']=password
        template['moderator']=moderator 
        return jwt.encode(template, appsecret, algorithm='HS256').decode('utf-8')

    def encodeResult_StartMeeting(self,result,appsecret):
        template={}
        template['result']=result 
        return jwt.encode(template, appsecret, algorithm='HS256').decode('utf-8')
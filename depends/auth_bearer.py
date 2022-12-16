from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from depends.auth_handler import decodeJWT
import time

class JWTBearer(HTTPBearer):
    """_summary_

    Args:
        HTTPBearer (_type_): _description_
    Desc:
        Lớp này chịu trách nhiệm thực thi việc kiểm tra tính hợp lệ của người dùng khi nhận được yêu cầu thực hiện tính năng
    """
    def __init__(self, auto_error: bool = True):
        super(JWTBearer,self).__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request):
        """Được gọi trước khi thực hiện request"""
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer,self).__call__(request)
        
        if credentials:
            
            if not credentials.scheme == "Bearer": # kiểm tra tính đúng đắn theo chuẩn Bearer
                raise HTTPException(status_code=403, detail='Invalid authentication scheme')
            
            if not self.verify_jwt(credentials.credentials): # kiểm tra token
                raise HTTPException(status_code=403, detail='Invalid token or expired')
            
            return credentials.credentials
        
        else:
            raise HTTPException(status_code=403,detail='Invalid authorization code.')
        
    # cần bổ sung thêm thông số của request để nhận biết url nào đang được gọi đến
    def verify_jwt(self,jwtoken: str)->bool:
        isTokenValid: bool = False
        try:
            payload = decodeJWT(jwtoken, with_secret_key=True)
            #

            #sau khi phân rã và xác định user_ID, truy tìm chức danh và phòng ban
            # print('payload',payload['expires'])
            # print('timesystem',time.time())
            # phân rã thông tin từ payload để xác định người dùng có thể thực hiện chức năng này hay không,
            # nếu không đúng sẽ raise HTTPException cũng như kiểm tra thời gian hiệu lực của token (nếu cần)
            # remove cmt to verify jwt_key is timeout
            # if time.time() < payload['expires']:
            #     raise HTTPException(status_code=403, detail='Token timeout')
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
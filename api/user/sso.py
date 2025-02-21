
import logging
from flask import Blueprint, request
from api.db.services.user_service import UserService
from api.utils.api_utils import get_json_result
from flask_login import login_user
from api import settings
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
import base64
import time
import hmac
import hashlib

# 创建蓝图
sso_bp = Blueprint('sso', __name__, url_prefix='/v1')
logger = logging.getLogger(__name__)

SECRET_KEY_BYTES = b"infiniflow_sso_secret_key_2024"

def encrypt_email_with_timestamp(email: str, timestamp: int = None) -> str:
    """
    加密email和时间戳
    :param email: 邮箱地址
    :param timestamp: 时间戳（秒），如果为None则使用当前时间
    :param key: 密钥
    :return: 加密后的字符串
    """
    if timestamp is None:
        timestamp = int(time.time())
    
    # 将email和timestamp组合
    message = f"{email}:{timestamp}".encode()
    
    # 使用HMAC-SHA256生成签名
    signature = hmac.new(SECRET_KEY_BYTES, message, hashlib.sha256).digest()
    
    # 组合消息和签名，并进行base64编码
    final_message = message + signature
    encoded = base64.urlsafe_b64encode(final_message).decode()
    
    return encoded

def decrypt_email_with_timestamp(encoded_str: str, max_age: int = 3600) -> tuple:
    """
    解密并验证email和时间戳
    :param encoded_str: 加密的字符串
    :param max_age: 最大有效期（秒）
    :return: (email, is_valid, error_message)
    """
    try:
        #logger.info(f"Received encrypted string: {encoded_str}")
        # 确保Base64字符串长度是4的倍数
        padding_length = len(encoded_str) % 4
        if padding_length:
            encoded_str += '=' * (4 - padding_length)

        # base64解码
        decoded = base64.urlsafe_b64decode(encoded_str.encode())
        
        # 分离消息和签名 (忽略签名部分)
        message = decoded[:-32]  # 只取消息部分
        
        # 解析消息
        email, timestamp_str = message.decode().split(":")
        timestamp = int(timestamp_str)
        #logger.info(f"Decoded email: {email}, timestamp: {timestamp}")
        
        # 验证时间戳
        current_time = int(time.time())
        if current_time - timestamp > max_age:
            return email, False, "Link expired"
        
        return email, True, "Valid"
    except Exception as e:
        logger.error(f"Decryption error details: {str(e)}")
        return None, False, f"Decryption error: {str(e)}"

@sso_bp.route('/user/sso_login', methods=['POST'])
def sso_login():
    #print("SSO Login endpoint called!")
    #logger.info("SSO Login endpoint called with request: %s", request.get_json())

    try:
        # 获取请求数据
        data = request.get_json()
        encrypted_str = data.get('email', '').strip()

        email, is_valid, message = decrypt_email_with_timestamp(encrypted_str)
        if is_valid:
            # 继续处理登录逻辑
            # 参数校验
            if not email:
                logger.warning("SSO Login: Empty email received")
                return get_json_result(code=settings.RetCode.AUTHENTICATION_ERROR, message='Email is required')
   
            # 查找用户
            #logger.info(f"解析过后的emailLLLLLLLLLL: {email}")
            users = UserService.query(email=email)

            if not users:
                logger.warning(f"SSO Login failed: User not found for email: {email}")
                return get_json_result(
                data=False,
                code=settings.RetCode.AUTHENTICATION_ERROR,
                message=f"Email: {email} is not registered!"
            )

            # 获取用户
            user = users[0]
        
            # 生成token
            # 生成token - 使用与__init__.py中相同的序列化方式
            jwt = Serializer(secret_key=settings.SECRET_KEY)
            encoded_token = jwt.dumps(user.id)  # 编码后的token，用于返回给前端
            raw_token = str(user.id)   
        
            # 更新用户token
            user.access_token = raw_token
            UserService.update_by_id(user.id, {"access_token": raw_token})
        
            # 登录用户
            login_user(user)
        
            return get_json_result(
                data={"access_token": encoded_token},
                code=settings.RetCode.SUCCESS,
                message="SSO Login Successful"
        )
        else:
            # 处理错误，message 包含具体错误信息
            logger.warning(f"SSO Login failed: {message}")
            return get_json_result(
                data=False,
                code=settings.RetCode.AUTHENTICATION_ERROR,
                message=message
            )
       

    except Exception as e:
        logger.error(f"SSO Login error: {str(e)}")
        return get_json_result(code=settings.RetCode.SERVER_ERROR, message='Internal server error')
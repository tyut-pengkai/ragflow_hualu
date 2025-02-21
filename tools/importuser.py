# import sys
# import csv
# import uuid
# from datetime import datetime
# from werkzeug.security import generate_password_hash
# from api.db.services.user_service import UserService, TenantService, UserTenantService
# from api.db.services.file_service import FileService
# from api.db.services.llm_service import TenantLLMService, LLMService
# from api.db import UserTenantRole, FileType
# from api import settings
# from api.utils import get_uuid, get_format_time

# def batch_register_users(csv_file_path):
#     """
#     从CSV文件批量导入用户
#     CSV格式：nickname,email,password
#     """
#     with open(csv_file_path, 'r', encoding='gbk') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             try:
#                 user_id = get_uuid()
#                 user_dict = {
#                     "id": user_id,
#                     "access_token": get_uuid(),
#                     "email": row['email'],
#                     "nickname": row['nickname'],
#                     "password": row['password'],  # 注意：这里假设密码已经是明文
#                     "login_channel": "password",
#                     "last_login_time": get_format_time(),
#                     "is_superuser": False,
#                 }
                
#                 # 创建租户信息
#                 tenant = {
#                     "id": user_id,
#                     "name": f"{row['nickname']}'s Kingdom",
#                     "llm_id": 'deepseek-r1:8b@Ollama',
#                     "embd_id": 'bge-m3:latest@Ollama',
#                     "asr_id": 'paraformer-realtime-8k-v1@Tongyi-Qianwen',
#                     "parser_ids": 'naive:General,qa:Q&A,resume:Resume,manual:Manual,table:Table,paper:Paper,book:Book,laws:Laws,presentation:Presentation,picture:Picture,one:One,audio:Audio,email:Email,tag:Tag',
#                     "img2txt_id": 'qwen-vl-max@Tongyi-Qianwen',
#                     "rerank_id": 'BAAI/bge-reranker-v2-m3@BAAI',
#                 }
                
#                 # 创建用户-租户关系
#                 usr_tenant = {
#                     "tenant_id": user_id,
#                     "user_id": user_id,
#                     "invited_by": user_id,
#                     "role": UserTenantRole.OWNER,
#                 }
                
#                 # 创建根文件夹
#                 file_id = get_uuid()
#                 file = {
#                     "id": file_id,
#                     "parent_id": file_id,
#                     "tenant_id": user_id,
#                     "created_by": user_id,
#                     "name": "/",
#                     "type": FileType.FOLDER.value,
#                     "size": 0,
#                     "location": "",
#                 }
                
#                 # 创建租户的LLM配置
#                 tenant_llm = []
#                 for llm in LLMService.query(fid=settings.LLM_FACTORY):
#                     tenant_llm.append({
#                         "tenant_id": user_id,
#                         "llm_factory": settings.LLM_FACTORY,
#                         "llm_name": llm.llm_name,
#                         "model_type": llm.model_type,
#                         "api_key": settings.API_KEY,
#                         "api_base": settings.LLM_BASE_URL,
#                         "max_tokens": llm.max_tokens if llm.max_tokens else 8192
#                     })
                
#                 # 保存所有数据
#                 if not UserService.save(**user_dict):
#                     print(f"Failed to create user: {row['email']}")
#                     continue
                    
#                 TenantService.insert(**tenant)
#                 UserTenantService.insert(**usr_tenant)
#                 TenantLLMService.insert_many(tenant_llm)
#                 FileService.insert(file)
                
#                 print(f"Successfully created user: {row['email']}")
                
#             except Exception as e:
#                 print(f"Error creating user {row['email']}: {str(e)}")
#                 # 如果出错，尝试回滚
#                 try:
#                     UserService.delete(user_id)
#                     TenantService.delete(user_id)
#                     UserTenantService.delete(tenant_id=user_id)
#                     FileService.delete(file_id)
#                 except:
#                     pass

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Usage: python batch_register_users.py <csv_file_path>")
#         sys.exit(1)
    
#     csv_file_path = sys.argv[1]
#     batch_register_users(csv_file_path)
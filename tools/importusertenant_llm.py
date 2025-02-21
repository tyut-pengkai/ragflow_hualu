# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

# import sys
# import os

# # 禁用代理设置
# os.environ['http_proxy'] = ''
# os.environ['https_proxy'] = ''
# os.environ['all_proxy'] = ''
# os.environ['HTTP_PROXY'] = ''
# os.environ['HTTPS_PROXY'] = ''
# os.environ['ALL_PROXY'] = ''

# from api.db.db_models import Tenant, DB, TenantLLM
# from api.db import StatusEnum
# from api.db.services.user_service import TenantService
# from api.db.services.llm_service import TenantLLMService

# def get_all_valid_tenants():
#     """
#     直接查询所有有效的租户
#     """
#     with DB.connection_context():
#         query = Tenant.select().where(Tenant.status == StatusEnum.VALID.value)
#         tenants = list(query)
#         print(f"Found {len(tenants)} valid tenants")
#         return tenants

# def import_tenant_llm():
#     """
#     从源租户导入 LLM 配置到其他租户
#     """
#     # 源租户 ID
#     source_tenant_id = '255f4c1aedc711ef93521957bb0373df'
#     # 排除的租户 ID 列表
#     excluded_tenant_ids = [
#         '255f4c1aedc711ef93521957bb0373df',  # 源租户
#         '016cf7dfee7211efaddfc15d9ec6c1ee'   # 其他要排除的租户
#     ]
    
#     # 1. 获取源租户的 LLM 配置
#     source_llm_configs = TenantLLMService.query(tenant_id=source_tenant_id)
#     if not source_llm_configs:
#         print(f"No LLM configurations found for source tenant: {source_tenant_id}")
#         return
        
#     # 2. 获取目标租户列表（排除指定的租户）
#     target_tenants = get_all_valid_tenants()
    
#     target_tenant_ids = [
#         tenant.id for tenant in target_tenants 
#         if tenant.id not in excluded_tenant_ids
#     ]
    
#     print(f"\nAfter excluding specified tenants, found {len(target_tenant_ids)} target tenants")
#     if target_tenant_ids:
#         print("Target tenant IDs:")
#         for tid in target_tenant_ids:
#             print(f"- {tid}")
    
#     if not target_tenant_ids:
#         print("\nNo target tenants found after exclusion")
#         print(f"Excluded tenant IDs: {excluded_tenant_ids}")
#         return
        
#     # 3. 为每个目标租户创建 LLM 配置
#     for tenant_id in target_tenant_ids:
#         try:
#             # 备份当前配置
#             backup_configs = backup_tenant_llm_configs(tenant_id)
            
#             # 准备新的 LLM 配置
#             new_llm_configs = []
#             for config in source_llm_configs:
#                 new_config = {
#                     "tenant_id": tenant_id,
#                     "llm_factory": config.llm_factory,
#                     "model_type": config.model_type,
#                     "llm_name": config.llm_name,
#                     "api_key": config.api_key,
#                     "api_base": config.api_base,
#                     "max_tokens": config.max_tokens
#                 }
#                 new_llm_configs.append(new_config)
            
#             # 删除已存在的配置
#             with DB.connection_context():
#                 TenantLLM.delete().where(TenantLLM.tenant_id == tenant_id).execute()
            
#             # 插入新配置
#             if new_llm_configs:
#                 with DB.connection_context():
#                     TenantLLM.insert_many(new_llm_configs).execute()
            
#             print(f"Successfully imported LLM configs for tenant: {tenant_id}")
            
#         except Exception as e:
#             print(f"Error importing LLM configs for tenant {tenant_id}: {str(e)}")

# def backup_tenant_llm_configs(tenant_id: str):
#     """
#     备份租户的 LLM 配置
#     """
#     configs = TenantLLMService.query(tenant_id=tenant_id)
#     if not configs:
#         return []
    
#     return [{
#         "tenant_id": config.tenant_id,
#         "llm_factory": config.llm_factory,
#         "model_type": config.model_type,
#         "llm_name": config.llm_name,
#         "api_key": config.api_key,
#         "api_base": config.api_base,
#         "max_tokens": config.max_tokens
#     } for config in configs]

# if __name__ == "__main__":
#     import_tenant_llm()
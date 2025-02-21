# from api.db.services.user_service import UserService, UserTenantService
# from api.db import UserTenantRole
# from api.db.db_models import User  
# from api import settings

# def update_user_tenants():
#     """
#     更新用户租户关系：
#     1. 遍历所有用户
#     2. 排除特定邮箱的用户
#     3. 为其他用户创建新的租户关系
#     """
#     # 初始化设置
#     settings.init_settings()
    
#     # 要排除的邮箱列表
#     exclude_emails = ['mxy2479@hlet.com', 'smy2234@hlet.com']
    
#     # 固定的租户ID和邀请人ID
#     tenant_id = '255f4c1aedc711ef93521957bb0373df'
#     invited_by = '255f4c1aedc711ef93521957bb0373df'
    
#     # 获取所有用户
#     users = User.select()  
#     users_list = list(users)
#     if not users_list:
#         print("Error: No users found in database!")
#         return False
        
#     print(f"\nTotal users found: {len(users_list)}")
    
#     # 记录已处理的用户，用于回滚
#     processed_users = []
#     skipped_users = 0
#     existing_users = 0
    
#     try:
#         # 遍历用户并创建租户关系
#         for user in users_list:
#             try:
#                 # 跳过排除的邮箱
#                 if user.email in exclude_emails:
#                     print(f"Skipping excluded user: {user.email}")
#                     skipped_users += 1
#                     continue
                
#                 # 检查是否已经存在租户关系
#                 existing = UserTenantService.query(
#                     tenant_id=tenant_id,
#                     user_id=user.id
#                 )
#                 if existing:
#                     print(f"Tenant relationship already exists for user: {user.email}")
#                     existing_users += 1
#                     continue
                
#                 # 创建用户-租户关系
#                 user_tenant = {
#                     "tenant_id": tenant_id,
#                     "user_id": user.id,
#                     "invited_by": invited_by,
#                     "role": UserTenantRole.NORMAL,
#                 }
                
#                 # 插入数据
#                 print(f"\nTrying to insert tenant relationship for {user.email}")
#                 print(f"User tenant data: {user_tenant}")
#                 result = UserTenantService.insert(**user_tenant)
#                 print(f"Insert result: {result}")
                
#                 processed_users.append(user.id)
#                 print(f"Successfully added tenant relationship for user: {user.email}")
                
#             except Exception as e:
#                 print(f"Error processing user {user.email}: {str(e)}")
#                 raise  # 抛出异常以触发回滚
                
#     except Exception as e:
#         print(f"\nError occurred during processing. Starting rollback...")
#         # 回滚所有已处理的用户
#         for user_id in processed_users:
#             try:
#                 UserTenantService.delete(tenant_id=tenant_id, user_id=user_id)
#                 print(f"Rolled back tenant relationship for user_id: {user_id}")
#             except Exception as rollback_error:
#                 print(f"Error during rollback for user_id {user_id}: {str(rollback_error)}")
        
#         print(f"Rollback completed. Original error: {str(e)}")
#         return False
    
#     print(f"\nProcessing Summary:")
#     print(f"Total users: {len(users_list)}")
#     print(f"Skipped users: {skipped_users}")
#     print(f"Existing relationships: {existing_users}")
#     print(f"Successfully processed: {len(processed_users)}")
#     return True

# if __name__ == "__main__":
#     success = update_user_tenants()
#     if not success:
#         print("Script failed with errors. Please check the logs above.")
#     else:
#         print("Script completed successfully.")
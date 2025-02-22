# 增加苗小智
# INSERT INTO dialog (
#     id, create_time, create_date, update_time, update_date,
#     tenant_id, name, description, icon, language,
#     llm_id, llm_setting, prompt_type, prompt_config,
#     similarity_threshold, vector_similarity_weight,
#     top_n, top_k, do_refer, rerank_id, kb_ids, status
# )
# SELECT 
#     REPLACE(UUID(), '-', ''), -- 生成32位的uuid作为id
#     UNIX_TIMESTAMP() * 1000, -- create_time
#     NOW(), -- create_date
#     UNIX_TIMESTAMP() * 1000, -- update_time
#     NOW(), -- update_date
#     t.id, -- 新的tenant_id（从tenant表的id字段获取）
#     d.name, d.description, d.icon, d.language,
#     d.llm_id, d.llm_setting, d.prompt_type, d.prompt_config,
#     d.similarity_threshold, d.vector_similarity_weight,
#     d.top_n, d.top_k, d.do_refer, d.rerank_id, d.kb_ids, d.status
# FROM dialog d 
# CROSS JOIN tenant t
# WHERE d.name = '苗小智' 
# AND d.tenant_id = '255f4c1aedc711ef93521957bb0373df'
# AND t.id != '255f4c1aedc711ef93521957bb0373df';
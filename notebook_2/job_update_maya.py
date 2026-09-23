# Databricks Job Script: Automated SCD Type 2 Update for Maya Lin
import re
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

# Retrieve user context
user_email = spark.sql("SELECT current_user()").collect()[0][0]
name_parts = re.sub(r'[^a-zA-Z0-9 ]', ' ', user_email.split('@')[0]).split()
first_name = name_parts[0].lower()
last_initial = name_parts[1][0].lower() if len(name_parts) > 1 else ""

user_prefix = f"{first_name}_{last_initial}"

CATALOG_NAME = f"data_eng_{user_prefix}"
SCHEMA_NAME = f"{user_prefix}"

# Stage Maya Lin practice change & promotion
maya_update_df = spark.createDataFrame([
    ("C003", "Maya Lin", "AI & Decision Intelligence", "Senior Consultant", "2026-09-17")
], ["consultant_id", "full_name", "practice", "seniority_level", "effective_date"])

maya_update_df.createOrReplaceTempView("maya_updates")

# Execute SCD Type 2 MERGE
spark.sql(f"""
MERGE INTO `{CATALOG_NAME}`.`{SCHEMA_NAME}`.`dim_consultant` target
USING (
    SELECT 
        consultant_id AS merge_key,
        consultant_id, full_name, practice, seniority_level, effective_date
    FROM maya_updates
    UNION ALL
    SELECT 
        NULL AS merge_key,
        u.consultant_id, u.full_name, u.practice, u.seniority_level, u.effective_date
    FROM maya_updates u
    JOIN `{CATALOG_NAME}`.`{SCHEMA_NAME}`.`dim_consultant` d ON u.consultant_id = d.consultant_id
    WHERE d.is_current = TRUE AND (d.seniority_level <> u.seniority_level OR d.practice <> u.practice)
) src
ON target.consultant_id = src.merge_key AND target.is_current = TRUE
WHEN MATCHED AND (target.seniority_level <> src.seniority_level OR target.practice <> src.practice) THEN
  UPDATE SET 
    target.is_current = FALSE,
    target.valid_to = CAST(src.effective_date AS DATE)
WHEN NOT MATCHED THEN
  INSERT (
    consultant_hash_key, consultant_id, full_name, practice, seniority_level, is_current, valid_from, valid_to
  )
  VALUES (
    sha2(concat_ws('||', src.consultant_id, src.full_name, src.seniority_level, src.practice), 256),
    src.consultant_id, src.full_name, src.practice, src.seniority_level, TRUE, CAST(src.effective_date AS DATE), NULL
  )
""")

print("✅ Maya Lin SCD Type 2 automated update executed successfully via Databricks Job!")
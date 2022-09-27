# 常用命令
/*
链接postgres数据库：
psql postgres://postgres:68Hjg6QYxNNPhAosp55Z@lite-pg.cvxmlpsy4xpw.eu-central-1.rds.amazonaws.com:5432/
psql postgresql://kili_prd_dbo:kd0LLk345byKNXhg4@lite-pg.cvxmlpsy4xpw.eu-central-1.rds.amazonaws.com/prd_data_centers

创建角色，并进行初始化设置
CREATE ROLE kili_prd_dbo LOGIN CREATEDB CREATEROLE INHERIT ENCRYPTED PASSWORD 'kd0LLk345byKNXhg4';
select * from pg_user;
select * from pg_roles;
切换用户：\c - [user_name]
给用户创建数据库：
create database prd_data_centers owner kili_prd_dbo;

INSERT INTO example_table (id, name)
SELECT 1 AS id, 'John' AS name FROM example_table
WHERE NOT EXISTS(
            SELECT id FROM example_table WHERE id = 1
    )
LIMIT 1;

INSERT INTO test_tab(name,sex,address,lastEndTime,createTime)
SELECT 'a','b','c',1,1
FROM (select 1) tmp WHERE NOT EXISTS (Select 1 FROM test_tab where name = '0')

CREATE TYPE YOUR_TYPE AS (
    id      integer,
    field   varchar
);

连接数据库: psql -h localhost -p 5432 -U postgres runoobdb
psql postgresql://pf_prd_dbo:l2w9ZVZP4gU2x9b24u6z@159.138.82.236:5432/test_data_centers
查看数据库： \l
进入数据库：\c + 数据库名
查看表名： \d
*/



explain analyze SELECT user_id, first_name, second_name, birthdate, biography, city FROM users WHERE first_name_tsvector @@ to_tsquery('russian', 'ан:*') and second_name_tsvector @@ to_tsquery('russian', 'бе:*') order by user_id asc

explain analyze SELECT user_id, first_name, second_name, birthdate, biography, city FROM users WHERE first_name ilike 'ан%' and second_name ilike 'бе%' order by user_id asc

SELECT count(*) FROM users WHERE first_name_tsvector @@ to_tsquery('russian', 'Ан:*') and second_name_tsvector @@ to_tsquery('russian', 'Бе:*')
SELECT count(*) FROM users WHERE first_name like 'Ан%' and second_name like 'Бе%'
CREATE INDEX ON users(second_name)

select * from pg_stat_user_indexes;

drop index user_id_idx
alter table users add column first_name_tsvector tsvector
alter table users add column second_name_tsvector tsvector

update users set first_name_tsvector=to_tsvector('russian', first_name)
update users set second_name_tsvector=to_tsvector('russian', second_name)
create index fs_idx on users using gin(first_name_tsvector,second_name_tsvector)
create index user_id_idx on users(user_id)


SELECT user_id, first_name, second_name, birthdate, biography, city FROM users WHERE first_name_tsvector @@ to_tsquery('russian', 'А:*')

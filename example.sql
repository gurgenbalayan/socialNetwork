CREATE DATABASE social_network;

select user_id from social_network.users limit 10;

select DISTINCT friends.friend_id_second from friends

INSERT INTO posts (author_id, posts, date) VALUES ('ce5bd74e-ef89-4f70-a98b-5c4dc288c695','тестовый пост', NOW())
select author_id, posts, posts.date from posts left join friends on author_id=friend_id_second where friend_id_first='ce5bd74e-ef89-4f70-a98b-5c4dc288c695' ORDER BY posts.date DESC LIMIT 100 OFFSET 0

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

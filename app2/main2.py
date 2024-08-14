import uvicorn


if __name__ == '__main__':
#    create_table_users()
#    create_table_posts()
#    create_table_friends()
#    create_table_dialogs()
#    build_all_cache_for_all_friends()
    uvicorn.run('app2:app2', host='127.0.0.1', port=8006, log_config="log_conf.yaml")
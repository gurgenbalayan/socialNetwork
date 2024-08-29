import sys

import uvicorn

import app
from create_tables import create_table_users, create_table_posts, create_table_friends, create_table_dialogs, create_table_chats
from rebuild_cache import build_all_cache_for_all_friends

if __name__ == '__main__':
#    create_table_users()
#    create_table_posts()
#    create_table_friends()
#    create_table_dialogs()
#    build_all_cache_for_all_friends()
    create_table_chats()
    #uvicorn.run('app:app', host='127.0.0.1', port=int(sys.argv[1]))
    uvicorn.run('app:app', host='127.0.0.1', port=8006)

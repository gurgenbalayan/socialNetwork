import uvicorn

import app
from create_tables import create_table_users, create_table_posts, create_table_friends
from rebuild_cache import *

if __name__ == '__main__':
#    create_table_users()
#    create_table_posts()
#    create_table_friends()
#    rebuild_cache_for_user('feed_55a7df26-f444-481b-b23c-9deaf676f861')
    uvicorn.run('app:app', host='127.0.0.1', port=8000)
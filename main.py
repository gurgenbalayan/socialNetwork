import uvicorn

import app
from create_tables import create_table_users, create_table_posts

if __name__ == '__main__':
    create_table_users()
    create_table_posts()

    uvicorn.run('app:app', host='127.0.0.1', port=8000)
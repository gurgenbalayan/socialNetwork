import sys
sys.path.insert(0,"app3")
from app3.db3 import add_unread, rollback_unread
sys.path.insert(0,"app2")
from db2 import get_dialog, send_message, rollback_send

def execute_saga(sender, recipient, message, date):
    try:
        add_unread(sender, recipient, date)
        send_message(sender, recipient, message, str(date))
        return "success"
    except:
        print("Произошла ошибка")
        rollback_saga(sender, recipient)
        return "error"

def rollback_saga(sender, recipient, message, date):
    try:
        rollback_send(sender, recipient, message, date)
        rollback_unread(sender, recipient, date)
    except Exception as e:
        print("Ошибка при откате саги: {e}")



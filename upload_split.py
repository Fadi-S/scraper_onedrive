from get_token import get_token
from onedrive import OneDrive
from multiprocessing import Process, Queue
import os
import json


def timeout(seconds, action=None):
    """Calls any function with timeout after 'seconds'.
       If a timeout occurs, 'action' will be returned or called if
       it is a function-like object.
    """
    def handler(queue, func, args, kwargs):
        queue.put(func(*args, **kwargs))

    def decorator(func):

        def wraps(*args, **kwargs):
            q = Queue()
            p = Process(target=handler, args=(q, func, args, kwargs))
            p.start()
            p.join(timeout=seconds)
            if p.is_alive():
                p.terminate()
                p.join()
                if hasattr(action, '__call__'):
                    return action()
                else:
                    return action
            else:
                return q.get()

        return wraps

    return decorator


token = get_token()
onedrive = OneDrive(token)


def update_token():
    print("Updating token")
    onedrive.token = get_token()


timeout(3600, update_token)

uploaded_files = []
if os.path.exists("uploaded_files.json"):
    with open("uploaded_files.json", "r") as file:
        uploaded_files = json.load(file)
else:
    uploaded = onedrive.list_files("me/drive/root:/deep_learning/data/splitted_audio")
    uploaded_files = [os.path.join("data/splitted_audio/", file['name']) for file in uploaded]
    # Save the list of uploaded files to avoid re-uploading
    with open("uploaded_files.json", "w") as file:
        json.dump(uploaded_files, file)
# uploaded_files = []

success = onedrive.upload_folder(
    "data/splitted_audio",
    "me/drive/root:/deep_learning/data/splitted_audio",
    skip=uploaded_files
)

print("Uploaded folder successfully")

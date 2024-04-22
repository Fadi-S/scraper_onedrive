from get_token import get_token
from onedrive import OneDrive
from multiprocessing import Process, Queue


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
    onedrive.token = get_token()


timeout(3600, update_token)

success = onedrive.upload_folder(
    "data/splitted_audio",
    "me/drive/root:/deep_learning/data/splitted_audio"
)

print("Uploaded folder successfully")

import websocket
import _thread as thread
import time
import json
import stomp

class WebSocketStompClient:
    def __init__(self, websocket_url, photo_id):
        self.websocket_url = websocket_url
        self.photo_id = photo_id
        self.ws = None
        self.conn = None

    def on_message(self, ws, message):
        print("Received message: " + message)

    def on_error(self, ws, error):
        print("Error: " + str(error))

    def on_close(self, ws, close_status_code, close_msg):
        print("WebSocket closed")

    def on_open(self, ws):
        def run(*args):
            self.conn = stomp.Connection12([('localhost', 8080)])
            self.conn.set_listener('', self.MyListener())
            self.conn.connect(wait=True, headers={'host': 'localhost:8080'})

            # Subskrypcja topicu
            self.conn.subscribe(destination=f'/topic/{self.photo_id}', id=1, ack='auto')

            # Wysłanie wiadomości do endpointu annotate
            annotation_message = {
                "photoId": self.photo_id,
                "userId": "user1",
                "content": "This is an annotation for the photo."
            }
            message = json.dumps(annotation_message)
            self.conn.send(body=message, destination=f'/app/annotate/{self.photo_id}')

            print("Connected and subscribed to /topic/%s" % self.photo_id)

            while True:
                time.sleep(1)

        thread.start_new_thread(run, ())

    class MyListener(stomp.ConnectionListener):
        def on_error(self, frame):
            print('Received an error: %s' % frame.body)

        def on_message(self, frame):
            print('Received a message: %s' % frame.body)

    def connect(self):
        self.ws = websocket.WebSocketApp(
            self.websocket_url,
            on_open=self.on_open,
            # on_message=self.on_message,F
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws.run_forever()

    def send_message(self, annotation_message):
        if self.conn:
            message = json.dumps(annotation_message)
            self.conn.send(body=message, destination=f'/app/annotate/{self.photo_id}')

# Example usage
# client = WebSocketStompClient("ws://localhost:8080/photo-socket", "123")
# client.connect()

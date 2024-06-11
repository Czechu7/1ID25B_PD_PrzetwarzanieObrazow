import websocket
import _thread as thread
import time
import json
import stomp
from websocket import create_connection

class MyListener(stomp.ConnectionListener):
    def on_error(self, frame):
        print('Received an error: %s' % frame.body)

    def on_message(self, frame):
        print('Received a message: %s' % frame.body)

# Funkcja obsługująca połączenie WebSocket
def on_open(ws):
    def run(*args):
        # Po nawiązaniu połączenia WebSocket, połącz się za pomocą STOMP
        conn = stomp.Connection()
        conn.set_listener('', MyListener())
        conn.connect(wait=True)
        # Subskrybuj topic
        photo_id = "123"
        conn.subscribe(destination=f'/topic/{photo_id}', id=1, ack='auto')

        # Wysłanie wiadomości do endpointu /app/annotate
        annotation_message = {
            "photoId": photo_id,
            "userId": "user1",
            "content": "This is an annotation for the photo."
        }
        message = json.dumps(annotation_message)
        conn.send(body=message, destination=f'/app/annotate/{photo_id}')

        print("Connected and subscribed to /topic/%s" % photo_id)
        
        # Utrzymywanie połączenia dla odbierania wiadomości
        while True:
            time.sleep(1)
    thread.start_new_thread(run, ())

# Funkcja obsługująca komunikaty z WebSocket
def on_message(ws, message):
    print("Received message from WebSocket: " + message)

# Funkcja obsługująca błędy z WebSocket
def on_error(ws, error):
    print("WebSocket error: " + str(error))

# Funkcja obsługująca zamknięcie połączenia WebSocket
def on_close(ws):
    print("WebSocket closed")

if __name__ == "__main__":
    # URL WebSocket serwera
    websocket_url = "ws://localhost:8080/photo-socket/websocket"

    # Ustanowienie połączenia WebSocket
    ws = websocket.WebSocketApp(
        websocket_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    # Nawiązanie połączenia
    ws.run_forever()

import socket
import threading

# Lista de réplicas conectadas
replicas = []

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            
            print(f"Datos recibidos: {data.decode('utf-8')}")

            # Enviar datos a las réplicas válidas
            for replica in replicas[:]:  # Usar una copia de la lista para evitar problemas al eliminar elementos
                try:
                    replica.send(data)
                except Exception as e:
                    print(f"Error al enviar datos a la réplica: {e}")
                    replicas.remove(replica)  # Eliminar la réplica inválida de la lista

        except (ConnectionResetError, ConnectionAbortedError) as e:
            print(f"Error de conexión: {e}")
            break

    # Cerrar el socket del cliente después de salir del bucle
    client_socket.close()

def master_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.0.211', 9999))
    server.listen(5)
    print("Servidor maestro escuchando en el puerto 9999...")

    while True:
        client_socket, addr = server.accept()
        print(f"Conexión aceptada de: {addr}")

        # Añadir la réplica a la lista
        replicas.append(client_socket)

        # Iniciar un hilo para manejar al cliente
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    master_server()

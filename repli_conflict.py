import socket

def replica_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))  # IP del servidor maestro

    while True:
        data = client.recv(1024)
        if not data:
            break

        print(f"Datos replicados: {data.decode('utf-8')}")

    client.close()

if __name__ == "__main__":
    replica_server()
def repli_conflict(existing_data, new_data):

    # Verificar que ambos datos contengan el campo 'timestamp'
    if 'timestamp' not in existing_data or 'timestamp' not in new_data:
        raise ValueError("Ambos conjuntos de datos deben contener el campo 'timestamp'.")

    # Estrategia de última escritura gana
    return new_data if new_data['timestamp'] > existing_data['timestamp'] else existing_data
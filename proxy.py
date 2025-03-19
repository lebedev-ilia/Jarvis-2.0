import time
import socket
import threading
import subprocess

def generate_wireguard_keys():
    # Генерация приватного ключа
    private_key = subprocess.check_output("wg genkey", shell=True).strip().decode()
    
    # Генерация публичного ключа из приватного
    public_key = subprocess.check_output(f"echo {private_key} | wg pubkey", shell=True).strip().decode()
    
    return private_key, public_key

private_key, public_key = generate_wireguard_keys()
print(private_key)
print(public_key)

def create_server_config(private_key, public_key, listen_port=51820):
    config = f"""
[Interface]
PrivateKey = {private_key}
Address = 10.0.0.1/24
ListenPort = {listen_port}

# Настройка для клиента
[Peer]
PublicKey = {public_key}
AllowedIPs = 10.0.0.2/32
"""
    with open("/opt/local/etc/wireguard/wg0.conf", "w") as f:
        f.write(config)
    print("Server configuration created at /opt/local/etc/wireguard/wg0.conf")


create_server_config(private_key, public_key)

def create_client_config(private_key, public_key, server_ip="server_ip", server_port=80):
    config = f"""
[Interface]
PrivateKey = {private_key}
Address = 10.0.0.2/24

[Peer]
PublicKey = {public_key}
Endpoint = {server_ip}:{server_port}
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
"""
    with open("/opt/local/etc/wireguard/client.conf", "w") as f:
        f.write(config)
    print("Client configuration created at client.conf")

# Генерация ключей для клиента
create_client_config(private_key, public_key, server_ip="172.67.75.195", server_port=80)

def start_wireguard_server():
    subprocess.run(["wg-quick", "up", "wg0"], check=True)
    print("WireGuard server started.")

def stop_wireguard_server():
    subprocess.run(["wg-quick", "down", "wg0"], check=True)
    print("WireGuard server stopped.")

def start_wireguard_client():
    subprocess.run(["wg-quick", "up", "client"], check=True)
    print("WireGuard client started.")

def stop_wireguard_client():
    subprocess.run(["wg-quick", "down", "client"], check=True)
    print("WireGuard client stopped.")


import string
import threading
from io import BytesIO
from OpenSSL import SSL
from PIL import Image, ImageTk
import os
import sys
import rsa
from requests import get
import socket
import random
from ipaddress import ip_address, AddressValueError


class ThreadedTask(threading.Thread):
    def __init__(self, target, args=None):
        super().__init__(target=target, args=(*args,), daemon=True) if args is not None \
            else super().__init__(target=target, daemon=True)
        self.start()


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_thumbnail(image, width):
    path = resource_path(r"assets/wallpapers/" + image + ".jpg")
    thumbnail = Image.open(path)
    width_percent = (width / float(thumbnail.size[0]))
    height_size = int((float(thumbnail.size[1]) * float(width_percent)))
    thumbnail = thumbnail.resize((width, height_size), Image.NEAREST)
    return ImageTk.PhotoImage(thumbnail)


def generate_pin():
    symbols = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>', '*', '(', ')', '<', '_', '-']
    length = random.randint(8, 16)
    password_ = []
    for i in range(length):
        ran = random.random()
        if ran <= 0.4:
            password_.append(random.choice(string.ascii_uppercase))
        elif ran <= 0.7:
            password_.append(random.choice(string.ascii_lowercase))
        elif ran <= 0.8:
            password_.append(random.choice(symbols))
        else:
            password_.append(random.choice('0123456789'))
    random.shuffle(password_)
    return "".join(password_)


#####


def get_available_port():
    # Get unused port starts From 4400
    port__ = 4400
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while 1:
        result = sock.connect_ex(('localhost', port__))
        if result != 0:
            sock.close()
            return port__
            break
        else:
            port__ += 1


def get_public_ip():
    # This Function Return Your Current Public IP Address
    return get('https://api.ipify.org').content.decode('utf8')


def is_valid_ip_address(ip):
    """Validates an ip address"""
    try:
        ip_address(ip)
        return True
    except (AddressValueError, ValueError):
        return False


def is_valid_host_name(host_name):
    if host_name == 'localhost':
        return True


def is_valid_host(host):
    return True if is_valid_ip_address(host) or is_valid_host_name(host) else False


"""____Encryption____"""


def generate_rsa_key(length=1024):
    # generate public and private keys with rsa.newkeys method,this method accepts key length as its parameter
    return rsa.newkeys(length)


def get_rsa_key():
    public_key, private_key = generate_rsa_key()
    n, e = public_key.__getstate__()
    key_msg = (str(n) + ", " + str(e))
    return key_msg, private_key


def extract_public_key(key_msg):
    n, e = key_msg.split(", ")
    key = rsa.PublicKey(int(n), int(e))
    return key


def encrypt_msg(message, public_key):
    """This Function chops message into 117-byte chunks then encrypt it using provided public_keyA. Because rsa 1024-bit
     key is 128 bytes long. Because of overhead, it can only encode 117 bytes at a time. So """
    encrypted_message = []
    for n in range(0, len(message), 117):
        part = message[n:n + 117]
        encrypted_message.append(rsa.encrypt(part.encode(), public_key))
    return b''.join(encrypted_message)


def decrypt_msg(encrypted_message, private_key):
    decrypted_message = []
    for n in range(0, len(encrypted_message), 128):
        part = encrypted_message[n:n + 128]
        decrypted_message.append(rsa.decrypt(part, private_key).decode())
    return "".join(decrypted_message)


def convert_to_binary_data(filename):
    """Converts image or file data to binary format"""
    file = open(filename, mode='rb')
    blob_data = file.read()
    return blob_data


def convert_binary_data_to_image(blob_data):
    """Converts from binary format to image or file data"""
    image = Image.open(BytesIO(blob_data))
    image.show()


def test_send_image():
    a = convert_to_binary_data(r"assets/clear_button.png")
    convert_binary_data_to_image(a)


def test_send_receive_encrypted_image():
    a = convert_to_binary_data(r"assets/clear_button.png")
    pub, pri = generate_rsa_key()

    encrypted_message = []
    for n in range(0, len(a), 117):
        part = a[n:n + 117]
        encrypted_message.append(rsa.encrypt(part, pub))
    encrypted_message = b''.join(encrypted_message)

    decrypted_message = []
    for n in range(0, len(encrypted_message), 128):
        part = encrypted_message[n:n + 128]
        decrypted_message.append(rsa.decrypt(part, pri))
    decrypted_message = b"".join(decrypted_message)

    convert_binary_data_to_image(decrypted_message)


def load_context():
    context = SSL.Context(SSL.TLSv1_2_METHOD)
    context.use_certificate_file(resource_path(r"assets/certificate.pem"))
    context.use_privatekey_file(resource_path(r"assets/key.pem"))
    return context

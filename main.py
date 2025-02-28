import socket
import os

def rmdir(path):
    if os.listdir(path) == []:
        try:
            os.rmdir(path)
            return 'deleted'
        except OSError:
            return 'error'
    else:
        try:
            for file in os.listdir(path):
                os.remove(path + '/' + file)
            os.rmdir(path)
            return 'deleted'
        except:
            return 'error'


def process(req):
    global users
    user = users[0]
    homedir = '/home/alisa/PycharmProjects/ftp/users/'
    if req.startswith('GET /pwd/'):
        with open('/home/alisa/PycharmProjects/ftp/log.txt', 'w') as logs:
            logs.write('pwd ' + user)
        return os.getcwd()
    elif req.startswith('GET /ls/'):
        with open('/home/alisa/PycharmProjects/ftp/log.txt', 'w') as logs:
            logs.write('ls ' + user)
        return '; '.join(os.listdir())
    elif req.startswith('GET /mkdir/'):
        name = req.split()[1][7:]
        try:
            os.mkdir(homedir + name)
            with open('/home/alisa/PycharmProjects/ftp/log.txt', 'w') as logs:
                logs.write('mkdir ' + name + ' ' + user)
            return 'created'
        except OSError:
            return 'error'
    elif req.startswith('GET /rmdir/'):
        name = req.split()[1][7:]
        try:
            resp = rmdir(homedir + name)
            if resp != 'error':
                with open('/home/alisa/PycharmProjects/ftp/log.txt', 'w') as logs:
                    logs.write('rmdir ' + name + ' ' + user)
            return resp
        except OSError:
            return 'error'
    elif req.startswith('GET /delete/'):
        name = req.split()[1][7:]
        try:
            os.remove(homedir + name)
            with open('/home/alisa/PycharmProjects/ftp/log.txt', 'w') as logs:
                logs.write('delete ' + name + ' ' + user)
            return 'deleted'
        except OSError:
            return 'error'
    elif req.startswith('GET /rename/'):
        data = req.split()[1][7:]
        prev = data.split('/')[0].replace('\\', '/')
        now = data.split('/')[1].replace('\\', '/')
        try:
            os.rename(homedir + prev, homedir + now)
            with open('/home/alisa/PycharmProjects/ftp/log.txt', 'w') as logs:
                logs.write('rename ' + prev + ' ' + now + ' ' + user)
            return 'renamed'
        except OSError:
            return 'error'
    elif req.startswith('GET /receive/'):
        data = req.split()[1][9:]
        try:
            with open(homedir+data, 'r') as file:
                with open('/home/alisa/PycharmProjects/ftp/log.txt', 'w') as logs:
                    logs.write('receive ' + data + ' ' + user)
                return file.read()
        except OSError as e:
            print(e)
            return 'error'
    elif req.startswith('GET /stop/'):
        conn.close()
    else:
        return 'bad request'

PORT = 9092
users = ['alisa']
sock = socket.socket()
sock.bind(('', PORT))
sock.listen()

while True:
    print("Слушаем порт", PORT)
    conn, addr = sock.accept()
    print(addr)

    request = conn.recv(1024).decode()
    print(request)

    response = process(request)
    conn.send(response.encode())
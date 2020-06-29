package main

import(
  "net"
  "log"
  "bufio"
  "io"
  "io/ioutil"
  "encoding/binary"
)

var SECRET [][]byte = [][]byte{
  []byte{0x41, 0x49, 0x53, 0x33, 0x7b, 0x4e, 0x4f, 0x7d},
  []byte{0x78, 0x53, 0x45, 0x43, 0x52, 0x45, 0x54, 0x78},
}

func main(){
  // socket server
  server, err := net.Listen("tcp", ":8080")
  if err != nil {
    log.Println("Fail to start server, %s", err)
    return
  }

  log.Println("Wait for connection...")

  times := 0
  for true {
    conn, err := server.Accept()
    if err != nil || conn == nil {
      log.Println("Fail to connect, %s", err)
      continue
    }
    defer conn.Close()

    log.Println("Connected from ", conn.RemoteAddr())
    go handler(conn, SECRET[times%2])
    times++
  }
}

func handler(conn net.Conn, secret []byte){
  // receive secret_1
  cr := ccReader{bufio.NewReader(conn)}
  secret_1, _ := cr.ReadBytes(8)

  // send secret_2
  XOR(secret, secret_1)
  conn.Write(secret_1)

  // receive files
  for i:=0; i<5; i++ {
    if err := storefile(cr, secret); err == io.EOF {
      log.Println(conn.RemoteAddr(), " disconnected.")
      return
    }
  }
}

func storefile(cr ccReader, secret []byte) error {
  // receive filename
  recvlen, err := cr.ReadBytes(4)
  if err != nil {
    return err
  }
  XOR(secret, recvlen)

  filename := make([]byte, binary.LittleEndian.Uint32(recvlen))
  if _, err := io.ReadFull(cr.r, filename); err != nil {
    return err
  }
  XOR(secret, filename)

  // receive file
  recvlen, _ = cr.ReadBytes(4)
  XOR(secret, recvlen)

  file := make([]byte, binary.LittleEndian.Uint32(recvlen))
  if _, err := io.ReadFull(cr.r, file); err != nil {
    return err
  }
  XOR(secret, file)

  if err := ioutil.WriteFile(string(filename), file, 0644); err != nil {
    return err
  }

  return nil
}

func XOR(key, text []byte){
  for i:=0; i<len(text); i++ {
    text[i] = text[i] ^ key[i%len(key)]
  }
}

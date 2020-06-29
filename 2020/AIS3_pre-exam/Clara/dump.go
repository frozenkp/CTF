package main

import(
  "bufio"
  "os"
  "log"
  "encoding/binary"
)

func main(){
  file, _ := os.Open("Clara.dump")
  defer file.Close()
  r := bufio.NewReader(file)

  key_1 := make([]byte, 8)
  r.Read(key_1)
  key := make([]byte, 8)
  r.Read(key)
  XOR([]byte{kay_1, key)
  log.Println("key =", string(key))


  for true {
    err := readFile(r, key)
    if err != nil {
      log.Fatal(err)
    }
  }
}

func readFile(r *bufio.Reader, key []byte) error {
  // filename
  size := make([]byte, 4)
  if _, err := r.Read(size); err != nil {return err}
  XOR(key, size)

  filename := make([]byte, binary.LittleEndian.Uint32(size))
  if _, err := r.Read(filename); err != nil {return err}
  XOR(key, filename)
  log.Printf("Filename: %s...", string(filename))

  // file content
  if _, err := r.Read(size); err != nil {return err}
  XOR(key, size)

  content := make([]byte, binary.LittleEndian.Uint32(size))
  if _, err := r.Read(content); err != nil {return err}
  XOR(key, content)

  if err := ioutil.WriteFile(string(filename), content, 0644) {return err}
  log.Println("[SAVED]")

  return nil
}

func XOR(key, text []byte){
  for i:=0; i<len(text); i++ {
    text[i] = text[i] ^ key[i%len(key)]
  }
}

package main

import(
  "bufio"
  "log"
  "encoding/binary"
  "io"
)

type ccReader struct {
  r   *bufio.Reader
}

func (cr ccReader) ReadByte() byte {
  b, err := cr.r.ReadByte()
  if err != nil {
    log.Fatal("Read Failed.")
  }
  return b
}

func (cr ccReader) ReadBytes(times int) ([]byte, error) {
  bytes := make([]byte, 0)
  for i:=0; i<times; i++ {
    b, err := cr.r.ReadByte()
    if err != nil {
      return []byte{}, err
    }
    bytes = append(bytes, b)
  }
  return bytes, nil
}

func (cr ccReader) ReadInt() uint32 {
  i := make([]byte, 4)
  if _, err := cr.r.Read(i); err != nil {
    log.Fatal("Read Failed.")
  }
  return binary.LittleEndian.Uint32(i)
}

func (cr ccReader) ReadStr() string {
  // length
  length := cr.ReadInt()

  // string
  str := make([]byte, length)
  if _, err := io.ReadFull(cr.r, str); err != nil {
    log.Fatal("Read Failed.")
  }

  return string(str)
}

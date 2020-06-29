package main

import(
  "fmt"
  "time"
  "syscall"
  "crypto/sha256"
  "math/rand"
)

func main(){
  rand.Seed(time.Now().UnixNano())

  //_, usrStart := getSysTime()

  flag := []byte("AIS3{A1r1ght_U_4r3_my_3n3nnies}")
  var guess string

  fmt.Printf("Flag: ")
  fmt.Scanf("%s", &guess)

  win := true
  guessByte := make([]byte, len(flag))
  copy(guessByte, []byte(guess))

  execTime := 0
  for i:=0; i<len(flag) && win; i++ {
    execTime += rand.Int()%5 + 11
    guessSum := hashNTimes(guessByte[:i+1], 20000)
    flagSum := hashNTimes(flag[:i+1], 20000)
    for j:=0; j<32; j++ {
      if guessSum[j] != flagSum[j] {
        win = false
        break
      }
    }
  }

  //_, usrEnd := getSysTime()

  if win {
    fmt.Println("Oh, you win. QQ")
  } else {
    //fmt.Printf("Haha, you lose in %v milliseconds.\n", sysEnd.Add(usrEnd.Sub(usrStart)).Sub(sysStart).Milliseconds())
    //fmt.Printf("Haha, you lose in %v milliseconds.\n", usrEnd.Sub(usrStart).Milliseconds())
    fmt.Printf("Haha, you lose in %d milliseconds.\n", execTime)
  }
}

func hashNTimes(text []byte, n int) [32]byte {
  hash := sha256.Sum256(text)
  tmphash := make([]byte, 32)
  for i:=0; i<n-1; i++ {
    copy(tmphash, hash[:])
    hash = sha256.Sum256(tmphash)
  }
  return hash
}

func getSysTime() (time.Time, time.Time) {
  var r syscall.Rusage
  syscall.Getrusage(syscall.RUSAGE_SELF, &r)

  sysTime := time.Unix(r.Stime.Sec, int64(r.Stime.Usec*1000))
  usrTime := time.Unix(r.Utime.Sec, int64(r.Utime.Usec*1000))

  return sysTime, usrTime
}

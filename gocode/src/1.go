package main

import (
    "fmt"
    "net"
)

func main() {

    var localaddr net.TCPAddr
    var remoteaddr net.TCPAddr
    localaddr.IP = net.ParseIP("192.168.0.109")
    localaddr.Port = 0
    remoteaddr.IP = net.ParseIP("192.168.0.1")
    remoteaddr.Port = 80

    if localaddr.IP == nil || remoteaddr.IP == nil {
        fmt.Println("error")
    }

    if _, err := net.DialTCP("tcp", &localaddr, &remoteaddr); err != nil {
        fmt.Println(err)
    }

    fmt.Println("End")

}

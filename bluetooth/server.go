package main

import (
	"bytes"
	"compress/gzip"
	b64 "encoding/base64"
	"fmt"
	"io/ioutil"
	"log"
	"math"
	"os/exec"
	"strings"
	"time"

	"github.com/paypal/gatt"
	"github.com/paypal/gatt/linux/cmd"
)

var serviceUUID = "eabea763-8144-4652-a831-82fc9d4e645c"
var writeCharacteristicUUID = "2e7a6c4b-b70e-49b6-acf9-2be297ac29e9"
var notifyCharacteristicUUID = "25db62b2-00d3-4df9-b7e0-125623d67008"

var chunkStartHeader = "---start-"
var chunkEndHeader = "---end-"

var chunkSize = 20.0
var commandChunks = []string{}
var hasIncomingPacket = false

// Command container
var Command string

// DefaultServerOptions options
var DefaultServerOptions = []gatt.Option{
	gatt.LnxMaxConnections(1),
	gatt.LnxDeviceID(-1, true),
	gatt.LnxSetAdvertisingParameters(&cmd.LESetAdvertisingParameters{
		AdvertisingIntervalMin: 0x00f4,
		AdvertisingIntervalMax: 0x00f4,
		AdvertisingChannelMap:  0x7,
	}),
}

func printPackets(input string, chunkSize float64, n gatt.Notifier) {
	length := len(input)
	chunks := math.Ceil(float64(length) / chunkSize)
	for i := 0; i < int(chunks); i++ {
		chunkSizeInt := int(chunkSize)
		start := i * chunkSizeInt
		end := int(math.Min(float64(length), float64(start)+chunkSize))
		chunk := input[start:end]
		fmt.Fprintf(n, "%s", chunk)
	}
}

func compress(input string) string {
	var buffer bytes.Buffer
	gz := gzip.NewWriter(&buffer)
	if _, err := gz.Write([]byte(input)); err != nil {
		return string(err.Error())
	}
	if err := gz.Flush(); err != nil {
		return string(err.Error())
	}
	if err := gz.Close(); err != nil {
		return string(err.Error())
	}
	return b64.StdEncoding.EncodeToString(buffer.Bytes())
}

func mergePackets(packet string) {
	if strings.HasPrefix(packet, chunkStartHeader) {
		commandChunks = []string{}
		hasIncomingPacket = true
	} else if strings.HasPrefix(packet, chunkEndHeader) {
		hasIncomingPacket = false
		Command = strings.Join(commandChunks, "")
		log.Println("Merged command: ", string(Command))
	} else if hasIncomingPacket {
		commandChunks = append(commandChunks, packet)
	}
}

// NewService : create new bluetooth service
func NewService() *gatt.Service {
	noopDelay := 250 * time.Millisecond
	Command = ""

	s := gatt.NewService(gatt.MustParseUUID(serviceUUID))
	s.AddCharacteristic(gatt.MustParseUUID(writeCharacteristicUUID)).HandleWriteFunc(
		func(r gatt.Request, data []byte) (status byte) {
			log.Println("Data received: ", string(data))
			mergePackets(string(data))
			return gatt.StatusSuccess
		})

	s.AddCharacteristic(gatt.MustParseUUID(notifyCharacteristicUUID)).HandleNotifyFunc(
		func(r gatt.Request, n gatt.Notifier) {
			for !n.Done() {

				if len(Command) > 0 {
					log.Println("Execute: ", string(Command))
					out, err := exec.Command("/bin/sh", "-c", Command).Output()
					Command = ""
					outString := ""
					// Errors are raw string, valid output is compressed string in base64 format
					if err != nil {
						outString = string(err.Error())
					} else {
						outString = compress(string(out))
					}
					log.Println("Output: ", outString)
					fmt.Fprintf(n, "---start-%d", len(outString))
					printPackets(outString, chunkSize, n)
					fmt.Fprintf(n, "---end-%d", len(outString))
					log.Println("Printing packets...")
				}

				log.Println("NOOP")
				time.Sleep(noopDelay)
			}
		})

	return s
}

func main() {
	deviceName, err := ioutil.ReadFile("/home/pi/device_name")
	if err != nil {
		fmt.Print(err)
	}
	d, err := gatt.NewDevice(DefaultServerOptions...)
	if err != nil {
		log.Fatalf("Failed to open device, err: %s", err)
	}

	d.Handle(
		gatt.CentralConnected(func(c gatt.Central) { fmt.Printf("Connect to %s\n", string(deviceName)) }),
		gatt.CentralDisconnected(func(c gatt.Central) { fmt.Printf("Disconnect device %s\n ", string(deviceName)) }),
	)

	onStateChanged := func(d gatt.Device, s gatt.State) {
		fmt.Printf("State: %s\n", s)
		switch s {
		case gatt.StatePoweredOn:
			s1 := NewService()
			d.AddService(s1)
			d.AdvertiseNameAndServices(string(deviceName), []gatt.UUID{s1.UUID()})
		default:
		}
	}

	d.Init(onStateChanged)
	select {}
}

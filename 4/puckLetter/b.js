const noble = require('@abandonware/noble');
const WebSocket = require('ws');

const ws = new WebSocket('ws://localhost:8000');

receivedFalse = true
receivedTrue = true

const NAME = "Puck.js fb35";
const PUCKLETTER = "b"

let COMMAND = '\x03\x10function press(){LED2.write(1), print("true")};\n\x10function released(){LED2.write(0)};\n\x10setWatch(press, BTN, {edge: "rising", repeat: true, debounce: 1});\n\x10setWatch(released, BTN, {edge: "falling", repeat: true, debounce: 1});\n';

function sendData() {
    ws.send('letter:' + PUCKLETTER);
}

let btDevice;
let txCharacteristic;
let rxCharacteristic;

noble.on('stateChange', function (state) {
    console.log("Noble: stateChange -> " + state);
    if (state === "poweredOn")
        noble.startScanning([], true);
});

let foundDevice = false;
noble.on('discover', function (dev) {
    if (foundDevice) return;
    if (dev.advertisement.localName) console.log("Found device: ", dev.advertisement.localName);
    if (dev.advertisement.localName !== NAME) return;
    foundDevice = true;
    noble.stopScanning();
    connect(dev, function () {
        write(COMMAND, function () {
            console.log("All set, click !")
        });
    });
});

function connect(dev, callback) {
    btDevice = dev
    console.log("BT> Connecting");
    btDevice.on('disconnect', function () {
        console.log("Disconnected");
        foundDevice = false;
        noble.startScanning([], true);
    });
    btDevice.connect(function (error) {
        if (error) {
            console.log("BT> ERROR Connecting", error);
            btDevice = undefined;
            return;
        }
        console.log("BT> Connected");
        btDevice.discoverAllServicesAndCharacteristics(function (error, services, characteristics) {
            function findByUUID(list, uuid) {
                for (let i = 0; i < list.length; i++)
                    if (list[i].uuid === uuid) return list[i];
                return undefined;
            }

            let btUARTService = findByUUID(services, "6e400001b5a3f393e0a9e50e24dcca9e");
            txCharacteristic = findByUUID(characteristics, "6e400002b5a3f393e0a9e50e24dcca9e");
            rxCharacteristic = findByUUID(characteristics, "6e400003b5a3f393e0a9e50e24dcca9e");
            if (error || !btUARTService || !txCharacteristic || !rxCharacteristic) {
                console.log("BT> ERROR getting services/characteristics");
                console.log("Service " + btUARTService);
                console.log("TX " + txCharacteristic);
                console.log("RX " + rxCharacteristic);
                btDevice.disconnect();
                txCharacteristic = undefined;
                rxCharacteristic = undefined;
                btDevice = undefined;
                return openCallback();
            }

            rxCharacteristic.on('data', function (data) {
                let s = "";
                for (let i = 0; i < data.length; i++) s += String.fromCharCode(data[i]);
                if (s.includes("true") && receivedTrue) {
                    receivedTrue = false
                    sendData()
                    setTimeout(() => {
                        receivedTrue = true
                    }, 200)
                } else if (s.includes("false") && receivedFalse) {
                    receivedFalse = false
                    setTimeout(() => {
                        receivedFalse = true
                    }, 200)
                }
            });
            rxCharacteristic.subscribe(function () {
                callback();
            });
        });
    });
}

function write(data, callback) {
    function writeAgain() {
        if (!data.length) return callback();
        let d = data.substr(0, 20);
        data = data.substr(20);
        let buf = Buffer.alloc(d.length);
        for (let i = 0; i < buf.length; i++)
            buf.writeUInt8(d.charCodeAt(i), i);
        txCharacteristic.write(buf, false, writeAgain);
    }

    writeAgain();
    console.log("Analysing data")
}
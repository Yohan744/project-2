const noble = require('@abandonware/noble');
const WebSocket = require('ws');

let removeLetterAtBeginning = false

const ws = new WebSocket('ws://localhost:8000');

const devices = [
    "c7:f8:6b:2d:52:46", "c1:68:14:e8:fb:35", "c3:26:d7:38:30:25", "d9:0e:5e:8a:76:f6", "ed:0d:64:c9:a2:e5", "ef:2d:7d:bc:69:02", "e4:8d:e2:32:6a:7e"
];

const tabDevices = {
    "c7:f8:6b:2d:52:46": "a", // 5246
    "c1:68:14:e8:fb:35": "n", // FB35 --- f5aba2a6-cd36-11ec-9d64-0242ac120002
    "c3:26:d7:38:30:25": "c", // 3025
    "d9:0e:5e:8a:76:f6": "r", // 76F6
    "ed:0d:64:c9:a2:e5": "e", // A2E5
    "ef:2d:7d:bc:69:02": "i", // 6902
    "e4:8d:e2:32:6a:7e": "l" // 6A7E
}

const tabDevicesKeys = Object.keys(tabDevices)

let lastAdvertising = {};

function onDeviceChanged(address, data) {
    let findLetter = tabDevicesKeys.indexOf(address)
    let letter = Object.values(tabDevices)[findLetter]
    console.log(letter)
    ws.send('letter:' + letter);
}

function onDiscovery(peripheral) {
    if (devices.indexOf(peripheral.address) < 0) return;
    if (!peripheral.advertisement.manufacturerData ||
        peripheral.advertisement.manufacturerData[0] !== 0x90 ||
        peripheral.advertisement.manufacturerData[1] !== 0x05) return;
    let data = peripheral.advertisement.manufacturerData.slice(2);
    //console.log(peripheral.advertisement.serviceUuids)
    if (lastAdvertising[peripheral.address] != data.toString())
        onDeviceChanged(peripheral.address, data);
    lastAdvertising[peripheral.address] = data;
}

noble.on('stateChange', function (state) {
    if (state !== "poweredOn") return;
    console.log("Starting scan...");
    let serviceUUIDs = []
    let allowDuplicates = true

    noble.startScanning(serviceUUIDs, allowDuplicates)
});
noble.on('discover', onDiscovery);
noble.on('scanStart', function () {
    console.log("Scanning started.");
});
noble.on('scanStop', function () {
    console.log("Scanning stopped.");
});
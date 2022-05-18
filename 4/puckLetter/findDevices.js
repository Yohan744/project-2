const noble = require('@abandonware/noble');

function onDiscovery(peripheral) {
    // peripheral.rssi                             - signal strength
    // peripheral.address                          - MAC address
    // peripheral.advertisement.localName          - device's name
    // peripheral.advertisement.manufacturerData   - manufacturer-specific data
    // peripheral.advertisement.serviceData        - normal advertisement service data
    // ignore devices with no manufacturer data
    if (!peripheral.advertisement.manufacturerData) return;
    // output what we have
    console.log(
        peripheral.address,
        JSON.stringify(peripheral.advertisement.localName),
        JSON.stringify(peripheral.advertisement.manufacturerData)
    );
}

noble.on('stateChange', function (state) {
    if (state != "poweredOn") return;
    console.log("Starting scan...");
     noble.startScanning(["6e400001b5a3f393e0a9e50e24dcca9e"], false)
});
noble.on('discover', onDiscovery);
noble.on('scanStart', function () {
    console.log("Scanning started.");
});
noble.on('scanStop', function () {
    console.log("Scanning stopped.");
});
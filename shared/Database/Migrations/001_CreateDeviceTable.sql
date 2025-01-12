
CREATE TABLE IF NOT EXISTS `ConnectedDevice` 
( 
    `ID` INTEGER PRIMARY KEY,
    `FriendlyName` TEXT, 
    `DeviceName` TEXT, 
    `IPAddress` TEXT NOT NULL, 
    `MACAddress` TEXT NOT NULL UNIQUE, 
    `Manufacturer` TEXT, 
    `NotifyOnConnect` INTEGER NOT NULL DEFAULT 1,
    `LastConnectedDate` INTEGER,
    `DeviceType` INTEGER NOT NULL DEFAULT 0
)
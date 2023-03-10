CREATE TABLE `ConnectedDevice` 
( 
    `FriendlyName` TEXT, 
    `DeviceName` TEXT, 
    `IPAddress` TEXT NOT NULL, 
    `MACAddress` TEXT NOT NULL UNIQUE, 
    `VendorName` TEXT, 
    `NotifyOnConnect` INTEGER NOT NULL DEFAULT 1,
    `LastConnectedDate` INTEGER 
)

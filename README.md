# NetworkMonitor
A tool to monitor devices connected to a network.
---
Planned functionality:
- The application will periodically search for devices connected to the network the application is running on.
- When a new device connects, it will save information about the device to a database: IP Address, Mac Address, number of times connected, last date connected, Device name (if available)
- A user can update the database entries with a user-provided Device name if they know which device just connected to their network (for example, the Device name may be 'GOOGLE PIXEL 6' but they could specify that the device is actually "Mom's Cell Phone" etc).
- From there, there are a few possibilities.
- - When a specific device connects, a specific command could execute (Amazon Alexa Skill to activate a plug when you connect to your network, etc)
- - The application could email you a notification when a new device connects (useful if you have an open Wi-Fi, or for security reasons)
- - - Ideally the user could reply to the email with the user-specified device name so they wouldn't need to log into an application or manually update the database.

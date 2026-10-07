### 5.1 Subsystem communication


```mermaid
flowchart LR
    APP["Mission Application"]
    SB["cFE Software Bus"]
    IFACE["Subsystem Interface Application"]
    LIB["Subsystem Library"]
    PROTOCOL["Protocol Adapter"]
    DRIVER["Platform Driver"]
    DEVICE["External Subsystem"]

    APP <--> SB
    SB <--> IFACE
    IFACE <--> LIB
    LIB <--> PROTOCOL
    PROTOCOL <--> DRIVER
    DRIVER <--> DEVICE
```

This architecture allows an implementation to use FreeRTOS drivers on the flight OBC and Linux device files or mocked transports during development without changing the mission application.

CSP/PUS is appropriate when a remote subsystem is an intelligent embedded node. It remains below the mission-facing subsystem API.

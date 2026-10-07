### 2.1 Layered Architecture

```mermaid
flowchart TB
    subgraph SOFTWARE["Flight Software"]
        APPS["Mission Applications and Services"]
        CFE["cFE-Based Core"]
        LIBS["Subsystem and Communication Libraries"]
    end

    subgraph ABSTRACTION["Platform Abstraction"]
        OSAL["Operating System Abstraction Layer"]
        PSP["Platform Support Package"]
        HAL["Hardware Abstraction Layer"]
        BSP["Board Support Package"]
    end

    subgraph RUNTIME["Runtime"]
        RTOS["FreeRTOS"]
        DRIVERS["Device Drivers"]
    end

    subgraph HARDWARE["OBC Hardware"]
        CPU["Single-Core CPU"]
        RAM["RAM"]
        NVM["Non-Volatile Memory"]
        IO["CAN, UART, SPI, I2C and Timers"]
        WDT["Hardware Watchdog"]
    end

    APPS --> CFE
    APPS --> LIBS

    CFE --> OSAL
    CFE --> PSP
    LIBS --> HAL

    OSAL --> RTOS
    PSP --> BSP
    HAL --> BSP

    RTOS --> BSP
    BSP --> DRIVERS

    DRIVERS --> CPU
    DRIVERS --> RAM
    DRIVERS --> NVM
    DRIVERS --> IO
    DRIVERS --> WDT
```

The diagram is logical rather than hardware-specific. The Propulsion Interface may use CSP over CAN in one implementation and a direct UART or CAN protocol in another. The Propulsion Application remains unchanged because the transport and protocol implementation are hidden below the Software Bus interface.


From a CDH point of view : 

```mermaid
flowchart LR
    GROUND["Ground Segment"]

    subgraph CORE["OBC Internal Software"]
        CI["Command Ingest"]
        TO["Telemetry Output"]
        SB["cFE Software Bus"]
    end

    subgraph INTERFACES["Subsystem Interface Applications"]
        AOCS_IF["AOCS Device Interface"]
        PROP_IF["Propulsion Interface"]
        EPS_IF["Power-System Interface"]
    end

    subgraph ADAPTERS["Protocol and Transport Adapters"]
        PUS["PUS-Compatible Gateway"]
        CSP["I2C BUS"]
        CAN["CAN or CANopen Adapter"]
        SERIAL["UART or RS-422 Adapter"]
    end

    subgraph DEVICES["External Subsystems"]
        AOCS_DEV["Sensors and Actuators"]
        PROP_ECU["Propulsion Controller"]
        EPS["Power System"]
        PAYLOAD_DEV["Payload Electronics"]
    end

    GROUND <--> PUS

    PUS --> CI
    TO --> PUS

    CI --> SB
    SB --> TO

    SB <--> AOCS_IF
    SB <--> PROP_IF
    SB <--> EPS_IF

    AOCS_IF <--> CSP
    PROP_IF <--> SERIAL
    EPS_IF <--> CAN

    CSP <--> AOCS_DEV
    CSP <--> PROP_ECU
    CAN <--> EPS
    SERIAL <--> PAYLOAD_DEV
```

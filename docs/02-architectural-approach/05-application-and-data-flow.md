### 2.5 Application and Data Flow

```mermaid
flowchart LR
    subgraph INTERFACES["Subsystem Interface Applications"]
        IMU["IMU Interface"]
        RW["Reaction Wheel Interface"]
        PROP_IF["Propulsion Interface"]
    end

    subgraph BUS["cFE Software Bus"]
        SB["Typed Commands and Telemetry"]
    end

    subgraph CONTROL["AOCS and Propulsion App"]
        EST["State Estimation"]
        CTRL["Control"]
        PROP_SEQ["Propulsion Sequencing"]
    end

    subgraph MISSION["Mission and Data Handling"]
        MODE["Mode Manager"]
        SCH["Mission Scheduler"]
        HM["Health Monitoring"]
        STORAGE["Storage Manager"]
        DOWNLINK["Downlink Manager"]
    end

    IMU --> SB
    PROP_IF --> SB
    RW --> SB

    SB --> EST
    EST --> CTRL

    SB --> PROP_SEQ
    PROP_SEQ --> SB

    MODE <--> SB
    SCH <--> SB
    HM <--> SB
    STORAGE <--> SB
    DOWNLINK <--> SB

    SB --> RW
    SB --> PROP_IF
```

An application does not need to know the implementation details of another application.

For example:

1. The AOCS Application publishes a reaction-wheel torque request.
2. The Reaction Wheel Interface subscribes to that message.
3. The interface converts the request into the wheel-specific command.
4. The command is transferred over the selected physical interface.
5. Reaction-wheel telemetry is decoded.
6. The interface publishes normalised telemetry on the Software Bus.
7. AOCS, Health Monitoring and Telemetry Output may subscribe to the same telemetry message.

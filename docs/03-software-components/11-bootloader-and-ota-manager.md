### 3.11 Bootloader and OTA Manager

The complete boot, recovery and rollback strategy is defined in Section 1.4. This section only defines the component.

The **bootloader**:

- Runs before FreeRTOS and cFE
- Selects and validates image
- Starts it
- Performs rollback selection after failed boots.

The **Golden Recovery Image**: 

- Provides minimal ground communication
- Provides essential storage and repair commands
- Receives replacement images
- Safes the spacecraft as required

The **Update Manager application** runs inside the operational or recovery image and is responsible for:

- Starting an update session
- Selecting the inactive slot or operational image area
- Receiving file blocks
- Validating block sequence and offset
- Supporting transfer resume 
- Checking complete-image integrity (xxhash)
- Recording build and version metadata
- Reporting update status
- wait for controlled activation 

The Update Manager cannot overwrite the currently executing validated image in the A/B configuration.

```c
 const uint32_t image_address =
    (boot_selection == BOOT_IMAGE_APP)
        ? APP_IMAGE_ADDRESS`
        : GOLDEN_IMAGE_ADDRESS;

if (image_is_valid(image_address, image_size)) {
    run_image(image_address);
}
```

A commit ID may be included in the image metadata for traceability. A cryptographic hash is used for integrity.

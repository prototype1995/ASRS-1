## asrs library

### asrsDB.py
It manages the database with two TABLES - current and record. Here 'current' contains the current database status and 'record' contains the whole history of the card storage and retrieval.
### asrsMotor.py
It controls the actuators ( 2 Stepper Motors and Solenoid ) directly using RPi.
### asrsOCR.py
It captures photos and deduces the OCR from the photos captured.
### asrsQRcode.py
It contains QR Code generation, printer detection and demo printer check.
### asrsSlots.py
It contains the unique ID & status of a card slot and date and time of card storage and retrieval.


### TODO:
- [ ] Add logging
- [ ] Create config file to store all defaults
- [ ] server.py - move init statements to main()
- [x] server.py - Change gpio pins
- [x] asrsMotor.py - Change GPIO.BCM to GPIO.BOARD
- [ ] Fix issue with retrieval
- [ ] Update for Rpi as AP
- [ ] Clean and modularize code
- [ ] Add init system checking - hardware check, network check, connection check
- [ ] asrsDB.py - Save pictures in a seperate directory
- [ ] asrsDB.py - Implement records table
- [ ] asrsQRcode.py - detect_printer() write udev rules

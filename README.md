## asrs library

### asrsDB.py
It manages the database with three TABLES - current, record and ocr_table. Here 'current' contains the current database status and 'record' contains the whole history of the item storage and retrieval and 'ocr_table' contains the OCR detected values from a card.
### asrsMotor.py
It controls the actuators ( 2 Stepper Motors and Solenoid ) directly using RPi.
### asrsOCR.py
It captures photos and deduces the OCR from the photos captured.
### asrsQRcode.py
It contains QR Code generation, printer detection and demo printer check.
### asrsSlots.py
It contains the unique ID & status of a card slot and date and time of card storage and retrieval.


### TODO:
- [x] Add logging
- [x] Create config file to store all defaults
- [x] server.py - move init statements to main()
- [x] server.py - Change gpio pins
- [x] asrsMotor.py - Change GPIO.BCM to GPIO.BOARD
- [x] Fix issue with retrieval
- [x] Update for Rpi as AP
- [x] Clean and modularize code
- [x] Add init system checking - hardware check, network check, connection check
- [x] asrsDB.py - Save pictures in a seperate directory
- [x] asrsDB.py - Implement records table
- [x] asrsQRcode.py - detect_printer() write udev rules

# Description
- create a repo house packages i use a lot
- when appropriate each package should have its own cli entry point as a separate script.
- 
## proposed packages
- Crypto
- Logging
- TK Live logging
- Network Manager
- 


Chat history
ChatGPT
ChatGPT

Explore GPTs
Today
IpFieldWidget Requirements Draft


Python IP Library Integration
Type Cast for ushort
Yesterday
C# Managed Exception Event System
Tkinter Base
Previous 7 Days
Encrypt Decrypt Package Module
Python Tkinter GUI Tutorial
Fotric Camera Comm Port
Previous 30 Days
Port Randomizer in C#
February
Run Python script in terminal.
Migration Issue Assistance Needed
ViperVision Release notes
Django Personal Website Discussion
Sass HTML Stephanie Quadrants
January
Build Your Own Email Server
2023
Reddit Post Help
Fantasy Book Excerpts
Django with htmx Integration
Setting User Permissions
Securely Handling User-Uploaded Images
Exclude "Not required" from copy.
Migration Types & Examples
Update Bootstrap 2/3 Nav
ViperVision Release Info
Code Directory Structure
Integrating Cryptography Changes
Django C# API Endpoint.
LicenseProcessor
Add Team workspace
Collaborate on a Team plan

User
Jarrod Burns

Close sidebar
ChatGPT 4

User
Let work on drafting the requirments fo my IPManagerWidget and my OctletWidget, this is the rough draft so far 

# [ ].[ ].[ ].[ ] requirements
thesde all need to be more clear abouyt their intent and organized

- [ ] Only valid digits in range allowed 1 - 254
- [ ] '.' should advance to the next octlet
- [ ] enter key should advance
- [ ] Essentially period and enter should function exactly like tab does including advancing to the set button
- [ ] 3 digits should advance
- [ ] 2 digets should advance if no other number can be logically added to make a valid ocltlet
- [ ] click should clear but return the old value if focus is lost without any changes
- [ ] click and click away remembers old input but defauts to og ip if needed
- [ ] set button disabled if ip is taken or current
- [ ] backspace on an empty box should go to the previous field
- [ ] delete should delete forward




### IPManagerWidget Requirements

1. **Field Composition**: Comprises four subfields (OctletWidgets) representing the octets of an IP address, separated by static labels displaying '.'.

2. **Navigation**:
   - **Tab Key**: Advances to the next octet. If the last octet is focused, it advances to the set button.
   - **Shift+Tab Key**: Moves focus to the previous octet or from the first octet back to another designated UI element.
   - **Enter Key**: Functions identically to the Tab key, advancing focus forward through the octets and to the set button.
   - **Period (.) Key**: Mimics the Enter/Tab key functionality within the octets.

3. **Data Validation and Handling**:
   - **Set Button**: Disabled if the input IP address is either currently in use or is the same as the existing address. Enabled only when a valid, unique IP address is entered.
   - **Backspace Key**: On an empty OctletWidget, focus shifts to the previous octet.
   - **Delete Key**: Clears the content forward, similar to a typical text field interaction.

4. **Focus and Input Management**:
   - **Click on Octlet**: Clears the current input but stores it temporarily. If focus is lost without new input, the old value is restored.
   - **Click Outside Octlet**: Focus loss without changes restores the original input. If changes are invalid upon focus loss, reverts to the last valid input or the original if no valid input was previously entered.

### OctletWidget Requirements

1. **Input Constraints**:
   - **Digit Acceptance**: Accepts only numeric input with a maximum of three digits.
   - **Valid Range**: Accepts digits from 1 to 254. Inputs like '0' and '255' are automatically rejected or corrected based on RFC standards.

2. **User Interaction**:
   - **Direct Input**: As numbers are entered, input automatically advances to the next octet under the following conditions:
     - Three digits are entered.
     - Two digits form a complete and valid octet and no subsequent valid digit can be added (e.g., entering '25' can logically be followed by any digit, but '26' must advance since '260'-'254' is invalid).
   - **Period/Enter as Tab**: Acts as a Tab within the octet context, moving to the next field.

### General Considerations

- **Dependency Injection**: Ensure components like OctletWidgets can be tested independently by injecting dependencies during initialization.
- **OOP Principles**: Utilize encapsulation for the widgets, ensuring that each component manages its state and behavior.
- **Use of Python's `ipaddress` Module**: Leverage this for validating IP address correctness and for potentially parsing and handling IP addresses.
- **Existing Solutions**: Research and potentially reuse existing implementations of IP address widgets or similar components to reduce development time.



============


### IPManagerWidget Requirements

1. **Field Composition**: Comprises four subfields (OctletWidgets) representing the octets of an IP address, separated by static labels displaying '.'.
   - [x] Implemented

2. **Navigation**:
   - [x] **Tab Key**: Advances to the next octet. If the last octet is focused, it advances to the set button.
   - [x] **Shift+Tab Key**: Moves focus to the previous octet or from the first octet back to another designated UI element.
   - [x] **Enter Key**: Functions identically to the Tab key, advancing focus forward through the octets and to the set button.
   - [x] **KP_Enter**: Mirrors the behavior of the Enter key, advancing focus forward.
   - [x] **Arrow Keys**: Left and Right Arrow keys allow navigation between octets.
   - [x] **Period (.) Key**: Mimics the Enter/Tab key functionality within the octets.
   - [x] **Shift+Enter** and **Shift+KP_Enter**: restrict navigation from the first octet.

3. **Data Validation and Handling**:
   - [x] **Set Button**: Needs implementation details about disabling based on IP address status.
   - [x] **Backspace Key**: On an empty OctletWidget, focus shifts to the previous octet. Does not move past the first octet when combined with Shift.
   - [x] **Delete Key**: Clears the content forward, similar to a typical text field interaction.

4. **Focus and Input Management**:
   - [x] **Click on Octlet**: Clears the current input but stores it temporarily. If focus is lost without new input, the old value is restored.
   - [x] **Click Outside Octlet**: Focus loss without changes restores the original input. If changes are invalid upon focus loss, reverts to the last valid input or the original if no valid input was previously entered.

### OctletWidget Requirements

1. **Input Constraints**:
   - [x] **Digit Acceptance**: Accepts only numeric input with a maximum of three digits.
   - [x] **Valid Range**: Accepts digits from 1 to 254. Inputs like '0' and '255' are automatically rejected or corrected based on RFC standards.

2. **User Interaction**:
   - [ ] **Direct Input**: As numbers are entered, input automatically advances to the next octet under the following conditions:
     - [ ] Three digits are entered.
     - [ ] Two digits form a complete and valid octet and no subsequent valid digit can be added.
   - [x] **Period/Enter as Tab**: Acts as a Tab within the octet context, moving to the next field.

### General Considerations

- [x] **Dependency Injection**: Ensure components like OctletWidgets can be tested independently by injecting dependencies during initialization.
- [x] **OOP Principles**: Utilize encapsulation for the widgets, ensuring that each component manages its state and behavior.
- [x] **Use of Python's `ipaddress` Module**: Leverage this for validating IP address correctness and for potentially parsing and handling IP addresses.
- [ ] **Existing Solutions**: Research and potentially reuse existing implementations of IP address widgets or similar components to reduce development time.

### Additional Constraints Identified During Development

- [x] Navigational controls extended to include arrow keys for intra-widget navigation.
- [x] Ensure Shift-modified keys do not allow navigation out of context, such as `Shift+Enter` not leaving the first octet.



`.`, `enter`, `shift + enter`, `kp_enter`, `shift + kp_enter`
these commands should temporarly clear the octet whenever they enter it this way fresh value can be entered
quickly and effeciently But if no changes are made it should repooulate with the old value,
in addition t everythng they already do.

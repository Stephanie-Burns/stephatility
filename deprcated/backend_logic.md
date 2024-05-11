## Network Configuration Application Plan

### 1. **GUI Design and Interaction**
#### Toplevel Window - Manage IP Configuration
- **Ethernet/Wifi Toggle**, Will help with regex capture.
- **Network Adapter Name**, What to interface with.
- **IP Address, Subnet Mask, and Gateway Entries:** Create fields in the GUI for users to input new values.
- **Set Button:** Triggers the submission of the network configuration changes.

#### Frame - IP Address Box
- **IP Address**, Create fields in the GUI for users to input new values.
- **Set Button:** Triggers the submission of the network configuration changes.

### 2. **Data Handling and Validation**
- **Entry Field Handlers:** 
  - Validate inputs either in the GUI or within the `NetworkConfiguration` instance.
  - If validation passes, update the `NetworkConfiguration` instance.
  - If validation fails, display an error message in the GUI.

### 3. **Change Network Configuration**
- **Method Setup:** 
  - Create a `change_network_configuration` method in `QuickWinIP` or a controller class to handle:
    - Admin privilege checks.
    - Apply changes via a CLI script with elevated privileges if not admin.
    - Apply changes directly using system commands if admin.

### 4. **Admin Check and Execution**
- **Admin Privilege Check:** Determine if the user has administrative privileges.
- **Non-Admin Handling:**
  - Launch a script or executable with elevated privileges to perform network changes.
  - Communicate results back to the main application via IPC mechanisms.
- **Admin Handling:**
  - Directly execute network setting changes using `subprocess`.
  - Capture and handle output and errors to log or display in the GUI.

### 5. **Reporting and Feedback**
- **Standard Output and Error Listening:**
  - Listen for the output from subprocess or external script.
  - Update GUI based on success or failure messages from the subprocess or script.

### 6. **Error Handling and User Feedback**
- Implement comprehensive error handling across all application components.
- Provide clear, informative feedback in the GUI regarding the status of operations.

### 7. **Testing and Iteration**
- **Unit Tests:** Write tests for individual components, especially input validation and `NetworkConfiguration` updates.
- **Integration Tests:** Test the integration between the GUI, `NetworkConfiguration` logic, and system-level commands.
- **User Testing:** Conduct testing with actual users to gather feedback on usability and reliability.

### Implementation Notes
- **Security Concerns:** Handle network configurations and elevated privileges with care. Ensure operations are secure and inputs are validated.
- **Compatibility:** Ensure methods for applying network settings and checking admin rights are compatible with target operating systems.
- **User Experience:** Design for a responsive and informative user interface that reflects the application state and changes promptly.

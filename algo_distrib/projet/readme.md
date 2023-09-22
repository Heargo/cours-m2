# Distributed Systems Communication Module

This Python class, named "Com," is designed to facilitate communication and synchronization in a distributed system with multiple processes. It's based on the [PyEventBus3](https://pypi.org/project/PyEventBus3/) module.

## Table of Contents

- [How to run the project](#how-to-run-the-project)
- [Features](#features)
- [Usage](#usage)
- [Technicals decisions](#technicals-decisions)

## How to run the project

execute the following command in the same directory as this readme file:

```bash
python3 Launcher.py
```

This command will run the `Launcher.py` file which will start 3 processes. The processes will communicate with each other and print the messages they receive.

You can customize the number of processes by changing the `nbProcess` variable in the `Launcher.py` file.

You can also change the test by uncommenting the test you want to run in the `Process.py` file and commenting the others tests (in the `run` method).

## Features

- Messages: Processes can send messages to each other asynchronously or synchronously.
- Broadcast: Broadcast messages to all processes asynchronously or synchronously.
- Synchronization: Processes can synchronize.
- Token-based access to critical section: Processes can request access to a critical section. The token is passed from process to process in a ring topology.
- Dead process handling: Processes can detect and handle the termination of other processes.

## Usage of the Com class

To use the `Com` API for inter-process communication and synchronization, follow these steps:

1. Import the `Com` class from your module:

   ```python
   from Com import Com
   ```

2. Create an instance of the `Com` class by specifying the number of processes. You can show or hide com logs. For example:

   ```python
   com = Com(number_of_processes,showLogs=True)
   ```

3. Retrieve the ID of the current process using the `getProcessId` method. This method waits for all processes to have a valid ID before returning the ID of the current process.

   ```python
   my_id = com.getId()
   ```

4. The `Com` class provides the following methods for communication and synchronization:

   - **Broadcast a Message (Asynchronous):**

     To send a message to all processes asynchronously, use the `broadcast` method:

     ```python
     com.broadcast("Hello, everyone!")
     ```

   - **Send a Direct Message (Asynchronous):**

     Send a direct message (async) to a specific process by its ID using the `sendTo` method:

     ```python
     com.sendTo(process_id, "Hello, Process {process_id}!")
     ```

     Replace `process_id` with the target process's ID.

   - **Synchronize Processes:**

     To synchronize all processes, use the `synchronize` method:

     ```python
     com.synchronize()
     ```

   - **Request and Release a Critical Section:**

     Use the following methods for critical section management:

     - Request access to a critical section:

       ```python
       com.requestSC()
       ```

     - Release control of the critical section:

       ```python
       com.releaseSC()
       ```

   - **Send a Synchronous Broadcast:**

     To send a synchronous broadcast message to all processes, use the `broadcastSync` method:

     ```python
     com.broadcastSync(sender_id,"Synchronous broadcast message")
     ```

   - **Send a Synchronous Message:**

     To send a synchronous message to a specific process by its ID, use the `sendToSync` method:

     ```python
     com.sendToSync(process_id, "Synchronous message")
     ```

   - **Receive a Synchronous Message:**

     Receive a synchronous message from a specific process by its ID using the `receiveFromSync` method:

     ```python
     com.receiveFromSync(process_id)
     ```

   - **Send a Token (Token-Based Algorithm):**

     To send a token and initiate a token-based algorithm, use the `sendToken` method:

     ```python
     com.sendToken()
     ```

5. Finally, to stop communication and terminate the thread, call the `stop` method. You should call this method when you stopping the process.

   ```python
   com.stop()
   ```

## Technicals decisions

### Token Algorithm

he token is passed from process to process in a ring topology. I chose this topology because it is the simplest to implement and it's efficient.

For the implementation, I chose to release the token after 300ms if the process does not need it. I chose to wait 300ms to avoid having too many messages in the system.

I also chose to use to variables instead of a single variable with 4 state to manage the token. I chose this solution because it is easier to read. The variables are `tokenPossessed` and `needToken` both are boolean.

### UUID for Process Identification during connection phase

I chose to use UUID for process identification during the connection phase because it is the simplest solution to implement. In the current state of the project, the processes are on the same machine, so there is no risk of identical UUIDs.

If the processes are on different machines, the possibility of having identical UUIDs is very low (as the UUID as 2<sup>122</sup> possible combinations). But if it happens, the processes will be stuck at the connection phase (when calling the `getId` method) and the user will have to restart the processes.

One way to avoid this issue is that instead of only using the UUID, we could use the UUID and the MAC address of the machine in this format for example: (`<mac_adresse>-<uuid>`). This way, the possibility of having identical UUIDs is not possible.

The UUID is generated using the `uuid4` method from the `uuid` module and are used to identify the process when the regular id (number) is unknown or changing.

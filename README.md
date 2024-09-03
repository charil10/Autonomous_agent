# Autonomous Agent Project

## Overview

This project involves the implementation of an autonomous agent system in Python. The system includes:

- An `AutonomousAgent` class that supports asynchronous messaging, reactiveness, and proactiveness.
- A `ConcreteAgent` class with specific behaviors and handlers.
- Two agents that communicate with each other via their inbox and outbox.
- Unit and integration tests to ensure correct functionality.

## Features

- **Asynchronous Messaging:** Agents communicate via queues, allowing asynchronous message passing.
- **Reactiveness:** Agents handle incoming messages using registered handlers.
- **Proactiveness:** Agents generate and send messages based on predefined behaviors.
- **Bidirectional Communication:** Two agents can exchange messages with each other.

## Classes

### `AutonomousAgent`

- **Attributes:**
  - `name`: The name of the agent.
  - `inbox`: A queue for incoming messages.
  - `outbox`: A queue for outgoing messages.
  - `handlers`: A dictionary mapping message types to handler functions.
  - `behaviors`: A list of proactive behaviors.

- **Methods:**
  - `register_handler(message_type, handler)`: Register a message handler for a given type.
  - `register_behavior(behavior)`: Register a proactive behavior.
  - `send_message(message)`: Send a message to the outbox.
  - `receive_message()`: Consume messages from the inbox and handle them.
  - `execute_behaviors()`: Execute proactive behaviors based on internal state or time.
  - `start()`: Start message handling and behavior execution in separate threads.
  - `stop()`: Stop the agent.

### `ConcreteAgent` (inherits from `AutonomousAgent`)

- **Initialization:**
  - Registers a handler for messages with the keyword "hello" that prints the message.
  - Registers a behavior that generates random 2-word messages every 2 seconds.

## Connecting Agents

Use the `connect_agents(agent_a, agent_b)` function to enable bidirectional message transfer between two agents.

## Running the Agents

To run the Agents, execute the `autonomous_agent.py` script:

```bash
python autonomous_agent.py

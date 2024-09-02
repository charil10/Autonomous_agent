import threading
import time
import random
from queue import Queue

class AutonomousAgent:
    def __init__(self, name):
        self.name = name
        self.inbox = Queue()
        self.outbox = Queue()
        self.handlers = {}
        self.behaviors = []
        self.running = True

    def register_handler(self, message_type, handler):
        """Register a message handler for a given message type."""
        self.handlers[message_type] = handler

    def register_behavior(self, behavior):
        """Register a proactive behavior."""
        self.behaviors.append(behavior)

    def send_message(self, message):
        """Send a message to the agent's outbox."""
        self.outbox.put(message)

    def receive_message(self):
        """Consume messages from the inbox."""
        while self.running:
            if not self.inbox.empty():
                message = self.inbox.get()
                message_type = message.get('type', None)
                handler = self.handlers.get(message_type)
                if handler:
                    handler(message)
            time.sleep(0.1)  # To avoid busy-waiting

    def execute_behaviors(self):
        """Execute proactive behaviors based on internal state or time."""
        while self.running:
            for behavior in self.behaviors:
                behavior(self)
            time.sleep(1)

    def start(self):
        """Start the agent's message handling and behavior execution."""
        threading.Thread(target=self.receive_message, daemon=True).start()
        threading.Thread(target=self.execute_behaviors, daemon=True).start()

    def stop(self):
        """Stop the agent."""
        self.running = False


# Concrete Agent Class
class ConcreteAgent(AutonomousAgent):
    def __init__(self, name):
        super().__init__(name)
        self.register_handler('greeting', self.handle_greeting)
        self.register_behavior(self.generate_random_message)

    def handle_greeting(self, message):
        """Handler that filters messages with the keyword 'hello'."""
        if 'hello' in message['content']:
            print(f"{self.name} received message: {message['content']}")

    def generate_random_message(self, agent):
        """Behavior that generates random 2-word messages every 2 seconds."""
        words = ["hello", "sun", "world", "space", "moon", "crypto", "sky", "ocean", "universe", "human"]
        message = {'type': 'greeting', 'content': f"{random.choice(words)} {random.choice(words)}"}
        print(f"{agent.name} sending message: {message['content']}")
        agent.send_message(message)
        time.sleep(2)  # Ensure it runs every 2 seconds



def connect_agents(agent_a, agent_b):
    """Continuously transfer messages from one agent's outbox to the other agent's inbox with logging."""
    
    def transfer_messages(from_agent, to_agent):
        while from_agent.running:
            if not from_agent.outbox.empty():
                message = from_agent.outbox.get()
                to_agent.inbox.put(message)
                # Print every transferred message for debugging
                print(f"{from_agent.name} -> {to_agent.name}: {message['content']}")
            time.sleep(0.1)  # Prevents busy-waiting

    # Create and start threads for bidirectional message transfer
    threading.Thread(target=transfer_messages, args=(agent_a, agent_b), daemon=True).start()
    threading.Thread(target=transfer_messages, args=(agent_b, agent_a), daemon=True).start()

# Create two agents
agent1 = ConcreteAgent("Agent 1")
agent2 = ConcreteAgent("Agent 2")

# Start the agents and connect their InBox and OutBox
agent1.start()
agent2.start()
connect_agents(agent1, agent2)

# Allow the agents to run for some time before stopping them
time.sleep(10)
agent1.stop()
agent2.stop()

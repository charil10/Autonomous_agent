import unittest
from unittest.mock import patch, call
import time
from autonomous_agent import ConcreteAgent, connect_agents  

class TestConcreteAgent(unittest.TestCase):

    def setUp(self):
        """Set up the agents before each test."""
        self.agent1 = ConcreteAgent("Agent 1")
        self.agent2 = ConcreteAgent("Agent 2")

    def tearDown(self):
        """Stop the agents after each test."""
        self.agent1.stop()
        self.agent2.stop()

    def test_handle_greeting(self):
        """Test the handle_greeting method to ensure it only prints messages with 'hello'."""
        with patch('builtins.print') as mock_print:
            message = {'type': 'greeting', 'content': 'hello world'}
            self.agent1.handle_greeting(message)
            mock_print.assert_called_with("Agent 1 received message: hello world")

            # Test a message without "hello" should not trigger print
            mock_print.reset_mock()
            message = {'type': 'greeting', 'content': 'goodbye world'}
            self.agent1.handle_greeting(message)
            mock_print.assert_not_called()

    def test_generate_random_message(self):
        """Test the generate_random_message method to ensure it creates a message of the correct format."""
        with patch.object(self.agent1, 'send_message') as mock_send_message:
            self.agent1.generate_random_message(self.agent1)
            mock_send_message.assert_called()
            args = mock_send_message.call_args[0]
            self.assertIn(args[0]['content'].split()[0], 
                          ["hello", "sun", "world", "space", "moon", "crypto", "sky", "ocean", "universe", "human"])
            self.assertIn(args[0]['content'].split()[1], 
                          ["hello", "sun", "world", "space", "moon", "crypto", "sky", "ocean", "universe", "human"])

    def test_agent_send_receive(self):
        """Test that agents can send and receive messages correctly."""
        # Manually send a message and check if it ends up in the other agent's inbox
        message = {'type': 'greeting', 'content': 'hello universe'}
        self.agent1.send_message(message)
        self.agent2.inbox.put(self.agent1.outbox.get())

        received_message = self.agent2.inbox.get()
        self.assertEqual(received_message['content'], 'hello universe')


class TestIntegration(unittest.TestCase):

    def setUp(self):
        """Set up two connected agents."""
        self.agent1 = ConcreteAgent("Agent 1")
        self.agent2 = ConcreteAgent("Agent 2")
        connect_agents(self.agent1, self.agent2)
        self.agent1.start()
        self.agent2.start()

    def tearDown(self):
        """Stop the agents after the tests."""
        self.agent1.stop()
        self.agent2.stop()

    def test_integration_message_flow(self):
        """Integration test to ensure proper message flow between the two agents."""
        with patch('builtins.print') as mock_print:
            # Let agents run for 10 seconds to allow multiple message exchanges
            time.sleep(10)

            # Check that messages with "hello" are correctly handled and printed
            print_calls = [call for call in mock_print.call_args_list if 'received message: hello' in str(call)]
            self.assertGreater(len(print_calls), 0, "Expected at least one 'hello' message to be handled and printed.")

if __name__ == '__main__':
    unittest.main()


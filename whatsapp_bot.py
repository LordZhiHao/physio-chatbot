import logging
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from chatbot import get_response
import os
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='lo_physio_bot.log'
)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)

@app.route('/bot', methods=['POST'])
def bot():
    try:
        # Get incoming message
        incoming_msg = request.values.get('Body', '').strip()
        sender = request.values.get('From', '')
        
        logger.info(f"Received message from {sender}: {incoming_msg}")
        
        # Create response
        resp = MessagingResponse()
        msg = resp.message()
        
        # Get response from chatbot
        response = get_response(incoming_msg)
        msg.body(response)
        
        logger.info(f"Sent response to {sender}: {response}")
        
        return str(resp)
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        
        # Create error response
        resp = MessagingResponse()
        msg = resp.message()
        msg.body("I'm sorry, I encountered an error. Please try again later or contact Lo Physiotherapy directly at +6012-529 7825.")
        
        return str(resp)

if __name__ == '__main__':
    app.run(debug=True)
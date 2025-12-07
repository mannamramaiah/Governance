from flask import Flask, request, jsonify, render_template_string
from markupsafe import Markup
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# HTML Template as a string
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Government Services Chatbot</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background: linear-gradient(135deg, #1a237e, #311b92);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .chat-container {
            width: 100%;
            max-width: 900px;
            height: 85vh;
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .header {
            background: linear-gradient(to right, #2c3e50, #4a6491);
            color: white;
            padding: 20px;
            text-align: center;
            position: relative;
        }

        .header h1 {
            font-size: 1.8rem;
            margin-bottom: 5px;
        }

        .header p {
            opacity: 0.9;
            font-size: 0.9rem;
        }

        .chatbot-icon {
            position: absolute;
            right: 20px;
            top: 20px;
            background: #00b894;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }

        .chat-content {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: #f8f9fa;
        }

        .message {
            margin-bottom: 15px;
            display: flex;
            align-items: flex-start;
        }

        .bot-message {
            justify-content: flex-start;
        }

        .user-message {
            justify-content: flex-end;
        }

        .message-bubble {
            max-width: 70%;
            padding: 12px 18px;
            border-radius: 18px;
            position: relative;
            word-wrap: break-word;
        }

        .bot-message .message-bubble {
            background: white;
            border: 1px solid #e0e0e0;
            border-top-left-radius: 4px;
            color: #333;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .user-message .message-bubble {
            background: linear-gradient(to right, #4776E6, #8E54E9);
            color: white;
            border-top-right-radius: 4px;
        }

        .service-response {
            margin-top: 10px;
            padding: 15px;
            background: #f8f9ff;
            border-radius: 10px;
            border-left: 4px solid #4776E6;
        }

        .service-response h4 {
            color: #2c3e50;
            margin-bottom: 8px;
            font-size: 1rem;
        }

        .service-response ul {
            padding-left: 20px;
            margin-bottom: 10px;
        }

        .service-response li {
            margin-bottom: 5px;
            color: #444;
        }

        .gov-link {
            color: #3498db;
            text-decoration: none;
            font-weight: 500;
        }

        .gov-link:hover {
            text-decoration: underline;
        }

        .phone-link {
            color: #e74c3c;
            text-decoration: none;
            font-weight: 500;
        }

        .processing-time {
            background: #e8f4fc;
            padding: 8px 12px;
            border-radius: 6px;
            margin-top: 10px;
            font-size: 0.9rem;
            color: #2980b9;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .input-area {
            padding: 20px;
            background: white;
            border-top: 1px solid #eee;
            display: flex;
            gap: 10px;
        }

        .input-area input {
            flex: 1;
            padding: 14px 18px;
            border: 2px solid #ddd;
            border-radius: 50px;
            font-size: 1rem;
            outline: none;
            transition: border-color 0.3s;
        }

        .input-area input:focus {
            border-color: #4776E6;
        }

        .input-area button {
            background: linear-gradient(to right, #4776E6, #8E54E9);
            color: white;
            border: none;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 1.2rem;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .input-area button:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(142, 84, 233, 0.4);
        }

        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 12px;
            margin-top: 15px;
        }

        .service-button {
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 12px;
            cursor: pointer;
            transition: all 0.3s;
            text-align: center;
            font-weight: 500;
            color: #2c3e50;
        }

        .service-button:hover {
            background: #4776E6;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        .welcome-message {
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #f8f9ff, #e8f4fc);
            border-radius: 15px;
            margin-bottom: 20px;
        }

        .welcome-message h3 {
            color: #2c3e50;
            margin-bottom: 10px;
        }

        .typing-indicator {
            display: inline-flex;
            gap: 4px;
        }

        .typing-indicator span {
            width: 8px;
            height: 8px;
            background: #95a5a6;
            border-radius: 50%;
            animation: typing 1.4s infinite ease-in-out;
        }

        .typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
        .typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

        @keyframes typing {
            0%, 80%, 100% { transform: scale(0.7); opacity: 0.5; }
            40% { transform: scale(1); opacity: 1; }
        }

        .suggestions {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 10px;
        }

        .suggestion-button {
            background: #e8f4fc;
            border: 1px solid #3498db;
            color: #2980b9;
            padding: 8px 15px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.3s;
        }

        .suggestion-button:hover {
            background: #3498db;
            color: white;
        }

        @media (max-width: 768px) {
            .chat-container {
                height: 90vh;
                border-radius: 15px;
            }
            
            .services-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .message-bubble {
                max-width: 85%;
            }
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="header">
            <h1>Government Services Chatbot</h1>
            <p>Your digital assistant for all government services</p>
            <div class="chatbot-icon">
                <i class="fas fa-robot"></i>
            </div>
        </div>

        <div class="chat-content" id="chatbox">
            <!-- Messages will be added here dynamically -->
        </div>

        <div class="input-area">
            <input type="text" id="userInput" placeholder="Ask about government services..." autocomplete="off">
            <button id="sendButton">
                <i class="fas fa-paper-plane"></i>
            </button>
        </div>
    </div>

    <script>
        // DOM Elements
        const chatbox = document.getElementById('chatbox');
        const userInput = document.getElementById('userInput');
        const sendButton = document.getElementById('sendButton');
        
        // API URL - Update this if your Flask server is running on a different port
        const API_URL = 'http://127.0.0.1:5000';
        
        // Initial welcome message
        window.onload = function() {
            addBotMessage("Hello! I'm your Government Services Assistant. I can help you with various services like income certificates, caste certificates, electricity bills, and more. How can I assist you today?");
            loadServices();
        };
        
        // Load available services
        function loadServices() {
            fetch(`${API_URL}/get_all_services`)
                .then(response => response.json())
                .then(data => {
                    if (data.services && data.services.length > 0) {
                        let servicesHTML = `
                            <div class="welcome-message">
                                <h3>Popular Services</h3>
                                <div class="services-grid">
                        `;
                        
                        data.services.forEach(service => {
                            servicesHTML += `
                                <div class="service-button" onclick="selectService('${service.id}')">
                                    ${service.title}
                                </div>
                            `;
                        });
                        
                        servicesHTML += `
                                </div>
                                <p style="margin-top: 15px; color: #666;">Or type your query in the box below</p>
                            </div>
                        `;
                        
                        chatbox.innerHTML += servicesHTML;
                        chatbox.scrollTop = chatbox.scrollHeight;
                    }
                })
                .catch(error => {
                    console.error('Error loading services:', error);
                    addBotMessage("Welcome! I can help you with government services. Please type your query.");
                });
        }
        
        // Add bot message to chat
        function addBotMessage(message, isHTML = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message bot-message';
            
            const bubble = document.createElement('div');
            bubble.className = 'message-bubble';
            
            if (isHTML) {
                bubble.innerHTML = message;
            } else {
                bubble.textContent = message;
            }
            
            messageDiv.appendChild(bubble);
            chatbox.appendChild(messageDiv);
            chatbox.scrollTop = chatbox.scrollHeight;
        }
        
        // Add user message to chat
        function addUserMessage(message) {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message user-message';
            
            const bubble = document.createElement('div');
            bubble.className = 'message-bubble';
            bubble.textContent = message;
            
            messageDiv.appendChild(bubble);
            chatbox.appendChild(messageDiv);
            chatbox.scrollTop = chatbox.scrollHeight;
        }
        
        // Show typing indicator
        function showTypingIndicator() {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message bot-message';
            messageDiv.id = 'typingIndicator';
            
            const bubble = document.createElement('div');
            bubble.className = 'message-bubble';
            bubble.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
            
            messageDiv.appendChild(bubble);
            chatbox.appendChild(messageDiv);
            chatbox.scrollTop = chatbox.scrollHeight;
        }
        
        // Remove typing indicator
        function removeTypingIndicator() {
            const indicator = document.getElementById('typingIndicator');
            if (indicator) {
                indicator.remove();
            }
        }
        
        // Select service by ID
        function selectService(serviceId) {
            // Add user message
            addUserMessage(`Tell me about ${serviceId.replace(/_/g, ' ')}`);
            
            // Show typing indicator
            showTypingIndicator();
            
            // Send request to backend
            fetch(`${API_URL}/get_service_info`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ service_id: serviceId })
            })
            .then(response => response.json())
            .then(data => {
                removeTypingIndicator();
                
                if (data.success) {
                    addBotMessage(`Here's information about ${data.title}:`, true);
                    addBotMessage(data.response, true);
                } else {
                    addBotMessage(data.error);
                    
                    // Show suggestions if available
                    if (data.suggestions && data.suggestions.length > 0) {
                        let suggestionsHTML = '<p>Try one of these:</p><div class="suggestions">';
                        data.suggestions.forEach(suggestion => {
                            suggestionsHTML += `<button class="suggestion-button" onclick="selectService('${suggestion.id}')">${suggestion.title}</button>`;
                        });
                        suggestionsHTML += '</div>';
                        addBotMessage(suggestionsHTML, true);
                    }
                }
            })
            .catch(error => {
                removeTypingIndicator();
                addBotMessage("Sorry, I'm having trouble connecting to the server. Please try again.");
                console.error('Error:', error);
            });
            
            userInput.value = '';
        }
        
        // Send message
        function sendMessage() {
            const message = userInput.value.trim();
            
            if (message === '') return;
            
            // Add user message to chat
            addUserMessage(message);
            
            // Clear input
            userInput.value = '';
            
            // Show typing indicator
            showTypingIndicator();
            
            // Send request to backend
            fetch(`${API_URL}/get_service_info`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: message })
            })
            .then(response => response.json())
            .then(data => {
                removeTypingIndicator();
                
                if (data.success) {
                    addBotMessage(`I found information about ${data.title}:`, true);
                    addBotMessage(data.response, true);
                } else {
                    addBotMessage(data.error || "I couldn't find that service. Please try being more specific.");
                    
                    // Show suggestions if available
                    if (data.suggestions && data.suggestions.length > 0) {
                        let suggestionsHTML = '<p>Did you mean:</p><div class="suggestions">';
                        data.suggestions.forEach(suggestion => {
                            suggestionsHTML += `<button class="suggestion-button" onclick="selectService('${suggestion.id}')">${suggestion.title}</button>`;
                        });
                        suggestionsHTML += '</div>';
                        addBotMessage(suggestionsHTML, true);
                    }
                }
            })
            .catch(error => {
                removeTypingIndicator();
                addBotMessage("Sorry, I'm having trouble connecting to the server. Please check if the Flask server is running.");
                console.error('Error:', error);
            });
        }
        
        // Event Listeners
        sendButton.addEventListener('click', sendMessage);
        
        userInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
'''

# Knowledge Base with all services and responses including proper links
SERVICES = {
    "income_cert": {
        "title": "Income Certificate",
        "keywords": ["income", "salary", "earnings", "income certificate"],
        "response": Markup("""
        <div class="service-response">
            <h4>Application Options:</h4>
            <ul>
                <li>Online: <a href="https://onlineap.meeseva.gov.in/CitizenPortal/UserInterface/Citizen/Home.aspx" target="_blank" class="gov-link">Meeseva Portal</a></li>
                <li>Offline: Visit local revenue office</li>
            </ul>
            
            <h4>Required Documents:</h4>
            <ul>
                <li>Salary slips/employer certificate</li>
                <li>Affidavit for self-employed individuals</li>
                <li>Ration card copy</li>
                <li>Aadhaar card</li>
            </ul>
            
            <div class="processing-time">
                <i class="fas fa-clock"></i> Processing Time: 10 working days
            </div>
        </div>
        """)
    },
    "cast_cert": {
        "title": "Caste Certificate",
        "keywords": ["caste", "sc", "st", "caste certificate"],
        "response": Markup("""
        <div class="service-response">
            <h4>Application Process:</h4>
            <ul>
                <li><strong>Online:</strong> <a href="https://ap.meeseva.gov.in/IMeeSeva2/IMeesevaHome.aspx" target="_blank" class="gov-link">Meeseva Portal</a></li>
                <li><strong>Offline:</strong> Visit local Tahsildar office</li>
            </ul>
            
            <h4>Required Documents:</h4>
            <ul>
                <li>School certificate with caste</li>
                <li>Father's caste certificate (if available)</li>
                <li>Aadhaar card</li>
                <li>Ration card</li>
            </ul>
        </div>
        """)
    },
    "electricity": {
        "title": "Electricity Bill Payment",
        "keywords": ["electricity", "power", "bill", "electricity bill", "eb bill"],
        "response": Markup("""
        <div class="service-response">
            <h4>Bill Payment Options:</h4>
            <ul>
                <li><strong>APEPDCL:</strong> <a href="https://www.apeasternpower.com/" target="_blank" class="gov-link">AP Eastern Power</a></li>
                <li><strong>APSPDCL:</strong> <a href="https://www.apspdcl.in/index.jsp" target="_blank" class="gov-link">AP Southern Power</a></li>
                <li><strong>TSSPDCL:</strong> <a href="https://tgsouthernpower.org/" target="_blank" class="gov-link">TS Southern Power</a></li>
            </ul>
            
            <h4>Complaint Numbers:</h4>
            <ul>
                <li><strong>24x7 Helpline:</strong> <a href="tel:1912" class="phone-link">1912</a></li>
            </ul>
        </div>
        """)
    },
    "education": {
        "title": "Education Certificates",
        "keywords": ["education", "marks", "certificate", "10th", "inter", "degree"],
        "response": Markup("""
        <div class="service-response">
            <h4>Certificate Downloads:</h4>
            <ul>
                <li><strong>10th Marks:</strong> <a href="https://bse.ap.gov.in/" target="_blank" class="gov-link">AP Board of Secondary Education</a></li>
                <li><strong>Inter Marks:</strong> <a href="https://bie.ap.gov.in/" target="_blank" class="gov-link">AP Board of Intermediate Education</a></li>
                <li><strong>Diploma Certificates:</strong> <a href="https://apsbtet.net/studentportal/screens/mainstudentinfo.aspx" target="_blank" class="gov-link">SBTET AP</a></li>
                <li><strong>Degree/UG/PG:</strong> <a href="https://apsche.ap.gov.in//" target="_blank" class="gov-link">AP State Portal</a></li>
            </ul>
            
            <h4>Verification:</h4>
            <ul>
                <li><strong>DigiLocker:</strong> <a href="https://digilocker.gov.in/" target="_blank" class="gov-link">DigiLocker</a></li>
            </ul>
        </div>
        """)
    },
    "dob_cert": {
        "title": "Date of Birth Certificate",
        "keywords": ["birth", "dob", "date of birth", "birth certificate"],
        "response": Markup("""
        <div class="service-response">
            <h4>Application Process:</h4>
            <ul>
                <li><strong>Online:</strong> <a href="https://crsorgi.gov.in/" target="_blank" class="gov-link">CRSORGI</a></li>
                <li><strong>Offline:</strong> Visit local Municipal office</li>
            </ul>
            
            <h4>Required Documents:</h4>
            <ul>
                <li>Hospital birth record</li>
                <li>Parent's ID proof</li>
                <li>Address proof</li>
                <li>Affidavit (if delayed registration)</li>
            </ul>
        </div>
        """)
    },
    "obc_cert": {
        "title": "OBC Certificate",
        "keywords": ["obc", "other backward", "obc certificate"],
        "response": Markup("""
        <div class="service-response">
            <h4>Application Process:</h4>
            <ul>
                <li><strong>Online:</strong> <a href="https://onlineap.meeseva.gov.in/CitizenPortal/UserInterface/Citizen/Home.aspx" target="_blank" class="gov-link">Meeseva Portal</a></li>
                <li><strong>Offline:</strong> Visit local Tahsildar office</li>
            </ul>
            
            <h4>Required Documents:</h4>
            <ul>
                <li>Income certificate</li>
                <li>Caste proof of parents</li>
                <li>Residence proof</li>
                <li>Aadhaar card</li>
            </ul>
        </div>
        """)
    },
    "healthcare": {
        "title": "Healthcare Services",
        "keywords": ["health", "hospital", "medical", "healthcare", "doctor"],
        "response": Markup("""
        <div class="service-response">
            <h4>Healthcare Schemes:</h4>
            <ul>
                <li><strong>Aarogyasri:</strong> <a href="https://www.rajivaarogyasri.telangana.gov.in/ASRI2.0/portal/body.html" target="_blank" class="gov-link">Aarogyasri Telangana</a></li>
                <li><strong>Aarogyasri:</strong> <a href="https://drntrvaidyaseva.ap.gov.in/" target="_blank" class="gov-link">Aarogyasri Andhra Pradesh</a></li>
                <li><strong>Ayushman Bharat:</strong> <a href="https://pmjay.gov.in/" target="_blank" class="gov-link">PM-JAY</a></li>
                <li><strong>Ambulance:</strong> Dial <a href="tel:108" class="phone-link">108</a></li>
            </ul>
            
            <h4>Hospital Search:</h4>
            <ul>
                <li><strong>Government Hospitals:</strong> <a href="https://health.telangana.gov.in/hospitals/" target="_blank" class="gov-link">TS Health Dept</a></li>
            </ul>
        </div>
        """)
    },
    "aadhar": {
        "title": "Aadhaar Services",
        "keywords": ["aadhaar", "uid", "aadhar", "aadhaar card"],
        "response": Markup("""
        <div class="service-response">
            <h4>Services Available:</h4>
            <ul>
                <li><strong>New Enrollment:</strong> <a href="https://uidai.gov.in/" target="_blank" class="gov-link">UIDAI</a></li>
                <li><strong>Update Details:</strong> <a href="https://uidai.gov.in/en/my-aadhaar/update-aadhaar.html" target="_blank" class="gov-link">Update Portal</a></li>
                <li><strong>Locate Center:</strong> <a href="https://appointments.uidai.gov.in/" target="_blank" class="gov-link">Find Centers</a></li>
            </ul>
        </div>
        """)
    },
    "pan": {
        "title": "PAN Card Services",
        "keywords": ["pan", "permanent account", "pan card", "income tax"],
        "response": Markup("""
        <div class="service-response">
            <h4>Application Process:</h4>
            <ul>
                <li><strong>New PAN:</strong> <a href="https://www.onlineservices.nsdl.com/paam/endUserRegisterContact.html" target="_blank" class="gov-link">NSDL Portal</a></li>
                <li><strong>Track Application:</strong> <a href="https://tin.tin.nsdl.com/pantan/StatusTrack.html" target="_blank" class="gov-link">Track PAN</a></li>
            </ul>
        </div>
        """)
    },
    "ration": {
        "title": "Ration Card Services",
        "keywords": ["ration", "food", "ration card", "pds"],
        "response": Markup("""
        <div class="service-response">
            <h4>Services Available:</h4>
            <ul>
                <li><strong>AP Ration Card:</strong> <a href="https://epds1.ap.gov.in/epdsAP/epds" target="_blank" class="gov-link">AP E-PDS</a></li>
                <li><strong>TS Ration Card:</strong> <a href="https://epds.telangana.gov.in/" target="_blank" class="gov-link">TS E-PDS</a></li>
            </ul>
        </div>
        """)
    }
}

def find_service_by_keyword(query):
    """Find service by natural language query"""
    query = query.lower().strip()
    
    # Exact match for service IDs
    if query in SERVICES:
        return query
    
    # Keyword matching
    for service_id, service_data in SERVICES.items():
        if 'keywords' in service_data:
            for keyword in service_data['keywords']:
                if keyword in query:
                    return service_id
    
    # Try partial matches
    for service_id, service_data in SERVICES.items():
        if service_data['title'].lower() in query or query in service_data['title'].lower():
            return service_id
    
    return None

def sanitize_input(text):
    """Sanitize user input"""
    if not text:
        return ""
    # Remove potentially harmful characters but keep essential punctuation
    text = re.sub(r'[<>]', '', text)
    return text.strip()

@app.route('/')
def home():
    """Serve the HTML page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/get_service_info', methods=['POST'])
def get_service_info():
    """Get service information based on user query"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        user_input = sanitize_input(data.get('query', ''))
        service_id = sanitize_input(data.get('service_id', ''))
        
        # If service_id is not provided, try to find by keyword
        if not service_id and user_input:
            service_id = find_service_by_keyword(user_input)
        
        if service_id in SERVICES:
            return jsonify({
                "success": True,
                "title": SERVICES[service_id]["title"],
                "response": SERVICES[service_id]["response"],
                "service_id": service_id
            })
        else:
            # Provide helpful suggestions
            suggestions = [
                {"id": key, "title": value["title"]} 
                for key, value in list(SERVICES.items())[:3]
            ]
            
            return jsonify({
                "success": False,
                "error": "I couldn't find that service. Here are some popular services:",
                "suggestions": suggestions,
                "user_input": user_input
            })
            
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "success": False,
            "error": "An error occurred. Please try again."
        }), 500

@app.route('/get_all_services', methods=['GET'])
def get_all_services():
    """Get all available services"""
    services_list = [
        {"id": key, "title": value["title"]} 
        for key, value in SERVICES.items()
    ]
    return jsonify({"services": services_list})

@app.route('/search_services', methods=['POST'])
def search_services():
    """Search services by keyword"""
    try:
        data = request.json
        search_term = sanitize_input(data.get('search', '')).lower()
        
        if not search_term:
            return jsonify({"services": []})
        
        results = []
        for service_id, service_data in SERVICES.items():
            # Search in title
            if search_term in service_data['title'].lower():
                results.append({"id": service_id, "title": service_data["title"]})
                continue
            
            # Search in keywords
            if 'keywords' in service_data:
                for keyword in service_data['keywords']:
                    if search_term in keyword:
                        results.append({"id": service_id, "title": service_data["title"]})
                        break
        
        return jsonify({"services": results})
        
    except Exception as e:
        return jsonify({"services": []})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "services_count": len(SERVICES)})

if __name__ == '__main__':
    print("Starting Government Services Chatbot...")
    print(f"Available services: {len(SERVICES)}")
    print("Open your browser and go to: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)

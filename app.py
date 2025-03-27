from flask import Flask, request, jsonify, render_template
from markupsafe import Markup

app = Flask(__name__)

# Knowledge Base with all services and responses including proper links
SERVICES = {
    "income_cert": {
        "title": "Income Certificate",
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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_service_info', methods=['POST'])
def get_service_info():
    service_id = request.json.get('service_id')
    
    if service_id in SERVICES:
        return jsonify({
            "title": SERVICES[service_id]["title"],
            "response": SERVICES[service_id]["response"]
        })
    return jsonify({"error": "Service not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
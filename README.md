# Kyntra 🛒
A secure e-commerce platform. Built keeping in mind basic security requirements to avoid and withstand common vulnerability exploits.

## Technology Stack

**Server:** nginx  
**Backend:** Django framework  
**Database:** SQLite  
**Frontend:** Django templating engine, Bootstrap

Tested on GNU/Linux based OSs.


## Steps to run

1. Clone this repository
2. Run ``python3 -m pipenv shell`` or `` pipenv shell``
3. Run ``python3 manage.py runserver``  
By default, the server would start at port 8000.
  

## Security Features Implemented

Following are some of the prime features that we ensured while building the platform:
- 2FA for critical user actions
- Transaction and activity logging by the admin
- Virtual keyboards for OTPs
- Strict access control for all users
- Self-signed certificate for HTTPS (MITM prevention)
- Firewall and port blocking
- CSRF protection via tokens
- XSS prevention by properly cleaning & escaping all user inputs
  

## Vulnerabilities Discovered

Following are the vulnerabilities discovered by our peers in the testing phase:  
- SSL stripping (HTTPS STSH not used)
- OTP bypassing
- DOS protection absent
- Minor functionality bugs
  

## Team Members
- [Bassam Pervez Shamzi](https://github.com/basp0)
- [Rohan Jain](https://github.com/rohanj-02)
- [Samarth Saxena](https://github.com/samarth-saxena)
- [Shashank Daima](https://github.com/shashankdaima)  
  
Feedback, suggestions and contributions are welcome! 😄
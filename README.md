# CV-AUTHENTICATION-APP

## Problem Statement
In the digital age, security is paramount. Traditional password-based authentication systems are vulnerable to breaches, and phishing attacks, and can be easily compromised. Furthermore, users often struggle with password fatigue, leading to weak password choices. There's a pressing need for a more secure and user-friendly authentication method.

## Solution
The CV-AUTHENTICATION-APP offers a two-factor authentication system that combines the reliability of face recognition with the familiarity of password-based authentication. By integrating the FaceNet algorithm for face recognition and the MTCNN algorithm for face detection, this system ensures a higher level of security while providing a seamless user experience.

- **FaceNet**: A deep learning algorithm trained to produce embeddings of faces, allowing for efficient comparison between faces to ascertain identity.
  
- **MTCNN**: An algorithm designed for accurate face detection, ensuring that faces within images and videos are promptly identified.

The system will work as follows:
* The user will be presented with a prompt to enter their face and password
* The system will use MTCNN to detect the user's face in the image
* The system will use FaceNet to compare the user's face to the faces in the existing database
* If the faces match, the system will accept the password and authenticate the user
* If the faces do not match, the system will reject the password and deny access to the user
* 
## How to Run the Code

1. **Setup**: Ensure you have all the required packages installed. You can do this by running:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the Application**: Execute the main application file:
   ```bash
   python app.py
   ```
3. **Docker Option**: If you prefer using Docker, build the Docker image and run it:
   ```bash
   docker build -t cv-authentication-app .
   docker run -p 8000:8000 cv-authentication-app
   ```
   

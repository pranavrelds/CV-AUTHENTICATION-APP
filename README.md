# CV-AUTHENTICATION-APP

In this project, you will build a two-factor authentication system that uses face recognition and a password to authenticate users. The first factor is the face recognition, which uses the FaceNet algorithm to compare the user's face to a database of known faces. The second factor is the password, which is entered by the user. If both factors match, the user is authenticated.

FaceNet is a deep learning algorithm that is trained to learn the embeddings of faces. Embeddings are a way of representing faces as a vector of numbers. FaceNet can be used to compare two faces and determine if they are the same person.

MTCNN is another deep learning algorithm that is used for face detection. Face detection is the process of finding faces in an image. MTCNN can be used to detect faces in images and videos.

The two-factor authentication system that you will build will use FaceNet for face recognition and MTCNN for face detection. The system will work as follows:

    The user will be presented with a prompt to enter their face and password.
    The system will use MTCNN to detect the user's face in the image.
    The system will use FaceNet to compare the user's face to the faces in the database.
    If the faces match, the system will accept the password and authenticate the user.
    If the faces do not match, the system will reject the password and deny access to the user.

This two-factor authentication system is more secure than a system that uses only a password. This is because it is more difficult for an attacker to spoof both the user's face and their password.


### Existing App

1) ageitey
2) Compreface
3) Face ++
4) Face X
5) Kairos

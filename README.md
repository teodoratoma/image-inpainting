# image-inpainting

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Image inpainting is the process of filling in missing or damaged parts of an image, using information from their surrounding area. The goal is to create an image as realistic and coherent as possible for viewers. To solve this problem, I trained a model based on a neural network with UNet architecture, which I later integrated into a web application, which allows the user to upload an image, mark the portion that must be removed, and download the obtained image. The user also has an eraser, to be able to delete the markings, and 2 buttons: Undo and Redo. To implement the client-side, I used HTML, JavaScript and CSS to create the website. The communication between client and server was done through the Flask micro-framework, and the server was written in Python, using TensorFlow for network design, and OpenCV for image processing.

![Screenshot 2023-12-09 131146](https://github.com/teodoratoma/image-inpainting/assets/100185337/a5d5c062-d274-470e-bcfd-84fdb60a3fa0)

Uploading an image

![Screenshot 2023-12-09 131503](https://github.com/teodoratoma/image-inpainting/assets/100185337/782f87af-75ae-421f-914f-0f46fb4ea323)

Marking the portion to be removed from the image

![Screenshot 2023-12-09 131531](https://github.com/teodoratoma/image-inpainting/assets/100185337/4b3261cd-afb7-470b-91d7-b4f43a563f12)

The resulting image after inpainting

![Screenshot 2023-12-09 131548](https://github.com/teodoratoma/image-inpainting/assets/100185337/264fd3da-09ee-4259-ad32-4a10b7ddd1d4)

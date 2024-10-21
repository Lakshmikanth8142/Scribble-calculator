import cv2
import pytesseract
import sympy as sp
import os
import re

# Initialize pytesseract for OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update based on your system

# Function to preprocess the image for better OCR
def preprocess_image(image_path):
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' does not exist.")
        return None



    img = cv2.imread(image_path)
    if img is None:
        print("Error: Image not found or unable to load.")
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    blur = cv2.GaussianBlur(gray, (5, 5), 0)      # Apply Gaussian Blur
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)  
    return thresh

# Function to recognize handwriting from an image
def recognize_handwriting(image_path):
    preprocessed_image = preprocess_image(image_path)
    if preprocessed_image is not None:
        recognized_text = pytesseract.image_to_string(preprocessed_image, config='--psm 7')
        recognized_text = recognized_text.strip()
        print(f"Recognized Equation: {recognized_text}")
        # Basic validation: check if the text contains numbers or math symbols
        if not re.search(r'[0-9+\-*/()=]', recognized_text):
            print("Invalid equation recognized. No numbers or operators found.")
            return None
        return recognized_text
    return None

# Function to solve the equation or evaluate expression
def solve_equation(equation):
    try:
        # If the equation contains an '=', attempt to solve it
        if '=' in equation:
            expr = sp.sympify(equation)
            solution = sp.solve(expr)
            print(f"Solution: {solution}")
            return solution
        else:
            # Evaluate arithmetic expressions
            expr = sp.sympify(equation)
            result = expr.evalf()  # Evaluate the expression
            print(f"Result: {result}")
            return result
    except Exception as e:
        print(f"Error solving the equation: {e}")
        return None

# Main function to integrate image capture, OCR, and solving
def main(image_path):
    print("Processing Image...")
    equation = recognize_handwriting(image_path)
    
    if equation:
        print("Solving Equation or Expression...")
        result = solve_equation(equation)
        if result is not None:
            print(f"Final Result: {result}")
        else:
            print("Could not solve the equation.")
    else:
        print("Could not recognize a valid equation.")

# Example usage:
if __name__ == "__main__":
    image_path = "C:\\Users\\bdhar\\.vscode\\extensions\\pythonlk\\equation_image.png" # Correct way with double backslashes
  # Replace with the correct path to your image  # Update with the correct path
    main(image_path)

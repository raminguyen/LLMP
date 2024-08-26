import sys
import os
import torch
from dotenv import load_dotenv
import LLMP as L

class ImageProcessor:
    def __init__(self):
        # Load environment variables from the .env file
        load_dotenv()

        # Clear CUDA cache if using GPU
        torch.cuda.empty_cache()

        # Set the device to CPU (if needed)
        self.device = torch.device("cpu")

        # Create instances of the Gemini models
        self.gpt4vision = L.GPTModel("gpt-4-vision-preview")
        self.gpt4o = L.GPTModel("gpt-4o")
        self.gemini1 = L.GeminiProVision()  
        self.gemini2 = L.Gemini1_5Flash() 

        # Add them to a dictionary for easy access
        self.model_instances = {
            "gpt4o": self.gpt4o,
            "gpt4vision": self.gpt4vision,
            "LLaVA": L.LLaVA(),  
            "CustomLLaVA": L.CustomLLaVA(),  
            "GeminiProVision": self.gemini1,  
            "Gemini1_5Flash": self.gemini2
        }

    def run_10_image(self, query):
        # Define your images
        images = [L.GPImage.figure1('direction') for i in range(10)]
        
        # Run the evaluator
        result1 = L.Evaluator.run(images, query, self.model_instances)
        return result1

    def run_55_image(self, query):
        # Define your images
        images = [L.GPImage.figure1('direction') for i in range(55)]
        
        # Run the evaluator
        result2 = L.Evaluator.run(images, query, self.model_instances)
        return result2



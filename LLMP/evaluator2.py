import LLMP as L
import re
import time
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import torch

class Evaluator2:

    @staticmethod
    def calculate_mse(gt, answers):
        gt_array = np.array(gt)
        answers_array = np.array(answers)
        return mean_squared_error(gt_array, answers_array)

    @staticmethod
    def calculate_mlae(gt, answers):
        gt_array = np.array(gt)
        answers_array = np.array(answers)
        mlae = np.log2(mean_absolute_error(gt_array * 100, answers_array * 100) + .125)
        return mlae

    @staticmethod
    def calculate_mean(answers):
        return np.mean(answers)

    @staticmethod
    def calculate_std(answers):
        return np.std(answers)

    @staticmethod
    def run(data, query, models):
        images = [d[0] for d in data]
        gt = [d[1] for d in data]
        results = {'gt': gt}

        for model_name in models:
            raw_answers = []
            parsed_answers = []
            forced_repetitions = 0
            times = []

            for image in images:
                torch.cuda.empty_cache()
                FLAG = False
                start_time = time.time()

                while not FLAG:
                    answer = ""
                    if model_name == "LLaVA":
                        answer = L.LLaVA.query(query, image)
                    elif model_name == "ChatGPT":
                        answer = L.ChatGPT.query(query, image)
                    elif model_name == "CustomLLaVA":
                        answer = L.CustomLLaVA.query(query, image)
                    else:
                        raise ValueError(f"Unknown model_name: {model_name}")

                    values = re.findall(r'(\d+\.\d+)', answer)

                    if len(values) != 5:
                        values = values[-5:]

                    ranges_numbers = [float(val) for val in values]

                    if len(values) == 5:
                        raw_answers.append(answer)
                        parsed_answers.append(ranges_numbers)
                        FLAG = True
                        end_time = time.time()
                        times.append((end_time - start_time) * 1000)
                        if model_name == "ChatGPT":
                            time.sleep(2)  # Avoid hitting rate limits!
                    else:
                        forced_repetitions += 1
                        if model_name == "ChatGPT":
                            time.sleep(2)  # Avoid hitting rate limits!

            mse = Evaluator2.calculate_mse(gt, parsed_answers)
            mlae = Evaluator2.calculate_mlae(gt, parsed_answers)
            mean = None
            std = None

            results[model_name] = {
                'parameters': None,
                'raw_answers': raw_answers,
                'parsed_answers': parsed_answers,
                'mean': mean,
                'std': std,
                'mse': mse,
                'mlae': mlae,
                'times': times,
                'forced_repetitions': forced_repetitions
            }

        return results

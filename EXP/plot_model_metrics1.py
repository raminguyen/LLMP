from prettytable import PrettyTable
import matplotlib.pyplot as plt
import numpy as np

def plot_charts_metrics(result1, result2):
    # Function to extract mse and mlae for all models, rounded to 1 decimal place
    def extract_metrics_for_models(results):
        return {
            'gpt4o': (round(results['gpt4o']['mse'], 1), round(results['gpt4o']['mlae'], 1)),
            'gpt4vision': (round(results['gpt4vision']['mse'], 1), round(results['gpt4vision']['mlae'], 1)),
            'LLaVA': (round(results['LLaVA']['mse'], 1), round(results['LLaVA']['mlae'], 1)),
            'CustomLLaVA': (round(results['CustomLLaVA']['mse'], 1), round(results['CustomLLaVA']['mlae'], 1)),
            'GeminiProVision': (round(results['GeminiProVision']['mse'], 1), round(results['GeminiProVision']['mlae'], 1)),
            'Gemini1_5Flash': (round(results['Gemini1_5Flash']['mse'], 1), round(results['Gemini1_5Flash']['mlae'], 1)),
        }

    # Extract metrics for each result set
    metrics1 = extract_metrics_for_models(result1)
    metrics2 = extract_metrics_for_models(result2)

    # Create a table for comparison
    table = PrettyTable()
    table.field_names = [
        "Model", 
        "Result 1 MSE", "Result 2 MSE",
        "Result 1 MLAE", "Result 2 MLAE"
    ]

    # Add rows for each model
    for model in metrics1.keys():
        table.add_row([
            model,
            metrics1[model][0], metrics2[model][0],  # MSEs
            metrics1[model][1], metrics2[model][1]   # MLAEs
        ])

    # Print the table
    print(table)

    # Prepare data for plotting
    models = ['gpt4o', 'gpt4vision', 'LLaVA', 'CustomLLaVA', 'GeminiProVision', 'Gemini1_5Flash']
    model_positions = np.arange(len(models))  # Numeric positions for the models on the x-axis
    
    result1_mse = [metrics1[model][0] for model in models]
    result2_mse = [metrics2[model][0] for model in models]
    result1_mlae = [metrics1[model][1] for model in models]
    result2_mlae = [metrics2[model][1] for model in models]

    # Define distinct colors for the two results
    colors = ['b', 'g']  # Blue, Green

    # Plotting the data
    plt.figure(figsize=(16, 8))  # Increase the figure size

    # Plotting MSE (points only)
    plt.subplot(1, 2, 1)
    plt.scatter(model_positions - 0.1, result1_mse, color=colors[0], label='Result 1 MSE')
    plt.scatter(model_positions + 0.1, result2_mse, color=colors[1], label='Result 2 MSE')
    plt.xticks(model_positions, models, rotation=15)
    plt.title('MSE Comparison')
    plt.xlabel('Models')
    plt.ylabel('MSE')
    plt.legend()

    # Plotting MLAE (points only)
    plt.subplot(1, 2, 2)
    plt.scatter(model_positions - 0.1, result1_mlae, color=colors[0], label='Result 1 MLAE')
    plt.scatter(model_positions + 0.1, result2_mlae, color=colors[1], label='Result 2 MLAE')
    plt.xticks(model_positions, models, rotation=15)
    plt.title('MLAE Comparison')
    plt.xlabel('Models')
    plt.ylabel('MLAE')
    plt.legend()

    # Adjust layout with more spacing between plots
    plt.subplots_adjust(wspace=0.4)  # Increase space between the two subplots
    plt.tight_layout()
    plt.show()

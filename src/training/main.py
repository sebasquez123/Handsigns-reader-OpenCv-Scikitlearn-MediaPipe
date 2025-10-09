from data_preprocess import process_images
from model_training import pre_training, final_training
from inference import test_model

dir_processed = 'data/gestures.csv'
dir_model = 'models/trained_model.pkl'

print("")
print("° Welcome to the Decision Tree Training Workshop for MediaPipe Hands! ⚙️🤖")
print("° This small local tool helps you collect hand-gesture data, find the best Decision Tree settings, train a final model, test in live, and run a demo. 🎯🖐️")
print("° Feel free to explore: collect data, tune parameters, analyze results, and demo your model live. 🚀")
print("")

# --- Menu --- #
print(" What do you want to do?")
print("📸 1. Collect gestures (MediaPipe Hands).")
print("🤖 2. Train model & find best parameters")
print("🔍 3. Start testing with trained model")
print("   (Make sure you have at least one model already set (test in live))")
print("   (Camera required. Press 'q or ctrl+c' to exit.)")

command = input("Select an option: ")

# Collect hand gesture data using MediaPipe and save to CSV file. The file is overwritten.
if(command == '1'):
    process_images()
# Partial training to find the best tree depth parameter.
elif(command == '2'):
    pre_training(dir_processed)
    best_depth = input("Provide the best tree depth parameter to train the model: ")
    final_training(best_depth, dir_processed)
# Test model accuracy with live camera feed.
elif(command == '3'):
    test_model(dir_model)



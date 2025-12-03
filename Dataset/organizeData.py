import os
import shutil

def organize_dataset(base_path, keywords):
    train_path = os.path.join(base_path, "train")
    val_path = os.path.join(base_path, "validation")
    # Create class folders if not existing
    for folder in [train_path, val_path]:
        os.makedirs(os.path.join(folder, "healthy"), exist_ok=True)
        os.makedirs(os.path.join(folder, "diseased"), exist_ok=True)

    def move_files(path):
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isdir(file_path):
                continue

            fname = file.lower()
            # organizing based on filename (keywords)
            if any(k in fname for k in keywords["healthy"]):
                shutil.move(file_path, os.path.join(path, "healthy", file))
            elif any(k in fname for k in keywords["diseased"]):
                shutil.move(file_path, os.path.join(path, "diseased", file))
            else:
                print(f"Could not classify: {file}")
    # running organizer on both folders (train & validation)
    move_files(train_path)
    move_files(val_path)
    print("Dataset organized successfully!")

# it helps detecting the classes (using related keywords)
keywords = {
    "healthy": ["healthy", "normal"],
    "diseased": ["diseased", "disease", "infected"]
}
base_dataset_path = "/Users/apple/Downloads/VS-code/PlantHealthAI/Dataset"
organize_dataset(base_dataset_path, keywords)
print("done")
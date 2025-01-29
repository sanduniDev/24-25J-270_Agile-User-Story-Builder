import os
from extractor import extract_requirements
from data_loader import load_data
from preprocessor import preprocess_text, load_noise_dataset


def display_results(file_name, tasks, subtasks, nfrs):
    print(f"\n--- Analysis for {file_name} ---")

    if tasks:
        print("\nTasks and Subtasks:")
        for task in tasks:
            print(f"- {task}")
            for subtask in subtasks.get(task, []):
                print(f"  - {subtask}")

        if "Orphaned" in subtasks and subtasks["Orphaned"]:
            print("\nOrphaned Subtasks:")
            for subtask in subtasks["Orphaned"]:
                print(f"  - {subtask}")
    else:
        print("\nNo tasks found.")

    if nfrs:
        print("\nNon-Functional Requirements (NFRs):")
        for nfr in nfrs:
            print(f"- {nfr}")
    else:
        print("\nNo NFRs found.")


def main():
    data_dir = "data/Conversations/"
    if not os.path.exists(data_dir):
        print(f"Error: The directory '{data_dir}' does not exist.")
        return

    # Load all text files
    files = [f for f in os.listdir(data_dir) if f.endswith('.txt')]
    if not files:
        print(f"No conversation files found in '{data_dir}'.")
        return

    # Load noise phrases
    noise_phrases = load_noise_dataset("data/noise_dataset.csv")

    # Process each file
    for file_name in files:
        file_path = os.path.join(data_dir, file_name)
        raw_text = load_data(file_path)

        # Extract tasks, subtasks, and NFRs
        tasks, subtasks, nfrs = extract_requirements(raw_text, noise_phrases)

        # Display results
        display_results(file_name, tasks, subtasks, nfrs)


if __name__ == "__main__":
    main()

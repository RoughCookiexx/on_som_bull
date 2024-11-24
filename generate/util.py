import os


def get_latest_file(directory):
    # Get all files in the directory
    files = [os.path.join(directory, f) for f in os.listdir(directory) if
             os.path.isfile(os.path.join(directory, f))]

    if not files:
        return None  # No files in the directory

    # Find the latest file by modification time
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

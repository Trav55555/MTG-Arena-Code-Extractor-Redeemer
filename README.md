# MTG Arena Code Extractor & Redeemer

This project contains two Python scripts that can be used to extract codes from images of Magic: The Gathering trading cards and input the extracted codes into the Magic: The Gathering Arena application.

## Prerequisites

1. Install Python 3.7 or higher.
2. Install the required Python packages using the following command:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Place your card images in a folder.

2. Run the first script to extract codes from the images:

    ```bash
    python just_use_textract.py <image_folder>
    ```

    Replace `<image_folder>` with the path to the folder containing your card images. The script will generate a `codes.txt` file containing the extracted codes.

3. Run the second script to input the codes into Magic: The Gathering Arena:

    ```bash
    python mtg_arena_code_redeemer.py
    ```

    This script will attempt to launch the MTG Arena application and input the codes from `codes.txt`. If the application is already running, it will connect to the existing instance.

## Troubleshooting

If you encounter issues with coordinates, you can use the `--use-coordinates` or `-u` command-line option when running the second script. This will read the coordinates from a `coordinates.json` file instead of performing OCR on the image files:

```bash
python mtg_arena_code_redeemer.py --use-coordinates
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
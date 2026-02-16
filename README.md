This is a beer walk script I'm building with the google maps API.

This is a python click CLI. The usage is `python3 beer-walk.py --start "<coordinates>" --end "<coordinates>" --density "1km"`.

The idea is, you set the start coordinates, in "x,y" format and the same for the end coordinates, and the CLI will output a list of places to stop for a beer at, stopping at one of the places.

## Getting Started

1. Create a virtual environment and activate it:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the CLI:
   ```
   python3 main.py --start "<coordinates>" --end "<coordinates>" --density "1km"
   ```
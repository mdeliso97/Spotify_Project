### Jacopo Caratti, Marco De Liso
# Spotify Featuring Artists Analysis
Welcome to our Network Analysis project readme file!

In this project, we analyze the Spotify featuring artists collaboration network. Here are the steps to run our project successfully:

## 1. Download the datasets
To get started, please download the three datasets we use for our analysis. You can find the links to download the datasets below:

* [nodes.csv](https://www.kaggle.com/datasets/jfreyberg/spotify-artist-feature-collaboration-network?select=nodes.csv)
* [edges.csv](https://www.kaggle.com/datasets/jfreyberg/spotify-artist-feature-collaboration-network?select=edges.csv)
* [tracks.csv](https://www.kaggle.com/datasets/lehaknarnauli/spotify-datasets?select=tracks.csv)

Make sure to name the datasets exactly as provided above.

## 2. Import the datasets
After downloading the datasets, please import them into the `./Data` directory in the project folder.

## 3. Create a Python virtual environment
Create a python virtual environment:
`python -m venv spotify_env`

Activate the virtual environment:
`source newenv/bin/activate`

## 4. Install the dependencies
`pip install -r requirements.txt`

## 5. Run the project
Now, open the `./spotify_featuring_artists_analysis/main.py` file and install all the Python libraries that are required by the project. Finally, you can run the project by executing this file.

## 6. Outputs
Upon completion of the project run, you will get two kinds of output. The first one is a terminal output containing runtime information about the project such as timings and network structure. The second one is graphical plot images with interesting information and patterns we discovered through our analysis. All the images will be saved in the `./Data/data_visualization` directory.

We hope you find our project insightful and enjoyable!
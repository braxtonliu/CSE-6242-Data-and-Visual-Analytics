## development environment requirement
1. make sure you already installed python3.11 and anaconda in your development environment

## Getting Started

To get started with the Song Recommendation Project, follow these steps:

1. **unzip this project**: uncompress the zip file in your local directory.
2. **set up environment**: Navigate to the project directory and activate the anaconda environment:
   ```
   (1) open anaconda prompt
   (2) cd new_project_6242
   (3) conda create --name new_project_6242
   (4) conda activate new_project_6242
   (5) pip install -r requirements.txt
   ```

3 ** install scikit-surprise package**:
    conda config --add channels conda-forge
    conda config --set channel_priority strict
    conda install scikit-surprise

4. **Run the Application**: Start the application by running the following command:
   ```
      python controller.py
   ```
5. **Access the User Interface**: Open your web browser and navigate to `http://localhost:5000` to access the user interface of the Song Recommendation Project.

6. **project presentation**: https://youtu.be/HOpLKNhk0tw


---

# Song Recommendation Project

Welcome to the Song Recommendation Project! This project aims to provide personalized song recommendations to users based on their music preferences. By leveraging machine learning algorithms and user interaction, the system suggests songs that users are likely to enjoy, thereby enhancing their music listening experience.

## Overview

The Song Recommendation Project utilizes a combination of data processing, machine learning, and user interface components to deliver personalized song recommendations. Here's a brief overview of the project components:

- **Data Collection**: Collects user listening data, including song information and listening history.
- **Data Processing**: Cleans, preprocesses, and analyzes the collected data to extract meaningful features for recommendation.
- **Machine Learning Model**: Trains a recommendation model using various algorithms, such as collaborative filtering, content-based filtering, or hybrid approaches.
- **User Interface**: Provides an intuitive interface for users to interact with the system, input preferences, and receive personalized recommendations.

## Features

- **Personalized Recommendations**: Generates song recommendations tailored to each user's music taste and preferences.
- **User Interaction**: Allows users to provide feedback on recommended songs, influencing future recommendations.
- **Dynamic Updates**: Continuously updates the recommendation model based on user feedback and evolving preferences.

## Notes

Due to GitHub file size limits, the following files are not included in the repository:

- `new_project_6242/models/model_1.pkl` (1.03GB)
- `new_project_6242/data/User_Listening_History.csv` (574MB)

Please contact the authors or refer to course resources to access the full dataset and model.


## Contributing

Contributions to the Song Recommendation Project are welcome! If you'd like to contribute, please follow these guidelines:

- Fork the repository and create a new branch for your feature or bug fix.
- Make your changes and ensure they adhere to the project's coding style and conventions.
- Test your changes thoroughly.
- Submit a pull request with a clear description of your changes and their purpose.


## Acknowledgements

- This project was inspired by the desire to enhance the music listening experience through personalized recommendations.
- Special thanks to the open-source community for providing valuable libraries, frameworks, and tools used in this project.

---


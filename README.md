
# Olympics Data Insights Web App

This web app provides insights into Olympic data using interactive visualizations built with `Streamlit`, `matplotlib`, and `seaborn`. Users can explore various metrics related to Olympic athletes, events, and countries through intuitive charts and graphs.








## About Dataset

This is a historical dataset on the modern Olympic Games, including all the Games from Athens 1896 to Rio 2016.

You can check out the dataset [here](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results).



## 📊 Features

- **Interactive Visualizations**: Explore Olympic data with dynamic visualizations using `matplotlib` and `seaborn`.
- **Country-wise Analysis**: Visualize the performance of countries over time.
- **Event Insights**: Track medal counts across different sports and events.
- **Athlete Analysis**: Dive into athlete-specific statistics such as age, gender, and performance.
- **User-friendly Interface**: Simple and interactive web app hosted on `Streamlit`.




## 🚀 Demo

You can check out the live version of the web app [here](https://olympics-data-insights.streamlit.app/).




## Project Structure
olympics-data-insights-web-app/

````
├── data                  # Directory containing Olympic dataset
├── .gitignore            # Files and directories to be ignored by Git
├── app.py                # Main Streamlit app file
├── favicon.png           # Favicon for the web app
├── helper.py             # Script containing helper functions for the app
├── preprocessor.py       # Script for preprocessing data before analysis               
└── README.md             # Project documentation
````


## 📦 Dependencies

- **Streamlit**: Web framework for creating interactive apps.
- **matplotlib**: Visualization library for plotting charts and graphs.
- **seaborn**: Statistical data visualization library for attractive and informative graphics.
- **pandas**: Data manipulation and analysis.
- **numpy**: Support for large, multi-dimensional arrays and matrices.
## 🛠️ Installation

Follow the steps below to set up and run the project locally:

### Clone the repository:

```bash
git clone https://github.com/xyxuxx/olympics-data-insights-web-app.git
cd olympics-data-insights-web-app
```

### Install dependencies:
Make sure you have Python 3.7+ installed. Then, install the required Python packages:
```bash
pip install -r requirements.txt
```

### Run the app:
Launch the Streamlit web app locally:
```bash
streamlit run app.py
```

### Access the web app: 
Once the server is running, open your browser and navigate to `http://localhost:8501` to explore the app.




    



## 📧 Contact

For any inquiries or suggestions, reach out to me at: [syfullah.shifat@gmail.com](mailto:syfullah.shifat@gmail.com).
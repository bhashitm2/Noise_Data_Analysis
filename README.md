# 🔊 Urban Noise Pollution Monitoring Dashboard

An interactive Streamlit dashboard for analyzing noise pollution levels across major Indian cities.

## 🌟 Features

- **Real-time Data Visualization** - Interactive charts and graphs using Plotly
- **Multi-city Analysis** - Compare noise levels across different Indian cities
- **Temporal Analysis** - Before, during, and after period comparisons
- **Zone-wise Breakdown** - Analysis by Commercial, Residential, and Silence zones
- **Violation Monitoring** - Track compliance with noise pollution limits
- **Station-wise Reports** - Detailed analysis by monitoring stations

## 📊 Data Overview

- **71 monitoring stations** across multiple Indian cities
- **5,006 noise measurement records** spanning multiple years
- **Day and Night noise levels** with corresponding legal limits
- **Zone-based classification** (Commercial, Residential, Silence zones)

## 🚀 Quick Start

### Local Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd noise-data-analysis-main
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

4. Open your browser and navigate to `http://localhost:8501`

## 📁 Project Structure

```
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
└── data/              # Data files
    ├── stations.csv   # Station information
    └── station_month.csv  # Monthly noise measurements
```

## 🌐 Deployment Options

This application can be deployed on various platforms:

- **Streamlit Cloud** (Recommended - Free)
- **Heroku**
- **Railway**
- **Render**
- **Google Cloud Platform**
- **AWS**

## 📈 Usage

1. **Select City**: Choose from available Indian cities
2. **Choose Time Period**: Select month and comparison periods
3. **Filter Zones**: Select specific zone types for analysis
4. **Explore Visualizations**: 
   - Current month overview with key metrics
   - Temporal trends and comparisons
   - Station-wise detailed analysis
   - Violation reports and compliance tracking

## 🎯 Key Insights

The dashboard helps identify:
- Noise pollution hotspots
- Temporal patterns in noise levels
- Zone-wise compliance rates
- Violation trends over time
- Station performance metrics

## 🛠️ Technologies Used

- **Streamlit** - Web app framework
- **Pandas** - Data manipulation
- **Plotly** - Interactive visualizations
- **NumPy** - Numerical computations
- **Matplotlib** - Additional plotting capabilities

## 📊 Data Sources

This project analyzes noise pollution data from monitoring stations across major Indian cities, providing insights into urban noise patterns and compliance with environmental regulations.

## 🤝 Contributing

Feel free to contribute to this project by:
- Adding new features
- Improving visualizations
- Enhancing data analysis
- Fixing bugs

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Your Name** - *Bhashit Maheshwari*

This is an independent project developed for educational and analytical purposes. The dashboard provides insights into urban noise pollution patterns across Indian cities.

## 🙏 Acknowledgments

- Data visualization powered by Plotly and Streamlit
- Noise pollution data from Indian environmental monitoring stations
- Built with modern Python data science libraries

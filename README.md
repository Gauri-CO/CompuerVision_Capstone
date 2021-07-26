**Azure Cloud Data Pipeline for In-Store Retail Traffic Analytics**

**What is Store Traffic Analytics?**

In-store traffic analytics allows data-driven retailers to collect meaningful insights about customer’s behavioral data.
The retail industry receives millions of visitors every year. Along with fulfilling the primary objective of a store, it is can also extract valuable insights from this constant stream of traffic.
The footfall data, or the count of people in a store, creates an alternate source of value for retailers. One can collect traffic data and analyze key metrics to understand what drives the sales of their product, customer behavior, preferences, and related information.

**How does it help store potential?**

**1. Customer Purchase Experience** 
 
Store Traffic Analytics helps provide insights and in-depth knowledge of customer shopping and purchasing habits, their in-store journey, etc., by capturing key data points such as the footfall at different periods, the preferred product categories identifying traffic intensity across departments, among others. Retailers can leverage such analytics to strategize and target their customers such that it enhances customer experience and drive sales.

**2. Customer Dwell Time Analysis**

Dwell time is the length of time a person spends looking at the display or remains in a specific area. It grants an understanding of what in a store holds customer attention and helps in optimizing store layouts and product placements for higher sales.

**3. Demographics Analysis**

Demographic analysis separates store visitors into categories based on their age and gender, aiding in optimizing product listing. For instance, a footwear store footfall analysis shows that the prevalent customers are young men between the age group of 18-25. The information helps the store manager list products that appeal to this demographic group, ensuring better conversion rates.

**4. Human Resource Scheduling**

With the help of store traffic data, workforce productivity can also be enhanced by effective management of staff schedules according to peak shopping times to meet demands and provide a better customer experience, directly impacting operational costs.

**Customer Footfall Data Sources**

The first step for Store Traffic Analytics is to have a mechanism to capture customer footfall data. Methods to count people entering the store (People Counting) have been evolving rapidly. Some of them are as follows –

Manual tracking
Mechanical counters
Pressure mats
Infrared beams
Thermal counters
Wi-Fi counting
Videos Counters

**Project Overview**

This Project is a cloud based implementation of DataPipeline for an AI-based object detection and tracking framework for Video counters using Python, Deep Learning and OpenCV, by leveraging CCTV footage of a store.

Data source : VIRAT Ground Dataset
https://viratdata.org/
Following are the steps involved in creating the Data Pipeline.

1. Upload the video files to Azure Cloud
2. Download the files to local temporary area
3. Execute Yolo Object Detetction Algorithm
4. Upload Annotated videos and files on Azure Blob Storage
5. Trigger the Azure Data Factory Pipeline to save the annoated files data in Azure Cosmos DB

Usage
python AnalyticsPipeline.py

Pre-requisite
User should have Azure account

Software Used:\
-> Programming Language : Python 3.9 \
-> Docker version 20.10.07 \
-> Storage : Cosmos DB and Azure Blob Storage\
-> ETL Tool: Azure Data factory\
-> Scheduling : Trigger in Azure Data factory\
-> Overall Monitoring : Azure Montoring 
-> Monitoring Dashboard Link: \
https://portal.azure.com/#@gauris08gmail.onmicrosoft.com/dashboard/arm/subscriptions/ed9adafd-e391-44da-9704-c3170c3decd7/resourceGroups/dashboards/providers/Microsoft.Portal/dashboards/6e20a63c-9464-4c05-a5ed-d8b066acec11 \

![DataPipeline](https://user-images.githubusercontent.com/75573079/126571428-a29e3b2b-5604-483c-b6ac-c4d1fb42128b.PNG)


Dockerization Steps: \
1. Create docker-build directory on your local system ans copy all the required files in this directory \
2. Run below commands from cmd prompt from docker-build directory \
   docker build --tag python-docker \
   docker run -t -i python-docker \

References Used: \
https://docs.microsoft.com/en-us/azure/iot-central/retail/tutorial-video-analytics-create-app-yolo-v3 \
https://affine.ai/in-store-traffic-analytics-retail-sensing-with-intelligent-object-detection/ \
https://towardsdatascience.com/object-detection-using-yolov3-and-opencv-19ee0792a420 \
https://towardsdatascience.com/object-detection-using-yolov3-on-colab-5d7d9eef02b3 \
https://www.youtube.com/watch?v=enhJfb_6KYU \
https://docs.microsoft.com/en-us/azure/developer/python/sdk/storage/storage-blob-readme?view=storage-py-v12 \
https://docs.microsoft.com/en-us/azure/cosmos-db/create-notebook-visualize-data \
https://app.diagrams.net/#G1co7nBbhtr_6Lm8q1SKttKDXvoauMw6jf \
https://www.sqlshack.com/how-to-use-iterations-and-conditions-activities-in-azure-data-factory/ \
https://www.youtube.com/watch?v=5-SRNiC_qOU \
https://www.youtube.com/watch?v=UZiccUhvWKE


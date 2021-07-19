import yaml

val = input("Enter the path for video files:")
info = [
    {

        'azure_storage_connectionstring' : "DefaultEndpointsProtocol=https;AccountName=retailanalytics08;AccountKey=Vk+/9Z9quDj3p1cY1AIaZ4GrCr+bNgU7JnknY9DpuWlF6o31jWo6wrOSU3rciJs4sxQ0+M8dItaTrhhCgGsJzQ==;EndpointSuffix=core.windows.net",
        'video_container_name': 'videos',
        'source_folder': 'C://Users/gauri/PycharmProjects/ComputerVisionAnalytics',
        'annotatedfiles': 'annotatedfiles',
        'mp4_file_pattern': '^VIRAT[_]S[_]\d{6}[_]\d{2}[_]\d{6}[_]\d{6}[_]\d{8}[\.]mp4$',
        'csv_file_pattern': '^VIRAT[_]S[_]\d{6}[_]\d{2}[_]\d{6}[_]\d{6}[_]\d{8}[\.]csv$',
        'avi_file_pattern': '^VIRAT[_]S[_]\d{6}[_]\d{2}[_]\d{6}[_]\d{6}[_]\d{8}[\.]avi$'

    }
]

with open("config.yaml", 'w') as yamlfile:
    data = yaml.dump(info, yamlfile)
    print("Write successful")
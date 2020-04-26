# lambda
Scripts em python executados no AWS Lambda


#### Rekognition/Watchfolder_Rekognition_Text.py
- Script em python para tratar os arquivos de imagem assim que são depositados em um bucket específico. Esse tratamento se refere a análise e extração de textos através do serviço Amazon Rekognition.


#### Textract/Watchfolder_Textract_image.py
- Script em python para tratar os arquivos de imagem assim que são depositados em um bucket específico. Esse tratamento se refere a análise e extração de textos através do serviço Amazon Textract (sync).


#### Watchfolder_extract_zip.py
- Script em python para tratar os arquivos .zip assim que são depositados em um bucket específico. Esse tratamento se refere ao unzip do arquivo, depositando seu conteúdo em outro diretório.

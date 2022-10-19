# Manual de utilização do scraper localmente no windows

Para rodar em uma máquina windows, é necessário uma instalação do google chrome,
uma instalação de python 3.9, uma instalação de java, e os arquivos
chromedrive.exe e selenium-server-x.x.x.jar.

Para a instalação tanto do python quanto do java, recomendo a utilização do conda,
como mostro no passo a passo abaixo.

1. Instalação do miniconda
    1. https://docs.conda.io/en/latest/miniconda.html
    2. Utilizar primeiro instalador para windows, ou um instalador com versão python 3.9
    3. Durante a instalação, adicionar o miniconda ao path
2. Teste da instalação do miniconda
    1. Se tiver terminais abertos, feche-os
    2. Abra um terminal (cmd)
    3. Teste o comando ```conda -V```, que deve retornar algo do tipo: ```conda 4.10.3```
3. Criação do ambiente conda
    1. Em um terminal, mude para a pasta raiz deste repositório
    2. Crie o ambiente scraping com o comando ```conda create -n scraping python=3.9```
    3. Entre no ambiente com o comando ```conda activate scraping```
    4. Teste a instalação do python com o comando ```python -V```, que deve retornar algo do tipo: ```Python 3.9.13```
4. Instalação dos pacotes do projeto
    1. Se já não estiver ativado, ative o ambiente com o comando ```conda activate scraping```
    2. Instale os pacotes usando o comando ```pip install -r requirements.txt```
5. Instalação do java no ambiente conda
    1. Se já não estiver ativado, ative o ambiente com o comando ```conda activate scraping```
    2. Instale o java com o comando ```conda install -c conda-forge openjdk```
    3. Teste a instalação com o comando ```java -version```, que deve retornar algo do tipo: ```java version "1.8.0_202"...```
6. Download do google driver
    1. Confira a versão do google chrome da sua máquina no link chrome://settings/help
    2. Sua versão deve ser algo do tipo ```Versão 106.0.5249.103 (Versão oficial) 64 bits```
    3. Baixe o chromedriver correspondente à sua versão no link https://chromedriver.chromium.org/downloads
    4. Copie o chromedriver.exe pra a raiz desse repositório
7. Download do selenium server
    1. Baixe o selenium server no link https://www.selenium.dev/downloads/
    2. A versão que utilizei é a 4.5.0, disponível no link https://github.com/SeleniumHQ/selenium/releases/download/selenium-4.5.0/selenium-server-4.5.0.jar
    3. Copie o arquivo .jar para a raiz desse repositório
8. Teste toda a aplicação
    1. Com o ambiente ativado, utilize o comando para ligar o servidor selenium ```java -jar selenium-server-4.5.0.jar standalone --host localhost```
    2. Em outro terminal, ative o ambiente
    3. Utilize o comando para testar a aplicação ```python scraper.py --i input\urls_test.csv```
    4. Verifique a saída na pasta data/ano/mes/dia/*.csv

# Ajuda

1. Instalação do java fora do conda
    1. Baixe alguma versão do java SDK https://www.oracle.com/java/technologies/downloads/#java17
    2. Utilize o vídeo para guiar a instalação e posterior configuração da variável de ambiente
    3. https://www.youtube.com/watch?v=IJ-PJbvJBGs
    4. Se tiver terminais abertos, feche-os
    5. Abra um terminal (cmd)
    6. Teste o comando ```java -version```, que deve retornar algo do tipo: ```java version "1.8.0_202"...```
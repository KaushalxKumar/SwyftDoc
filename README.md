# The University of Sydney
# SwyftDoc - Thesis Project 
**Kaushal Kumar (kkum9480)** 

**480236025**

## About
SwyftDoc is a quantum resistant blockchain-based document certification and verification platform.

## How To Install & Run (Windows)

### Project Components 
Ensure the following applications is installed on your local machine.
* Python - [Python Installation Guide](https://wiki.python.org/moin/BeginnersGuide/Download)
* Truffle - [Truffle Installation Guide](https://trufflesuite.com/docs/truffle/how-to/install/)
* Ganache - [Ganache Installation Guide](https://trufflesuite.com/ganache/)
* IDE - [PyCharm Recommended](https://www.jetbrains.com/pycharm/download/?section=windows)

### Clone Project
```angular2html
$ git clone https://github.com/KaushalxKumar/SwyftDoc.git
```

### 1. Install Django and Python Modules 
Navigate into the inner "SwyftDoc" folder (SwyftDoc\SwyftDoc).
```angular2html
$ pip install -r requirements.txt
```

### 2. Ganache Blockchain
1. Open up the ganache application.
2. Create new workspace and chose and appropriate name.
3. Start Ganache blockchain.

### 3. Deploy Smart Contract
Navigate into the "Truffle" folder (SwyftDoc\Truffle).
Ensure "Host" and "Port" in the "truffle-config.js" file is the same as your Ganache Blockchain.

```angular2html
$ truffle migrate --network development
```

### 4. SendGrid 
1. Create [SendGrid](https://sendgrid.com/) account. 
2. In Settings > API Keys. Create a new API save the key itself.
3. In Settings > Sender Authentication. Verify the ownership of a single email address that you own.
 
### 5. Input Credentials
Navigate into the inner "SwyftDoc" folder (SwyftDoc\SwyftDoc).

1. Open up "credentials.py" and replace the required fields with your own credentials.

If not using the default Ganache URL.
2. Change "ganache_url" in both "certify.py" and "verify.py" files in the Interactions folder (SwyftDoc\SwyftDoc\Interactions) to the URL of your Ganache blockchain.

### 6. Run
Ensure Ganache Blockchain is open and running.

Navigate into the inner "SwyftDoc" folder (SwyftDoc\SwyftDoc).

```angular2html
python manage.py runserver 
```

Open URL in browser
[SwyftDoc](http://127.0.0.1:8000)
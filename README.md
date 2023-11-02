

![Capture d’écran 2023-11-01 220619](https://github.com/m0hss/IkarmaAPI/assets/60576085/f9115c78-7a53-44e2-b89f-984a3c7c3042)



</p>

<a href="https://github.com/tiangolo/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/tiangolo/fastapi/workflows/Test/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/tiangolo/fastapi" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/tiangolo/fastapi.svg" alt="FastAPI">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

- **REST API** serves a desktop app

- **Documentation**: [AWS](http://ec2-16-170-146-217.eu-north-1.compute.amazonaws.com/redoc) || [heroku](https://ec2-16-170-146-217.eu-north-1.compute.amazonaws.com/redoc)
  
## Requirements

- [**FastAPI**;](https://github.com/tiangolo/fastap) a modern, high-performance web framework for building APIs with Python 3.7+ based on standard Python type hints.**
- [**MySQL Connector/Python**](https://dev.mysql.com/doc/connector-python/en/)



## Installation

```bash
$ git clone https://github.com/m0hss/IkarmaAPI.git
$ python -m venv ikapi
$ cp -a /IkarmaAPI/. ikapi
$ pip install -r requirements.txt 
```

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`USER_DATABASE_URL`= ${db_url} (mysql+mysqlconnector://root@localhost:3306/db_name)

`SECRET_KEY`= ${secret_key}

`ALGORITHM`= HS256

`ACCESS_TOKEN_EXPIRE_MINUTES`

## Usage/Examples 

```bash
 $ uvicorn main:app
```


## Documentation

 <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>
 
 <a href="https://github.com/tiangolo/fastap" target="_blank">[https://fastapi.tiangolo.com](https://github.com/tiangolo/fastap)</a>
 
 <a href="https://docs.pydantic.dev/latest" target="_blank">https://docs.pydantic.dev/latest</a>
 
 <a href="https://www.uvicorn.org" target="_blank">https://www.uvicorn.org/</a>
 
 <a href="https://dev.mysql.com/doc/connector-python/en/" target="_blank">MySQL Connector/Python Developer Guide</a>
 
 <a href="https://docs.sqlalchemy.org/en/20/" target="_blank">https://docs.sqlalchemy.org/en/20/</a>
 


## License

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)


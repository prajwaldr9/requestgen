# HTTP REQUEST GENERATOR AND CONVERTER
This package can be used to generate the code to send http requests in several languages.
It can also be used to convert the code from curl to other languages

### Install
```pip install requestgen```
or 
Clone the repo and run the command
```python install setup.py```

### Usage
Convert from Curl to Apache HttpClient Request
```shell script
convert CURL JAVA_APACHE_HTTP_CLIENT, 'curl google.com'
```
or takes input from stdin
```shell script
convert CURL PYTHON_REQUESTS
```

Usage via API
```python
import requestgen

print(requestgen.convert(from_language='CURL', to_language='JAVA_HTTP_URL_CONNECTION',
 input_code='curl google.com'))
```



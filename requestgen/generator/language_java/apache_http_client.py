from requestgen.generator.generator import Generator
from requestgen.parser.curl_parser import CurlParser


class ApacheHttpClientCodeGenerator(Generator):
    cookies_template = "cookies = {{\n{text}}}"
    headers_template = "headers = {{\n{text}}}"
    data_template = "data = '{text}'"
    tab = '    '

    def __init__(self, http_request):
        super().__init__(http_request)

    def generate_import_statement(self):
        self.code += '''import org.apache.http.HttpEntity;
import org.apache.http.HttpHeaders;
import org.apache.http.util.EntityUtils;
import org.apache.http.entity.StringEntity;
import org.apache.http.client.methods.*;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;

import java.io.IOException;'''
        self.code += self.new_lines(2)

    def generate_headers(self):
        text = ''
        d = self.http_request.headers
        if not d:
            return text
        for key, val in d.items():
            text += f'request.addHeader("{key}", "{val}");\n'
        text += self.new_lines(1)
        return text

    def generate_cookies(self):
        text = ''
        d = self.http_request.cookies
        if not d:
            return text
        cookie_val = ''
        for key, val in d.items():
            cookie_val += f'{key}={val}; '
        cookie_val = cookie_val[:-2]
        text += f'request.addHeader("Cookie", "{cookie_val}");'
        text += self.new_lines(2)
        return text

    def generate_call_and_result(self):
        result = '''int responseCode = con.getResponseCode();
System.out.println("Response code: " + responseCode);

InputStreamReader inputStreamReader = null;
if (responseCode >= 200 && responseCode < 400) {
    inputStreamReader = new InputStreamReader(
            con.getInputStream());
} else {
    inputStreamReader = new InputStreamReader(
            con.getErrorStream());
}
BufferedReader in = new BufferedReader(inputStreamReader);
String inputLine;
StringBuilder response = new StringBuilder();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();

System.out.println(response.toString());'''
        self.add(result)

    def generate_connection_statements(self):
        self.code += f'''URL url = new URL("{self.http_request.url}");
HttpURLConnection con = (HttpURLConnection) url.openConnection();'''
        self.code += self.new_lines(2)

    def generate_method_and_data(self):
        method = self.http_request.method
        body = self.http_request.data

        # add the method
        self.add(f'con.setRequestMethod("{method}");')
        self.add(self.new_lines(2))

        # add body if exists
        body_template = '''String jsonInputString = "{}";
try (OutputStream os = con.getOutputStream()) {{
    byte[] input = jsonInputString.getBytes("utf-8");
    os.write(input, 0, input.length);
}}'''
        if body:
            self.add('con.setDoOutput(true);\n')
            self.add(body_template.format(body))
            self.add(self.new_lines(2))

    def get_method(self):
        class_name = f'Http{self.http_request.method.capitalize()}'
        return f'{class_name} request = new {class_name}("{self.http_request.url}");'

    def generate_code(self):
        self.sanitize_input()
        self.generate_import_statement()
        self.code += self.get_method() + self.new_lines(2)
        self.code += self.generate_headers()
        self.code += self.generate_cookies()

        # If body exists
        if self.http_request.data:
            self.code += f'''String input = "{self.http_request.data}";
request.setEntity(new StringEntity(input));'''
            self.code += self.new_lines(2)

        # execute and print the results success and failure
        self.code += '''try (CloseableHttpClient httpClient = HttpClients.createDefault();
    CloseableHttpResponse response = httpClient.execute(request)) {
    System.out.println("Response code: " + response.getStatusLine().getStatusCode());
    HttpEntity entity = response.getEntity();
    if (entity != null) {
        String result = EntityUtils.toString(entity);
        System.out.println(result);
    }
}'''
        self.code += self.check_insecure_connection()
        return self.code

    def check_insecure_connection(self):
        if self.http_request.insecure:
            result = '''
// You have specified -k or --insecure in the input request
// Please follow the steps to enable it
// https://stackoverflow.com/questions/19517538/ignoring-ssl-certificate-in-apache-httpclient-4-3'''
            return result
        return ''

def main():
    curl_command = '''curl -H "Content-Type:application/json" 
    -H "Authorization:Basic token" 
    -H "Cookie: cookie1=cookie_val; cookie2=cookie2_val; "
    -X POST 
    -d "test body" --data-raw "test body2"
    http://example.com/example?a=1&b=2'''
    with open('../input.txt', 'r') as f:
        curl_command = f.read()
    http_request = CurlParser(curl_command).parse()
    generator = ApacheHttpClientCodeGenerator(http_request)
    code = generator.generate_code()
    print(code)
    pass


if __name__ == '__main__':
    main()

# todo Improvements
# curl -o myfile.css https://cdn.keycdn.com/css/animate.min.css download this file and save it

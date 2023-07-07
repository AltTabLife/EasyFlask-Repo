<h2>Welcome to EasyFlask!</h2>

<p>The purpose of EasyFlask is to create template-esque Flask applications while not having brain overload from syntax. Ideally, this will be part of the prototyping section of development, since I find myself creating sections of psuedo-code to map out what it would look like anyways.</p>


<h3>How does it do this?</h3>
  <p>The meat of EasyFlask uses a modified ruamel.yaml parser in html_generator to take html tags like below and automatically turn it into an html document. All tags are ran through a list of current open and closed tags in HTML, filtering out 'attributes' for key-value pairs.</p> 


<h3>Important notes:</h3>
  <ol>
    <li>The main reason for modifying the yaml parser is so it can take duplicate keys. This is the crux of how the html is made.</li>
    <li>This is not able to parse both having a value pair, and attributes for it at the same time due to how the parser works, therefore 'content' elements are required for those. They will work universally, whereas a straight key-value pair will only work at the end of a tree.</li>
    <li>For a full explanation of how the program works, feel free to install and build off the splash_page.yamlish file</li>
  </ol>

Example:

  ```yaml
    title: Splash Page
  ```
  
  and

  ```yaml
  title:
    content:
      text: Splash Page
  ```

  and
  
  ```yaml
  title:
    content:
      text:
        Splash Page
      attributes:
        class: title_class
  ```

  all work, but
  
  ```yaml
  title: Splash Page
    attributes:
      class: title_class
  ```

  does not work.
  

<h3>Example EasyFlask file:</h3>

```yaml
page:
  page_name: Splash_Page
  route_list: ['/','/splash_page']
  html:  
    head:  
      title: Splash Page  
      link:  
        attributes:  
          href: path-to-css  
    body:  
      div:  
        attributes:  
          class: header_class  
        h1: Nobody questions the spammish inspiration  
        p: inspiration inspiration inspiration inspiration inspiration inspiration inspiration   
      br:  
      div:  
        attributes:  
          class: inspiration_realized  
        h2: Conclusion  
        ul:  
          li: You  
          li: Should  
          li: Now  
          li: be  
          li: inspired  
        footer:  
```

<h3>Python Example app.py:</h3>
  
  ```py
  from Flask import Flask, render_template_string  
  from pathlib import Path  
  from EasyFlask.html_generator import HTMLGenerator  

  app = Flask(__name__)  

  @app.route('/')  
  def index():  
    file_in = Path('website_config.yaml')  
    html_generator = HTMLGenerator(file_in)  
    html_output = html_generator.generate_html()  
    return render_template_string(html_output)  
  ```
<h3>What's coming to EasyFlask next?</h3>
  <p>I fully understand it's in a state that I wouldn't even use it over just jinja2 at the moment after the inital generation. The next few major updates are designed to add the following.</p>
  <ul>
    <li>Jinja2 compatability for cutting down further on the amount of individual elements needed while maintaining logic capabilities</li>
    <li>Live edit mode to be able to change the config file and have it change the website on file-save (thankfully flask's debug mode should make this pretty easy)</li>
    <li>Source builder file to output the code being run to a source folder of your choosing, for the times there is website specific functionality that hasn't been accounted for yet.</li>
    </ul>
    
<h3>So you're ready to install EasyFlask?</h3>  
  <p>All you need to do is a standard install by</p>
    <ol>
    <li>Cloning the repo with git</li>
    <li>cd into the EasyFlask-Repo</li>
    <li>run "pip install dist/EasyFlask-1.0.tar.gz"</li>
    </ol>

  <p>If you're not worried about modifying the repo with your own improvements, feel free to download just the .tar.gz and install as normal with pip.</p>

<h2>Basic Jinja3 Parsing</h2>

<h3>Overview</h3>
<p>This update is mainly to introduce Jinja with a syntax that can be modified off of. In the next update, there will be the start of a way to add custom jinja-html as includes from other files to help speed up development.</p>

<h3>Important Notes</h3>
<ul>
<li>
For clarity's sake, 2 different forms of the jinja keyword are distinguished. Ones that would be interacting with direct python scripts (namely app.py), are under the page keyword. Ones that would be coded directly in the html templates are used by the other.
<p>For Example:</p>

```yaml
page:
  jinja: ##Denotes first jinja type
  html:
    body:
      jinja: ##Denotes second jinja type
```
</li>
<li>
For now, Sub-Keywords will be parsed like the intended function
<p>For Example:</p>

```py
jinja.Environment.add_extension(extension)
```

Becomes

```yaml
jinja:
  Environment:
    add_extension:
      extension: "*value"
```

Any exceptions to this rule will be documented below.
</li>
<li>
For mainstream jinja-html programming, the "content" Sub-Keyword will transfer 1 to 1 with the proper formatting around it.
</li>
</ul>

<h3>Function Dependencies</h3>
This module is intended to be completely independent of other modules in the current moment. html_generator will need to be modified with a pass-through ability for the jinja blocks.
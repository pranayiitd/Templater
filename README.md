Usage
====
<code>
 $templater template data output
</code>

+ template: path to source code (html + code)
+ data: path to data in json
+ output: path to the resultant output html

Sample command to run.
<code>
$templater template.panoramatemplate data.json output.html
</code>

Assumption
=========

+ Syntax handled in engine : text html. variables and for loop (EACH)
+ Nearest Local variable will be in scope in case of conflict

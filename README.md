Usage
====
$templater template data output

template : location the source code(html + code)
data : data in json
output: location to dump the resultant html

Sample command to run.
$templater template.panoramatemplate data.json output.html

Assumption
=========

+ Syntax handled in engine : text html. variables and for loop (EACH)
+ Nearest Local variable will be in scope in case of conflict.
+

-> Model: QuizResult

id = 1

date = 2014-03-05 23:33:42.764601+00:00

hash = 8a110e259e43ca938f15c46ca3e0d1c11e8de64ac3cdebb936121cf82bdc7d46

log = Show solution of task None of collection None.
Show solution of task None of collection None.
Show solution of task None of collection None.
--- Reset session to allow a new quiz. ---
Show  task 0 of collection 1.
Show solution of task 0 of collection 1.
Show  task 1 of collection 1.
Show solution of task 1 of collection 1.
Show final page.

- - - 

id = 2

date = 2014-03-05 23:34:55.137659+00:00

hash = 5b5ba5065a758d583c9aedd384a4d1e672c2753e1f0e8d1a7199c5596133045d

log = --- Reset session to allow a new quiz. ---
Show  task 0 of collection 2.
Show solution of task 0 of collection 2.
Show solution of task 0 of collection 2.
Show  task 1 of collection 2.
Show solution of task 1 of collection 2.
Show final page.

- - - 

id = 3

date = 2014-03-05 23:37:01.901930+00:00

hash = 89412ee8b5f8147c45d5dec6795c2c45bd49e671effda023bfb50cb8838aba69

log = --- Reset session to allow a new quiz. ---
Show  task 0 of collection 3.
Show  task 1 of collection 3.
Show final page.

- - - 

- - - - - - - 

- -> Model: TC_Membership

id = 1

task = T001: sympy Grundfunktionen

group = T001: demo1

ordering = 0

- - - 

id = 2

task = T002: Lineare Algebra 1

group = T001: demo1

ordering = 1

- - - 

id = 3

task = T001: sympy Grundfunktionen

group = T002: demo2 (no solutions)

ordering = 0

- - - 

id = 4

task = T002: Lineare Algebra 1

group = T002: demo2 (no solutions)

ordering = 1

- - - 

id = 5

task = T001: sympy Grundfunktionen

group = T003: demo3 (no results)

ordering = 0

- - - 

id = 6

task = T002: Lineare Algebra 1

group = T003: demo3 (no results)

ordering = 1

- - - 

- - - - - - - 

- -> Model: Task

id = 1

author = ck

title = sympy Grundfunktionen

revision = 7

pub_date = 2014-03-05 22:56:13+00:00

body_data = {"segments":[{"content":"<p>Gegeben Sei folgender Quelltext:</p>","type":"text"},{"content":"import sympy as sp\nfrom sympy import sin, cos\na, x, y = sp.symbols('a x y')","type":"source"},{"content":"<p>Vervollst&auml;ndingen Sie jeweils das Code-Fragment so, dass die Ausgabe mit dem Kommentar &uuml;bereinstimmt. (Die Sterne sind zu ersetzen!)</p>","type":"text"},{"type":"input","content":[{"content":"Achtung","type":"text"}],"answer":{"content":"r = a*(x+y)\nr2 = sp.******(r)\nprint r2 # a*x + a*y","type":"source"},"solution":[{"content":"r = a*(x+y)\nr2 = sp.expand(r)\nprint r2 # a*x + a*y","type":"source"},{"content":"lsg2","type":"source"},{"content":"lsg3","type":"text"}]},{"type":"input","content":[{"content":"","type":"text"}],"answer":{"content":"r = sin(y)**2 + cos(y)**2\nr2 = sp.******(r)\nprint r2 # 1\n\n","type":"source"},"solution":[{"content":"r = sin(y)**2 + cos(y)**2\nr2 = sp.trigsimp(r)\nprint r2 # 1","type":"source"},{"content":"r = sin(y)**2 + cos(y)**2\nr2 = sp.simplify(r)\nprint r2 # 1","type":"source"}]},{"type":"input","content":[{"content":"Hinweis 2","type":"text"}],"answer":{"content":"r = 5*x**3 + 7*x -a\nr2 = sp.****(***)\n# Ableitung nach x:\nprint r2 # 15*x**2 + 7","type":"source"},"solution":[{"content":"r = 5*x**3 + 7*x -a\nr2 = sp.diff(r, x)\n# Ableitung:\nprint r2 # 15*x**2 + 7","type":"source"}]}]}

- - - 

id = 2

author = ck

title = Lineare Algebra 1

revision = 7

pub_date = 2014-03-05 23:10:15+00:00

body_data = {"segments":[{"content":"<p>Gegeben sei die Matrix</p>\n<p>$$A = \\left(\\begin{array}{ccc}<br />3 &amp; 2 &amp; 0\\\\<br />0 &amp; -1 &amp; 5\\\\<br />\\end{array}\\right)$$</p>\n<p>Beantworten Sie folgende Fragen bzw. markieren Sie wahre Aussagen:</p>","type":"text"},{"type":"check","content":[{"content":"$A$ ist regulär.","type":"text"}],"solution":false},{"content":"<p><strong>Fakt: </strong>Nur quadratische Matrizen k&ouml;nnen regul&auml;r sein.</p>","type":"text","comment":true},{"type":"check","content":[{"content":"Die Spalten von $A$ sind linear abhängig.","type":"text"}],"solution":true},{"type":"check","content":[{"content":"$\\mathrm{ker} A = \\{0\\}$.","type":"text"}],"solution":true},{"type":"input","content":[{"content":"$\\mathrm{rank}(A)=$","type":"text"}],"answer":{"content":"","type":"text"},"solution":[{"content":"2","type":"text"}]},{"type":"check","content":[{"content":"$A$ ist injektiv.","type":"text"}],"solution":false},{"type":"check","content":[{"content":"$A$ ist surjektiv.","type":"text"}],"solution":true}]}

- - - 

id = 3

author = ck

title = Mut zur Lücke

revision = 13

pub_date = 2014-04-12 10:02:49+00:00

body_data = {"segments":[{"content":"<p>F&uuml;lle aus</p>","type":"text"},{"type":"input","content":[{"content":"Wie heißt die Server-Software","type":"text"}],"answer":{"content":"dj","type":"text"},"solution":[{"content":"django","type":"text"}]},{"content":"<p>18: Das ist ein L&uuml;ckentext. D.h. es befinden sich&nbsp;&para;|345|L&uuml;cken|Fehlstellen|Auslassungen&para; im Text. Und hier &para;murx|noch&para; eine.</p>","type":"gap-fill-text","solution":[{"type":"gapTextSolution","answer":"","solutions":["345"]},{"type":"gapTextSolution","answer":"murx","solutions":["noch"]}]}]}

- - - 

- - - - - - - 

- -> Model: TaskCollection

id = 1

author = ck

title = demo1

exam_mode = 0

- - - 

id = 2

author = ck

title = demo2 (no solutions)

exam_mode = 1

- - - 

id = 3

author = ck

title = demo3 (no results)

exam_mode = 2

- - - 

- - - - - - - 

- 
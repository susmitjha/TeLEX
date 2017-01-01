from parsimonious import Grammar, NodeVisitor
from collections import namedtuple 

#Bug reports
#templogicdata =  'G[0,2] F[b? 3;3,  a? 4;4](x1 > 2)' works but templogicdata =  'G[0,2]F[b? 3;3,  a? 4;4](x1 > 2)' does not
    
grammar_text = (r''' 
formula = ( _ globally _) / ( _ future _ ) / ( _ expr _ ) / ( _ paren_formula _)
paren_formula = "(" _ formula _ ")"
globally = "G" interval formula
future = "F" interval formula
interval = _ "[" _ bound  _ "," _ bound _ "]" _
expr = or / and / implies / npred / pred 
or = "(" _ formula _ "|" _ formula _ ")"
and = "(" _ formula _ "&" _ formula _ ")"
implies = "(" _ formula _ "->" _ formula _ ")"
npred = "!" _ formula 
pred = constraint / atom 
constraint =  term _ relop _ bound _
term = infix / var
infix = "{" _ term _ arithop _  term _ "}"
var = _ id _
atom = _ id _
bound = param / num 
param =  id "?" _ num ";" num _ 
id = ~r"[a-zA-z\d]+"
num = ~r"[\+\-]?\d*(\.\d+)?"
relop = ">=" / "<=" / "<" / ">" / "=="
arithop = "+" / "-" / "*" / "/"
_ = ~r"\s"*
''')

_grammar = Grammar(grammar_text)
 
class TLVisitor(NodeVisitor):

    def visit_formula(self, node, children):
        return children[0][1]

    def visit_paren_formula(self, node, children):
        return children[2]

    def visit_globally(self, node, children):
        _, interval, formula = children
        return Globally(interval, formula)
        
    def visit_future(self, node, children):
        _, interval, formula = children
        return Future(interval, formula)

    def visit_interval(self, node, children):
        _, _, _, left, _, _, _, right, _, _, _  = children
        return Interval(left, right)

    def visit_expr(self, node, children):
        return children[0]

    def visit_or(self, node, children):
        _, _, left, _, _, _, right, _, _ = children
        return Or(left, right)

    def visit_and(self, node, children):
        _, _, left, _, _, _, right, _, _ = children
        return And(left, right)

    def visit_implies(self, node, children):
        _, _, left, _, _, _, right, _, _ = children
        return Implies(left, right)

    def visit_npred(self, node, children):
        _, _, right = children
        return Not(right)

    def visit_pred(self, node, children):
        return children[0]

    def visit_constraint(self, node, children):
        left, _, relop, _, right, _ = children
        return Constraint(relop, left, right)
    
    def visit_term(self, node, children):
        return children[0]

    def visit_infix(self, node, children):
        _, _, left, _, arithop, _, right, _, _ = children
        return Expr(arithop, left, right)

    def visit_atom(self, node, children):
        return Atom(children[1])

    def visit_var(self, node, children):
        return Var(children[1])
    
    def visit_bound(self, node, children):
        return children[0]

    def visit_param(self, node, children):
        name, _, _, left, _, right, _ = children
        return Param(name, left, right)

    def visit_id(self, node, children):
        return node.text

    def visit_num(self, node, children):
        return Constant(node.text)

    def visit_relop(self, node, children):
        return node.text

    def visit_arithop(self, node, children):
        return node.text

    def generic_visit(self, node, children):
        if children:
            return children

class Globally(namedtuple('G',['interval','subformula'])):
    def children(self):
        return [self.subformula]
    def __repr__(self):
        return "G{}{}".format(self.interval, self.subformula)
    
class Future(namedtuple('F',['interval','subformula'])):
    def children(self):
        return [self.subformula]
    def __repr__(self):
        return "F{}{}".format(self.interval, self.subformula)

class Interval(namedtuple("Interval", ['left','right'])):
    def __repr__(self):
        return "[{},{}]".format(self.left, self.right)
    def children(self):
        return [self.left, self.right]

class Or(namedtuple("Or",["left", "right"])):
    def __repr__(self):
        return "({} | {})".format(self.left, self.right)
    def children(self):
        return [self.left,self.right]

class And(namedtuple("And",["left", "right"])):
    def __repr__(self):
        return "({} & {})".format(self.left, self.right)
    def children(self):
        return [self.left,self.right]

class Implies(namedtuple("Implies",["left", "right"])):
    def __repr__(self):
        return "({} => {})".format(self.left, self.right)
    def children(self):
        return [self.left,self.right]

class Not(namedtuple("Negation", ['subformula'])):
    def __repr__(self):
        return "(! {})".format(self.subformula)
    def children(self):
        return [self.subformula]

class Constraint(namedtuple("Constraint",["relop", "term", "bound"])):
    def __repr__(self):
        return "({} {} {})".format(self.term, self.relop, self.bound)
    def children(self):
        return [self.term, self.bound]
    
class Expr(namedtuple("Var", ["arithop", "left", "right"])):
    def __repr__(self):
        return "{{{}{}{}}}".format(self.left, self.arithop, self.right)
    
class Atom(namedtuple("Atom", ["name"])):
    def __repr__(self):
        return "{}".format(self.name)

class Var(namedtuple("Var", ["name"])):
    def __repr__(self):
        return "{}".format(self.name)

class Param(namedtuple("Param", ["name", "left", "right"])):
    def __repr__(self):
        return "{}?[{},{}]".format(self.name, self.left, self.right)

class Constant(float):
    pass




def parse(tlStr):
    return TLVisitor().visit(_grammar["formula"].parse(tlStr))
    #return _grammar["formula"].parse(tlStr)


      

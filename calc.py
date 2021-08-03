from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.properties import ObjectProperty

class Calc(BoxLayout):
    display_lb = ObjectProperty(None)
    equate_to_lb = ObjectProperty(None)
    delete = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(Calc, self).__init__(**kwargs)
        self.equation = ""
        self.operations = ["X", "÷", "-", "+"]
        self.operation_coloration = ("[color=33FF33]", "[/color]")
        self.closing_brackets = False
        self.bracket_counter = 0
        self.negative = False
        self.equals_pressed = False

    def numeric_selection(self, number):
        if self.equation != "": 
            if self.equation[-1] in self.operations:
                self.equation += " "
            if self.bracket_counter > 0:
                print("HITT")
                self.closing_brackets = True
            if self.equation[-1] == ")" or self.equation[-1] == "π":
                self.operation_selection("X ")
                self.closing_brackets = True

        self.equation += str(number)
        if any(op in self.equation for op in self.operations):
            self.pre_evaluate()
        self.delete.disabled = False
        self.display_equation()
        print(self.equation, "num")

    def operation_selection(self, operation):
        if self.equation != "" and self.equation[-1] != "(" and self.equation[-1] != "~":
            if self.equation[-1] != operation and self.equation[-1] in self.operations:
                self.equation = self.equation[:-1]
                self.equation += operation
            elif self.equation[-1] != operation:
                self.equation += " " + operation
            self.closing_brackets = False
            self.negative = False
        self.display_equation()
        self.equate_to_lb.text = ""
        print(self.equation, "op")

    def backspace(self):
        if self.equation[-1] == "(":
            self.bracket_counter -= 1
        elif self.equation[-1] == ")":
            self.bracket_counter += 1
        elif self.equation[-1] == "~":
            self.negative = False

        self.equation = self.equation[:-1]
        if self.equation != "" and self.equation[-1] == " ":
            self.equation = self.equation[:-1]
        
        if self.equation != "":
            if self.equation[-1] in self.operations:
                self.closing_brackets = False
                self.equate_to_lb.text = ""
            else:
                self.closing_brackets = True
                if self.bracket_counter == 0:
                    self.closing_brackets = False

                if self.equation[-1] == "(" or self.equation[-1] == "~":
                    self.equate_to_lb.text = ""
                else:
                    self.pre_evaluate()
            
            last_value = self.equation.split(" ")[-1]
            if last_value[-1].isdigit():
                for i in range(len(last_value)-1, -1, -1):
                    if last_value[i] == "~":
                        self.negative = True
                        break
                    elif last_value[i] == ")":
                        self.negative = False
                        break

        if self.equation == "":
            self.equate_to_lb.text = ""
            self.closing_brackets = False
            self.bracket_counter = 0
            self.delete.disabled = True

        if not any(op in self.equation for op in self.operations):
            if "π" in self.equation:
                self.display_equation()
            else:
                self.equate_to_lb.text = ""
        self.display_equation()
        print(self.equation, "backspace")

    def pi(self):
        if self.equation == "":
            self.equation += "π"
        else:
            if self.equation[-1] == "(" or self.equation[-1] == "~":
                self.equation += "π"
                self.closing_brackets = True
            elif self.equation[-1] == ")" or self.equation[-1] == "." or self.equation[-1].isdigit():
                self.operation_selection("X ")
                self.equation += "π"
                self.closing_brackets = True
            elif self.equation[-1] in self.operations:
                self.equation += " π"
        print(self.bracket_counter, self.closing_brackets)
        self.pre_evaluate()
        self.delete.disabled = False
        self.display_equation()


    def brackets(self):
        if self.closing_brackets:
            self.equation += ")"
            self.bracket_counter -= 1
            if self.bracket_counter == 0:
                self.closing_brackets = False
                self.pre_evaluate()
                self.negative = False
        else:
            if self.equation != "": 
                if self.equation[-1] in self.operations:
                    self.equation += " "
                if self.equation[-1] == ")" or self.equation[-1].isdigit() or self.equation[-1] == ".":
                    self.operation_selection("X ")
            self.equation += "("
            self.bracket_counter += 1
            self.equate_to_lb.text = ""

        self.display_equation()
        self.delete.disabled = False
        print(self.equation, "brackets")

    def negative_positive(self):
        if self.negative:
            for i in range(len(self.equation)-1,-1,-1):
                if self.equation[i] == "~":
                    self.equation= self.equation[:i-1] + self.equation[i+1:]
                    break
            self.bracket_counter -= 1
            if self.bracket_counter == 0:
                self.closing_brackets = False
            self.negative = False
        else:
            if self.equation != "": 
                if self.equation[-1] in self.operations:
                    self.equation += " "
                if self.equation[-1] == ")" or self.equation[-1] == "%":
                    self.operation_selection("X ")
                if self.equation[-1].isdigit() or self.equation[-1] == "π":
                    splice = self.equation.split(" ")
                    last_value = splice[-1]
                    splice.pop(-1)
                    current = ""
                    for i, strings in enumerate(last_value):
                        if strings != "(":
                            current += "(~" + last_value[i:]
                            break
                        current += strings
                    self.equation = " ".join(splice) + " " + current
                    self.closing_brackets = True
                    self.bracket_counter += 1
                    self.negative = True     
                    print("hit")
                    self.pre_evaluate()              
            if not self.negative:
                self.equation += "(~"
                self.bracket_counter += 1
            self.negative = True
            self.delete.disabled = False
        
        self.display_equation()
        if any(op in self.equation for op in self.operations) and self.equation[-1] != "~":
            self.pre_evaluate()   
        print(self.equation, "Neg")

    def decimals(self):
        splice = self.equation.split(" ")
        last_value = splice[-1]
        if "." not in last_value:
            if self.equation == "":
                self.equation += "0."
            elif last_value[-1] == "(" or last_value[-1] == "~":
                self.equation += "0."
                self.closing_brackets = True
            elif last_value[-1] == ")":
                self.operation_selection("X ")
                self.equation += "0."
            elif last_value in self.operations:
                self.equation += " 0."  
            elif last_value[-1].isdigit():
                self.equation += "."

        if any(op in self.equation for op in self.operations):
            self.pre_evaluate()      
        self.delete.disabled = False
        self.display_equation()
        print(self.equation, " dec")

    def pre_evaluate(self):
        fixed = self.equation.replace("~", "-").replace("X", "*").replace("÷","/").replace("π", "3.1415926536")
        if self.closing_brackets:
            for i in range(self.bracket_counter):
                fixed += ")"
        print(fixed)
        total = str(eval(fixed))
        if float(total).is_integer():
            total = str(int(float(total)))
        self.equate_to_lb.text = total

    def equals(self):
        if self.equate_to_lb.text != "":
            self.equation = self.equate_to_lb.text
            self.display_lb.text = "[size=40]" + self.operation_coloration[0] + self.equation + self.operation_coloration[1] + "[/size]"
            self.closing_brackets = False
            self.bracket_counter = 0
            self.negative = False
            self.equate_to_lb.text = ""
    
    def clear(self):
        self.equation = ""
        self.closing_brackets = False
        self.bracket_counter = 0
        self.negative = False
        self.equate_to_lb.text = ""
        self.display_lb.text = ""
        self.delete.disabled = True

    def display_equation(self):
        self.display_lb.text = ""
        for chars in self.equation:
            if chars == " ":
                continue
            elif chars == "~":
                self.display_lb.text += self.operation_coloration[0] + "-" + self.operation_coloration[1]
                continue
            elif chars in self.operations or chars == "%" or chars == "(" or chars == ")" or chars == "π":
                self.display_lb.text += self.operation_coloration[0] + chars + self.operation_coloration[1]
                continue
            self.display_lb.text += chars


class CalcApp(App):
    def build(self):
        return Calc()


CalcApp().run()
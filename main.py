from flask import Flask, send_file,request,jsonify
import schemdraw
from schemdraw.flow import *



app = Flask(__name__)


@app.route("/")
def welcome():
    return 'This is your flask application hosted'
    


@app.route('/custom_graph',methods=['POST'])
def custom_graph():
    data = request.json
    if data.get("start") is None:
        return "No start or End of the workflow was given"
    
    with schemdraw.Drawing() as d:
        d += Start().label("Start")
        d += Arrow().down(d.unit / 2)

        for step, value in data["steps"].items():
            if step == "Decision":
                if len(value) != 3:
                    return "Invalid decision format. It should be a list with two elements.", 400
                
                d+= (decision := Decision(w = 5, h= 5,S = "True",E = "False").label(value[0]))
                d += Arrow().down(d.unit / 2)
                d+= (true := Box(w = 5).label(value[1]))
                d += Arrow().down(d.unit / 2)
                d+= Arrow().right(d.unit).at(decision.E)
               
                #false box and then add 1 arrow down and then 1 to the left
                d+= (false := Box(w = 5).label(value[2]))
                d+= Arrow().down(d.unit*2.5).at(false.S)
                d+= Arrow().left(d.unit*2.15)
               
                  
               
            else:
                d += Box(w=4).label(value)
                d+= Arrow().down(d.unit)
                
            

        d += Ellipse().label("End")
        image_bytes = d.get_imagedata('svg')

    return image_bytes, {"Content-type": "image/svg+xml"}
    #return jsonify(data)

@app.route('/graphs')
def func_factory():
    with schemdraw.Drawing(show=False) as d:
   
    
        d+= Start().label("Start")
        d+= Arrow().down(d.unit/2)
        #Input the string 
        d+= Data(w = 4).label("Enter a string:\n string")
        d+= Arrow().down(d.unit/2)
        
        #Reverse the string
        d+= Box(w = 4).label("Reverse the string:\n reverse_string")
        d+= Arrow().down(d.unit/2)
        
        #Check if string and reverse_string are same
        d+= (decision := Decision(w = 5, h= 5,S = "True",E = "False").label("Is \n string\n == \nreverse_string?"))
        
        #If True
        d+= Arrow().length(d.unit/2)
        d+= (true := Box(w = 5).label("string is a palindrome."))
        d+= Arrow().length(d.unit/2)
        
        #End program
        d+= (end := Ellipse().label("End"))
        
        #If False. Start the arrow from East of decision box
        d+= Arrow().right(d.unit).at(decision.E)
        
        #false is referring to the box where string is not a palindrome.
        d+= (false := Box(w = 5).label("string is not\n a palindrome."))
        
        #Add a downward arrow from the South of false box 
        d+= Arrow().down(d.unit*2.5).at(false.S)
        
        #Extend the arrow to reach the end of the program
        d+= Arrow().left(d.unit*2.15)
        image_bytes = d.get_imagedata('svg')
    
    # Return the SVG content as a response
    return image_bytes, 200, {'Content-Type': 'image/svg+xml'}

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)

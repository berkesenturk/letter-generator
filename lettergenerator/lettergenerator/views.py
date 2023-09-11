from django.http import HttpResponse
import requests
import logging
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG) 

@csrf_exempt
def index(request):
    # response = ""
    # if request.method == "POST":
    #     try:
    #         response += requests.post('https://lettergenerator.onrender.com/coverletter', data = request.POST)
    #     except Exception as ex:
    #         logger.error(f"Something terrible with request/response. Exception message: {ex}")
    #         # Redisplay the question voting form.
    #         return render(
    #             request,
    #             "lettergenerator/",
    #             {
    #                 "error_message": f"Something terrible. Exception: {ex}",
    #             },
    #         )
    
    return HttpResponse("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Two Pane Layout</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: space-between;
            padding: 20px;
        }
        .left-pane {
            flex: 1;
            padding: 10px;
            border: 1px solid #ccc;
            margin-right: 10px;
        }
        .right-pane {
            flex: 1;
            padding: 10px;
            border: 1px solid #ccc;
        }
        .grid-container {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
        }
        .grid-item {
            width: 100%;
            padding: 5px;
            margin: 20px 0
        }
        .label {
            text-align: left;
            padding-right: 5px;
            margin: 20px 0
        }
        .resizer {
            width: 5px;
            background-color: #ccc;
            cursor: col-resize;
            position: absolute;
            top: 0;
            bottom: 0;
            z-index: 1;
        }
                        
        div {
            margin-top: 27px;
        }
        #serializearray, #serialize {
            background-color: #eee;
            border: 1px solid #111;
            padding: 3px;
            margin: 9px;
        }
    </style>
    
    <script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>

                        
    <script>
                            
        //checks for the button click event
            $(document).ready(function() {
                $("#submit-form").click(function(e) {

                console.log("submitted data", JSON.stringify($('#form_letter').serializeArray()))
                var jsonRequest;

                if (JSON.stringify($('#form').serializeArray()) != undefined) {
                    jsonRequest = parseFieldsAndValues($('#form_letter').serializeArray());
                }

                alert(jsonRequest);
                console.log("sent", JSON.stringify(jsonRequest));
  

                $.ajax({
                    type: "POST",
                    url: "https://lettergenerator.onrender.com/coverletter",
                    data: JSON.stringify(jsonRequest),
                    crossDomain: true,
                    contentType: "application/json; charset=utf-8",
                    beforeSend: function() {
                    $(".submit").show().html("<center><img src='images/loading.gif'/></center>");
                    },

                    //if received a response from the server
                    success: function(response) {
                    alert(response);
                    console.log("response", response);
                    $("#resultPane").append(response);
                    }
                });

                e.preventDefault();

                var update = function() {
                    // console.log("data", JSON.stringify($('#form_letter').serializeArray()))
                    var jsonRequest;

                    if (JSON.stringify($('#form_letter').serializeArray()) != undefined) {
                    jsonRequest = parseFieldsAndValues($('#form_letter').serializeArray());
                    }
                    // console.log(jsonRequest);  
                    $('#serializearray').text(
                    JSON.stringify($('#form_letter').serializeArray())
                    );
                    $('#serialize').text(
                    //JSON.stringify($('#form_letter').serialize())
                    JSON.stringify(jsonRequest)
                    );

                    console.log("request", JSON.stringify(jsonRequest));


                    update();
                    $('form').change(update);
                };


                });
                var parseFieldsAndValues = function(json) {

                // console.log("data taken", typeof json, json);
                var jsonRequest = {
                    args: {},
                    letter: {},
                    email: {}
                };

                var letter = json.filter((data) => data.name === "letter");
                var email = json.filter((data) => data.name === "email");
                var args = json.filter((data) => data.name.includes("input"));

                var values = args.map((data) => data.value)
                
                for(let i = 0; i < values.length; i++) {
                    // key
                    if (i % 2 == 0) {
                        jsonRequest.args[values[i]] = "";
                    } 
                    else {
                        jsonRequest.args[values[i - 1]] = values[i];              
                    }
                }    
                        
                letter.map((data) => jsonRequest.letter = data.value);
                email.map((data) => jsonRequest.email = data.value);

                return jsonRequest
                }
            });
                        

    </script>

</head>
<body>
    <div class="left-pane">
      <form id="form_letter" name="form_letter" method="POST">
        <textarea rows="10" style="width: 100%;" name = "letter" placeholder="Large Textbox"></textarea>
        <div class="grid-container">
            <div class="label">Field 1:</div>
            <div class="grid-item" ><input type="text" name="input1" placeholder="key"></div>
            <div class="grid-item"><input type="text"  name="input2" placeholder="value"></div>
            <div class="label">Field 2:</div>
            <div class="grid-item"><input type="text" name="input3" placeholder="key"></div>
            <div class="grid-item"><input type="text" name="input4" placeholder="value"></div>
            <div class="label">Field 3:</div>
            <div class="grid-item"><input type="text" name="input5" placeholder="key"></div>
            <div class="grid-item"><input type="text" name="input6" placeholder="value"></div>
        </div>
        <div style = "margin-top: 10px">
        <div class="label">Email:</div>
        <input type="email" style="width: 100%;" type="email" name="email" placeholder="Additional Input" value = "berkesenturk11@gmail.com">
        </div>
      
        <button type="button" id="submit-form"> Submit </button>

        </form>
        
        <!--               
            <div>$('form').serializeArray():</div>
            <div id=serializearray>asfdg</div>
            <div id=serialize>asfdg</div>
        --> 
    </div>
    
    <div class="right-pane">
        <textarea id="resultPane" rows="10" style="width: 100%;"  placeholder="Right Textbox"></textarea>
        
    </div>
</body>
</html>

""")



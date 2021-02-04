// Bot_Q - Question : Yes/No
// Bot_N - Next reply to be send by user.Auto replies.Eg next leave application
// Bot_L - List of replies.No Buttons. Eg List of jobs
//Bot_C - Choices. Choose one from the given as reply.
console.log("Hey New")
var input = document.getElementById("input-content");
//----------
box = document.getElementById("chatbox")
var send = document.createElement("div");
send.setAttribute("class","d-flex flex-row");
var msgbox = document.createElement("div");
msgbox.setAttribute("class","recbox");
var msg = document.createTextNode("Hey. I am you assistant here ! How can I help you ? ");
msgbox.appendChild(msg);
send.appendChild(msgbox);
box.appendChild(send);
//---------
var buttons =[];
var flexbox =document.createElement("div")
flexbox.setAttribute("class","d-flex flex-wrap")


var suggetions = ["Ecommerce","Blog","Portfolio","iOS","IoT","Android","Services","Location"]
length =suggetions.length
for (i=0;i<length;i++)
{
  var msgbox = document.createElement("div");
  var button = document.createElement("BUTTON");
  button.setAttribute("class","btn")// btn-success")
  button.setAttribute("class",'btn-outline-info')
  button.textContent = suggetions[i];
  buttons.push(button)
  msgbox.appendChild(button);
  flexbox.appendChild(msgbox);
}
for ( var i = 0; i < length; i++ ) (function(i){ 
  buttons[i].onclick = function() {
    sendMessage(suggetions[i])
    console.log(suggetions[i])

  }
})(i);
box.append(flexbox)

function commonButtons(commonList,style)
{
  buttonsList=[];
  console.log("Common Buttons")
  var commonFlexbox =document.createElement("div")
  commonFlexbox.setAttribute("class",style)
  for(i=0;i<commonList.length;i++)
  {
    var msgbox = document.createElement("div");
    var button = document.createElement("BUTTON");
    button.setAttribute("class","btn")
    button.setAttribute("class",'btn-outline-info')
    button.textContent = commonList[i];
    buttonsList.push(button)
    msgbox.appendChild(button);
    commonFlexbox.appendChild(msgbox);
  }
  for ( var i = 0; i < buttonsList.length; i++ ) (function(i){ 
    buttonsList[i].onclick = function() {
      sendMessage(commonList[i])
      console.log(commonList[i])
      commonFlexbox.remove()
    }
  })(i);
  box.append(commonFlexbox);
  var objDiv = document.getElementById("chatform");
  objDiv.scrollTop = objDiv.scrollHeight;
}
function repliesList(replies)
{
  for(i=0;i<replies.length;i++)
  {
    var send = document.createElement("div");
    send.setAttribute("class","d-flex flex-row");      
    var msgbox = document.createElement("div");
    msgbox.setAttribute("class","recbox");
    var msg = document.createTextNode(replies[i]);
    msgbox.appendChild(msg);
    send.appendChild(msgbox);
    box.appendChild(send);
  }
  
  var objDiv = document.getElementById("chatform");
  objDiv.scrollTop = objDiv.scrollHeight;

}

function sendMessage(textContent)
{
var send = document.createElement("div");
    send.setAttribute("class","d-flex flex-row-reverse")
    var msgbox = document.createElement("div");
    msgbox.setAttribute("class","sendbox")
    var msg = document.createTextNode(textContent);
    msgbox.appendChild(msg)
    send.appendChild(msgbox)
    box.appendChild(send)
    
    $.ajax(
    {
      type: "POST",
      url:'http://localhost:8000/chat',
      headers: {'X-CSRFToken':token},
      data:
      {
          'text':textContent
      },
      dataType:'json',
      success:function(data)
      { console.log(data)
        var send = document.createElement("div");
        send.setAttribute("class","d-flex flex-row");
        var msgbox = document.createElement("div");
        msgbox.setAttribute("class","recbox");
        var msg = document.createTextNode(data['Bot']);
        msgbox.appendChild(msg);
        send.appendChild(msgbox);
        box.appendChild(send);
        var objDiv = document.getElementById("chatform");
        objDiv.scrollTop = objDiv.scrollHeight
        console.log(data)
        if (data['Bot_'])
        {
          var send = document.createElement("div");
          send.setAttribute("class","d-flex flex-row");      
          var msgbox = document.createElement("div");
          msgbox.setAttribute("class","recbox");
          var msg = document.createTextNode(data['Bot_']);
          msgbox.appendChild(msg);
          send.appendChild(msgbox);
          box.appendChild(send);
          var objDiv = document.getElementById("chatform");
          objDiv.scrollTop = objDiv.scrollHeight
        }
        
        if (data['Bot__'])
        {    
          var link = data['Bot__'];
          console.log(link)
          var send = document.createElement("div");
          send.setAttribute("class","d-flex flex-row");
          var msgbox = document.createElement("div");
          msgbox.setAttribute("class","recbox");
          var a = document.createElement('a');
          var msg = document.createTextNode(link);
          a.appendChild(msg)
          a.title="Tilte";
          a.href=link;
          console.log(a)
          msgbox.appendChild(a);
          send.appendChild(msgbox);
          box.appendChild(send);
          var objDiv = document.getElementById("chatform");
          objDiv.scrollTop = objDiv.scrollHeight
        }
        if(data["Bot_Q"])
        {
          console.log("Bot Q")
          commonButtons(data["Bot_Q"],"d-flex justify-content-around")
        } 
        if(data["Bot_C"])
        {
          commonButtons(data["Bot_C"],"d-flex flex-wrap")

        } 
        if(data["Bot_N"])
        {
          sendMessage(data["Bot_N"])
        }
        if(data["Bot_L"])
        {
          repliesList(data["Bot_L"])
        }
      }
    })
}

$("#input-content").on('keypress',function(e)
{
  if(e.which == 13)
  {
    sendMessage(input.value)
    input.value=''
  }
})

function popup()
{
  console.log('Opened');
  document.getElementById('chatform').style.display='block';
  document.getElementById('chatbtn').style.display='none';
}

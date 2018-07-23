var active_users = [];
var current_user = {};
var io = io.connect('http://localhost:5000');

io.on('connect', function() {
  io.emit('user_connected')
})

io.on('get_users', function(users) {
  active_users = users
  let $active_user_div = $("#active_users")
  active_users.forEach(function(user) {
      var rowElement = document.createElement('div')
      rowElement.classList.add('row')
      var colElement = document.createElement('div')
      colElement.classList.add('col-md-12')
      rowElement.append(colElement)
      var panelElement = document.createElement('div')
      var notificationElement = document.createElement('span')
      notificationElement.dataset.id = user['email']
      notificationElement.classList.add('badge','badge-info')
      notificationElement.style = "margin-left: 4px"
      panelElement.classList.add('card')
      colElement.append(panelElement)
      var name = document.createElement('h5')
      name.innerText = user.first_name+" "+user.last_name
      name.append(notificationElement)
      var email = document.createElement('h6')
      email.innerText = user.email
      var panelBodyElement = document.createElement('div')
      var chatBtn = document.createElement('button')
      chatBtn.addEventListener('click', function() {
          current_user = user
          $("#name").text(user['first_name']+" "+user['last_name'])
          $("#messages").empty()
      })
      chatBtn.classList.add('btn','btn-primary')
      chatBtn.innerText = 'Message'
      panelBodyElement.classList.add('card-body')
      panelBodyElement.append(name)
      panelBodyElement.append(email)
      panelBodyElement.append(chatBtn)
      panelElement.append(panelBodyElement)

      $active_user_div.append(rowElement)
  })
})

io.on('receive_message', function(packet) {
    if (current_user['email'] == packet.from) {
      var messageElement = document.createElement('h5')
      messageElement.innerText = packet.message
      $("#messages").append(messageElement)
    } else {
        var initialCount = $("[data-id='"+packet['from']+"'").text()
        if (!initialCount) {
          initialCount = 1
        } else {
          initialCount = parseInt(initialCount) + 1
        }
         $("[data-id='"+packet['from']+"'").text(initialCount)
    }
})

$("#send").on('click', function() {
    $message_box = $("#chat_message")
    var message = $message_box.val();
    $("#send").prop('disabled', true)
    $("#messages").append("<h5 class='clear-fix' style='text-align: right'>"+message+"</h5>")
    $message_box.val('')
    io.emit('send_message', { to: current_user['email'], message: message })
});

$("#chat_message").on('change', function(e) {
  if (e.target.value) {
    $("#send").prop('disabled', false)
  } else {
    $("#send").prop('disabled', false)
  }
})
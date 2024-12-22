document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#details-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('#compose-form').addEventListener('submit', send_email)
}


// by default, inbox is loaded and start listening for click events
// when a folder is clicked, load_mailbox is triggered, else compose_mail is triggered
// index (js)>compose_mail (js)>send_email (js, fetch post method)>compose.py (views.py return)> load_mailbox


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#details-view').style.display = 'none';

  // displays the name of the selected mailbox by updating the innerHTML
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // update to show emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    console.log(emails);

    // ... do something else with emails ...
    emails.forEach(email => {
      // console.log(element)
      let sender = email.sender
      let subject = email.subject
      let timestamp = email.timestamp
      let read = email.read
      let mail_id = email.id

      // create a new div
      const element = document.createElement('div');

      // print title, subject and timestamp
      element.innerHTML = `<b>From:</b> ${sender}<p><b>Subject:</b> ${subject}<br>${timestamp}`;
      element.className = 'list-group-item'
      // listen for click event
      element.addEventListener('click', function() {
          console.log('This element has been clicked!')
          // get a json representation of the email
          load_details(mail_id)
      });

      // If the email is unread, it should appear with a white background. If the email has been read, it should appear with a gray background.
      if(read){
        element.style.backgroundColor = 'lightgrey'
      }
      // append new div to #emails-view 
      document.querySelector('#emails-view').append(element);
    });
    
});
}

function load_details(mail_id) {
  document.querySelector('#details-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  fetch(`/emails/${mail_id}`)
  .then(response => response.json())
  .then(details => {    
    // Print email
    console.log(details);
    // sender, recipients, subject, timestamp, body 
    let sender = details.sender
    let recipients = details.recipients
    let subject = details.subject
    let timestamp = details.timestamp
    let body = details.body

    // create a new div
    const element = document.createElement('div');
    element.innerHTML = `
    <ul class="list-group">
      <li class="list-group-item"><b>From:</b> ${sender}</li>
      <li class="list-group-item"><b>To:</b> ${recipients}</li>
      <li class="list-group-item"><b>Subject:</b> ${subject}</li>
      <li class="list-group-item"><b>Timestamp:</b> ${timestamp}</li>
      <li class="list-group-item">${body}</li>
    </ul>`

    // `<b>From:</b> ${sender}, to: ${recipients}</b> <p>${subject} ${timestamp}</p><br>${body}`

    document.querySelector('#details-view').innerHTML = element.innerHTML      

    if (!details.read){
      fetch(`/emails/${mail_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      })
    }
    // --------------------------------------
    // create archiving/unarchiving buttons
    const btn_arch = document.createElement('button')
    if(details.archived){
      btn_arch.innerHTML = "Unarchive"
      btn_arch.className = 'btn btn-primary'
    } else {
      btn_arch.innerHTML = "Archive"
      btn_arch.className = 'btn btn-secondary'
    }
    console.log(btn_arch) 
    // add button to bottom of details div
    document.querySelector('#details-view').append(btn_arch)

    // add event listener for button click to trigger change in archive status
    // document.querySelector('#details-view').lastChild.
    btn_arch.onclick = function(){    
      console.log('btn_arch button clicked')
      fetch(`/emails/${mail_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: !details.archived
        })
      })
      .then(() => {load_mailbox('inbox')})
    }

    // --------------------------------------
    // reply logic
    const btn_reply = document.createElement('button')
    btn_reply.innerHTML = "Reply"
    btn_reply.className = "btn btn-info"
    document.querySelector('#details-view').append(btn_reply)
    btn_reply.onclick = function() {
      // console.log('reply me button')
      compose_email()

      // prefill recipient
      document.querySelector('#compose-recipients').value = sender;
      // prefill subject
      // console.log(subject.slice(0,3))
      if(subject.slice(0,3) != 'Re:') {
        document.querySelector('#compose-subject').value = 'Re: ' + subject;
      } else {
        document.querySelector('#compose-subject').value = subject
      }
      // prefill body
      document.querySelector('#compose-body').value = `On ${timestamp} ${sender} wrote ${body}`;
    }
  });
}

function send_email(event) {
  event.preventDefault();
  // console.log('hi')
  // store values
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // send data to backend, calling function compose in views.py
  fetch('/emails', {
    method: 'POST',
    // send body of data in json
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  // back to js after django
  .then(response => response.json())
  // result is what the function django return to you
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent')
  });

  return false
}
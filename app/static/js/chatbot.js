// var socket;
$(document).ready(function() {
	$('form').on('submit', function(event) {
		$.ajax({
			data : {
				name: $('.username').val(),
				message : $('#message').val()
			},
			type : 'POST',
			url : '/chatbot',
			success: function(response) {
				$("body").html(response);
				const conversationDiv = document.getElementById('conversation');
				conversationDiv.scrollTop = conversationDiv.scrollHeight;
			},
		})
        clearChat();
		event.preventDefault();
	});
});

function speechToText() {
	var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;
	var recognition = new SpeechRecognition();

	recognition.onstart = function() {};

	recognition.onspeechend = function() {
		recognition.stop();
	}

	recognition.onresult = function(event) {
		var transcript = event.results[0][0].transcript;
		$('#message').val(transcript);
		$(".send-btn").click();	
	};

	recognition.start();
}

function clearChat() {
    $('#message').val('');
}

$(".option-btn").click(function () {
	var text = $(this).text();
	$("#message").val(text);
	$(".send-btn").click();	
});

$('.reviews').click(function() {
	var text = $(this).data('datac');      
	$("#message").val(text);
	$(".send-btn").click();	  
});

$('.booking').click(function() {
	var text = $(this).data('datac');      
	$("#message").val(text);
	$(".send-btn").click();	
});

var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})
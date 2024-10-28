$(document).ready(function() {
    const messageForm = $('#message-form');
    const messageInput = $('#message-input');
    const messagesDiv = $('#messages');
    const userList = $('#user-list');
    const createChannelButton = $('#create-channel');
    const newChannelInput = $('#new-channel-input');
    const logoutButton = $('#logout');
    const channelList = $('#channel-list');

    // Mesaj gönderme işlemi
    messageForm.on('submit', function(e) {
        e.preventDefault();
        const message = messageInput.val();
        $.post('/send', { message: message }, function(response) {
            messagesDiv.append(`<div class="message">${response.message}</div>`);
            messageInput.val('');  // Mesaj kutusunu temizle
        });
    });

    // DM butonuna tıklayınca DM gönder
    $(document).on('click', '.dm-button', function() {
        const recipient = $(this).data('recipient');
        const message = prompt(`${recipient} için mesajınızı yazın:`);
        if (message) {
            $.post('/dm', { recipient: recipient, message: message }, function(response) {
                alert(response.message);
            });
        }
    });

    // Kanal oluşturma
    createChannelButton.on('click', function() {
        const channelName = newChannelInput.val();
        if (channelName) {
            $.post('/create_channel', { channel_name: channelName }, function(response) {
                channelList.append(`<li class="channel-item" data-channel="${response.channel}">${response.channel}</li>`);
                newChannelInput.val('');  // Kanal girişini temizle
            });
        }
    });

    // Kanal değişimi
    $(document).on('click', '.channel-item', function() {
        const channelName = $(this).data('channel');
        $.post('/switch_channel', { channel_name: channelName }, function(response) {
            $('#messages').empty();  // Eski mesajları temizle
            // Yeni kanala ait mesajları yükleme kodu ekleyebilirsiniz
        });
    });

    // Çıkış yapma
    logoutButton.on('click', function() {
        window.location.href = '/logout';
    });

    // Mesajları yükleme
    function loadMessages() {
        $.get('/messages', function(data) {
            messagesDiv.empty();  // Mesajları temizle
            data.forEach(msg => {
                messagesDiv.append(`<div class="message">${msg}</div>`);
            });
        });
    }

    // Belirli aralıklarla mesajları güncelle
    setInterval(loadMessages, 3000); // Her 3 saniyede bir güncelle
});

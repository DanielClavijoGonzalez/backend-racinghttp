$(function () {
  //socket iniciado
  let token =
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsImlhdCI6MTYxNjIyMDk4NSwiZXhwIjoxNjE2MjIyNzg1fQ.ASFA8bU3uGP-xUbIq11Iwx5UKSt52facK0si9LmPrS0";
  let socket = io("", {
    query: "token=" + token,
  });
  const user = 123321;

  function now() {
    return new Date();
  }
  function formatAMPM(date) {
    let hours = date.getHours();
    let minutes = date.getMinutes();
    let ampm = hours >= 12 ? "PM" : "AM";
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? "0" + minutes : minutes;
    let strTime = hours + ":" + minutes + " " + ampm;
    return strTime;
  }

  //variables
  const message = $("#chat-message");
  const chatb = $("#chat");

  message.focus();

  $("#message-box").submit(function (e) {
    e.preventDefault();
    document.getElementById(
      "chat"
    ).innerHTML += `<b style="color: red">${user}:</b> ${message.val()} <br>
    <small>${now().getDate()}/${
      now().getMonth() + 1 <= 9
        ? "0" + (now().getMonth() + 1).toString()
        : now().getMonth()
    }/${now().getFullYear().toString().slice(-2)}, ${formatAMPM(
      now()
    )}</small>`;
    socket.emit("general-message", {
      remitente:
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTM3NzcwNTQsImVtYWlsIjoiZ3J1cG9qZWRAZ21haWwuY29tIn0.waL5_h-DdgFUG3EaSFp6njh_X-SB8eIPCdwmATEyH3E",
      emitente: user,
      msg: message.val(),
      img: "",
      dateSend: `${now().getDate()}/${
        now().getMonth() + 1 <= 9
          ? "0" + (now().getMonth() + 1).toString()
          : now().getMonth()
      }/${now().getFullYear().toString().slice(-2)}, ${formatAMPM(now())}`,
    });
    message.val("");
  });

  socket.on("general-message-server", function (data) {
    if (data.remitente == user) {
      document.getElementById("chat").innerHTML += `
      <b style="color: red">${data.emitente}:</b> ${data.msg}
       <br>
       <small>${data.dateSend}</small>
      `;
    }
  });
  socket.on("connect", () => {
    console.log("CONNECTED SCKT");
  });

  socket.on("unauthorized", function (error) {
    console.error("ERROR TOKEN");
  });
});

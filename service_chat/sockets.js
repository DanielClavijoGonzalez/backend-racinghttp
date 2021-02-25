const io = require("socket.io", {
  pingInterval: 10000,
  pingTimeout: 5000,
});
const socketioJwt = require("socketio-jwt");
let jwtSecret = "BASE64";

setInterval(() => {
  console.log("");
}, 30000);

module.exports = function (server) {
  let sockets = io.listen(server, {
    reconnectionDelayMax: 5000,
  });
  sockets.set(
    "authorization",
    socketioJwt.authorize({
      secret: jwtSecret,
      handshake: true,
    })
  );

  sockets.on("connection", function (socket) {
    console.log(
      `SERVIDOR: Usuario: ${socket.id.slice(
        0,
        10
      )} ha establecido una nueva conexión`
    );
    console.log(socket.client.request.decoded_token.user_id, "connected");

    socket.on("general-message", function (data) {
      console.log(`Mensaje de ${data.emitente.slice(
        0,
        10
      )} para ${data.remitente.slice(0, 10)}
      -------------------------------------------------------------
      `);
      sockets.emit("general-message-server", data);
      console.log("Respuesta emitida");
    });

    socket.on("general-writing", function (data) {
      if (data.writing) {
        console.log(
          `El usuario: ${data.emitente.slice(
            0,
            10
          )} Está escribiendole a el usuario ${data.remitente.slice(0, 10)}`
        );
        console.log("----");
      }

      sockets.emit("general-writing-emit", data);

      console.log(
        `Se ha enviado señal a el usuario ${data.remitente.slice(
          0,
          10
        )} de que el usuario ${data.emitente.slice(0, 10)} está en línea`
      );
    });
  });

  sockets.on("disconnect", (reason) => {
    console.log(`Disconnected, Reason: ${reason}`);
    sockets.disconnect();
  });
};

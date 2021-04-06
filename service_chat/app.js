const http = require("http");
const express = require("express");
const app = express();
const morgan = require("morgan");

const server = http.createServer(app);

// configuración del Servidor
app.set("port", process.env.port || 3000);

app.use(morgan("dev"));

// app.get("/about", function (req, res) {
//   res.send("about");
// });
const jwt = require("jsonwebtoken");
// other requires

const jwtSecret = "BASE64";

server.listen(app.get("port"), function () {
    console.log(`Running in port ${app.get("port")}`);
});

// este es la logica de los sockets
require("./sockets")(server);

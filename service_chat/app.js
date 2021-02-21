const http = require("http");
const express = require("express");
const app = express();
const morgan = require("morgan");

const server = http.createServer(app);

// configuración del Servidor
app.set("port", 3000);

app.use(morgan("dev"));
app.use(express.static(__dirname + "/public"));

// app.get("/about", function (req, res) {
//   res.send("about");
// });
const jwt = require("jsonwebtoken");
// other requires

const jwtSecret = "BASE64";

app.post("/login", function (req, res) {
  // TODO: validate the actual user user
  let profile = {
    first_name: "John",
    last_name: "Doe",
    email: "john@doe.com",
    id: 123,
  };

  // we are sending the profile in the token
  let token = jwt.sign(profile, jwtSecret, {
    expiresIn: "30m",
    algorithm: "HS256",
  });

  res.json({ token: token });
});

server.listen(app.get("port"), function () {
  console.log("servidor en puerto 3000");
});

// este es la logica de los sockets
require("./sockets")(server);

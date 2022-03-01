var fs = require("fs");
var ss = require("socket.io-stream");
var io = require("socket.io")({
  allowEIO3: true, // false by default
  transport: ["websocket"],
  credentials: true,
});

// var socket = io.connect("localhost:5000");
var stream = ss.createStream();

//Create a new file stream. You can write buffer data into this file.
var outStream = fs.createWriteStream("./videos/out.mp4");

io.on("filename", function (socket) {
  ss(socket).emit("filename", stream);
  stream.pipe(outStream);
});

// io.on("filename", function (socket) {
//   console.log("filename");
//   socket.on("blob", function (data) {
//     //You will received buffer data from browser client and you will write buffer to client.
//     console.log(data);
//     outStream.write(data);
//   });
// });

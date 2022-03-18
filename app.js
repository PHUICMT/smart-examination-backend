var tools = require("./services/video-receiver");

var express = require("express");
var path = require("path");
var cookieParser = require("cookie-parser");
var cors = require("cors");
var formidable = require("formidable");

var app = express();

var corsOptions = {
  origin: ["http://localhost:3000"],
};

app.use(cors(corsOptions));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, "public")));

app.post("/upload-video", function (req, res) {
  console.log(req.body);

  if (!req.body) {
    console.log("No file received");
    return res.status(400).json({ message: "Can't Accept" });
  } else {
    tools.VideoReceiver(req.body);
    return res.status(200);
  }
});

app.listen(5000, () => console.log("Server Started!! 5000"));
